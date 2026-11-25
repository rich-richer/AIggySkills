#!/usr/bin/env python3
"""Generate images through OpenRouter's /api/v1/images endpoint.

Reads the API key from $OPENROUTER_API_KEY. Never accepts a key as an argument,
so keys stay out of shell history and process listings.
"""

import argparse
import base64
import json
import math
import mimetypes
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://openrouter.ai/api/v1/images"
DEFAULT_MODEL = "bytedance-seed/seedream-4.5"
# Measured: ~USD 0.014 / 5s, against Seedream's flat USD 0.040 / 23s.
DRAFT_MODEL = "black-forest-labs/flux.2-klein-4b"
TIMEOUT = 300  # image generation can take a while

# python.org builds on macOS ship no usable CA bundle; fall back to certifi's.
try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

ASPECT_RATIOS = {
    "1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3", "4:5", "5:4",
    "1:2", "2:1", "1:4", "4:1", "1:8", "8:1", "9:21", "21:9", "auto",
}
RESOLUTIONS = {"512", "1K", "2K", "4K"}
FORMATS = {"png", "jpeg", "webp", "svg"}
PIXEL_RE = re.compile(r"\d+x\d+")

# Seedream rejects anything smaller; other models have no such floor.
SEEDREAM_MIN_PIXELS = 3_686_400
DRAFT_PIXELS = 1_048_576  # ~1K-equivalent budget for models without a floor

# Appended verbatim to every prompt in a run. Seeds do not work on Seedream, so
# a repeated wording anchor is the main lever for making a set cohere.
STYLES = {
    "business": (
        "clean corporate photography, soft diffused studio lighting, neutral palette of "
        "white and grey with one muted blue accent, uncluttered composition with generous "
        "negative space, shallow depth of field, understated and professional"
    ),
    "tech": (
        "sleek futuristic technology aesthetic, dark charcoal background, cool cyan and "
        "electric blue accent lighting, crisp rim light along edges, contrast between "
        "glossy and matte surfaces, high contrast, cinematic"
    ),
    "illustration": (
        "flat vector illustration, bold clean shapes, limited harmonious palette of four "
        "colors, minimal shading, no photographic texture, generous white space, friendly "
        "modern editorial style"
    ),
    "warm": (
        "warm natural photography, golden hour light, soft directional shadows, amber and "
        "cream palette, gentle bokeh, 85mm prime lens, inviting and human"
    ),
    "minimal": (
        "extreme minimalism, single subject centered on a plain seamless background, soft "
        "even lighting, muted near-monochrome palette, large areas of empty space, "
        "product-catalogue precision"
    ),
}


def draft_size(model, aspect):
    """Smallest sensible size for the model, as explicit WxH.

    Always explicit pixels rather than a tier: tiers get normalized per-provider
    and some models (FLUX) then ignore aspect_ratio entirely, silently returning
    a square — which defeats the point of previewing a composition.
    """
    floor = SEEDREAM_MIN_PIXELS if "seedream" in model else DRAFT_PIXELS
    try:
        a, b = (int(x) for x in (aspect or "1:1").split(":"))
    except ValueError:  # e.g. "auto"
        a = b = 1
    k = math.sqrt(floor / (a * b))
    while True:
        w = math.ceil(a * k / 16) * 16
        h = math.ceil(b * k / 16) * 16
        if w * h >= floor:
            return f"{w}x{h}"
        k *= 1.01


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def slugify(text, limit=48):
    slug = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip()
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:limit].strip("-").lower() or "image"


def read_batch(path):
    """One prompt per line; blank lines and # comments ignored."""
    f = Path(path).expanduser()
    if not f.is_file():
        die(f"batch file not found: {path}")
    prompts = [
        line.strip()
        for line in f.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not prompts:
        die(f"no prompts found in {path}")
    return prompts


def to_reference(src):
    """Turn a local path or URL into an input_references entry."""
    if src.startswith(("http://", "https://", "data:")):
        url = src
    else:
        path = Path(src).expanduser()
        if not path.is_file():
            die(f"reference image not found: {src}")
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        b64 = base64.b64encode(path.read_bytes()).decode()
        url = f"data:{mime};base64,{b64}"
    return {"type": "image_url", "image_url": {"url": url}}


def post(body, key):
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        try:
            detail = json.dumps(json.loads(detail), indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        hint = {
            401: "  -> check that OPENROUTER_API_KEY is a valid key",
            402: "  -> insufficient credits on the OpenRouter account",
            404: "  -> model id not found; verify it supports image output",
            429: "  -> rate limited, retry in a moment",
        }.get(e.code, "")
        raise RuntimeError(f"HTTP {e.code} from OpenRouter\n{detail}{chr(10) + hint if hint else ''}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"network failure: {e.reason}")


def generate(prompt, args, model, key, outdir, refs, index=None, total=None):
    """Generate one prompt. Returns (saved_paths, cost)."""
    style = STYLES[args.style] if args.style else None
    full = f"{prompt}, {style}" if style else prompt

    requested = draft_size(model, args.aspect) if args.draft else args.resolution
    size = requested if requested and PIXEL_RE.fullmatch(requested) else None
    resolution = None if size else requested

    body = {"model": model, "prompt": full, "output_format": args.format}
    if args.n != 1:
        body["n"] = args.n
    if resolution:
        body["resolution"] = resolution
    if size:
        body["size"] = size
    # Explicit WxH already encodes the ratio; sending both risks a conflict.
    if args.aspect and not size:
        body["aspect_ratio"] = args.aspect
    if args.seed is not None:
        body["seed"] = args.seed
    if refs:
        body["input_references"] = [to_reference(r) for r in refs]

    tag = f"[{index}/{total}] " if total else ""
    print(f"{tag}{prompt}", flush=True)

    started = time.time()
    result = post(body, key)
    elapsed = time.time() - started

    images = result.get("data") or []
    if not images:
        raise RuntimeError(f"no images returned:\n{json.dumps(result, indent=2, ensure_ascii=False)}")

    outdir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    slug = slugify(prompt)
    prefix = "draft-" if args.draft else ""
    if index:
        prefix = f"{index:02d}-{prefix}"

    saved = []
    for i, item in enumerate(images):
        b64 = item.get("b64_json")
        if not b64:
            print(f"  warning: image {i} had no b64_json, skipping", file=sys.stderr)
            continue
        ext = (item.get("media_type") or f"image/{args.format}").split("/")[-1]
        ext = {"jpeg": "jpg", "svg+xml": "svg"}.get(ext, ext)
        suffix = f"-{i + 1}" if len(images) > 1 else ""
        path = outdir / f"{stamp}-{prefix}{slug}{suffix}.{ext}"
        path.write_bytes(base64.b64decode(b64))
        saved.append(path)

    if not saved:
        raise RuntimeError("every returned image was empty")

    cost = (result.get("usage") or {}).get("cost")
    line = f"  {elapsed:.1f}s"
    if isinstance(cost, (int, float)):
        line += f"  |  USD {cost:.4f}"
    print(line)
    for path in saved:
        print(f"  -> {path.resolve()}  ({path.stat().st_size / 1024:.0f} KB)")
    return saved, (cost if isinstance(cost, (int, float)) else 0.0)


def main():
    ap = argparse.ArgumentParser(
        description="Generate images via OpenRouter.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  gen.py 'a red panda astronaut' --aspect 16:9 --resolution 4K\n"
            "  gen.py 'a red panda astronaut' --aspect 16:9 --draft\n"
            "  gen.py 'make this watercolor' --ref ./photo.jpg --resolution 4K\n"
            "  gen.py --batch slides.txt --style business --aspect 16:9 --resolution 4K\n"
            "  gen.py --batch slides.txt --style tech --anchor --aspect 16:9 --resolution 4K\n"
        ),
    )
    ap.add_argument("prompt", nargs="?", help="what to draw (omit when using --batch)")
    ap.add_argument("-m", "--model", help=f"default: {DEFAULT_MODEL}; with --draft: {DRAFT_MODEL}")
    ap.add_argument("-o", "--outdir", default="./generated-images", help="default: ./generated-images")
    ap.add_argument("-n", type=int, default=1, help="images per prompt (default: 1)")
    ap.add_argument("--aspect", metavar="RATIO", help=f"one of: {', '.join(sorted(ASPECT_RATIOS))}")
    ap.add_argument("--resolution", metavar="RES",
                    help=f"tier ({', '.join(sorted(RESOLUTIONS))}) or explicit pixels, e.g. 2560x1440")
    ap.add_argument("--draft", action="store_true",
                    help="fast cheap preview for trying compositions: swaps in a budget model "
                         "at its smallest size (~3x cheaper, ~4x faster). Style will differ "
                         "from the final; use -m to keep a specific model.")
    ap.add_argument("--style", choices=sorted(STYLES),
                    help="append a shared style anchor to every prompt, so a set coheres")
    ap.add_argument("--list-styles", action="store_true", help="print the style presets and exit")
    ap.add_argument("--batch", metavar="FILE",
                    help="file of prompts, one per line (# comments and blank lines ignored)")
    ap.add_argument("--anchor", action="store_true",
                    help="with --batch: reuse the first image as a reference for the rest. "
                         "Strongest consistency, but tends to homogenize composition too.")
    ap.add_argument("--yes", action="store_true", help="skip the batch cost confirmation")
    ap.add_argument("--format", default="png", metavar="FMT", help=f"one of: {', '.join(sorted(FORMATS))}")
    ap.add_argument("--seed", type=int, help="seed (note: silently ignored by Seedream)")
    ap.add_argument("--ref", action="append", default=[], metavar="PATH_OR_URL",
                    help="reference image for editing / img2img (repeatable)")
    args = ap.parse_args()

    if args.list_styles:
        for name in sorted(STYLES):
            print(f"\n{name}:\n  {STYLES[name]}")
        return

    if not args.prompt and not args.batch:
        die("give a prompt, or --batch FILE")
    if args.prompt and args.batch:
        die("--batch replaces the positional prompt; pass one or the other")
    if args.anchor and not args.batch:
        die("--anchor only applies to --batch runs")

    # Strip stray whitespace: keys pasted from CRLF text files pick up \r\n
    key = "".join((os.environ.get("OPENROUTER_API_KEY") or "").split())
    if not key:
        die("OPENROUTER_API_KEY is not set.\n"
            "  Add to ~/.zshenv:  export OPENROUTER_API_KEY='sk-or-v1-...'\n"
            "  then open a new terminal.")

    if args.draft and args.resolution:
        die("--draft and --resolution are mutually exclusive")
    if args.aspect and args.aspect not in ASPECT_RATIOS:
        die(f"invalid --aspect '{args.aspect}'; allowed: {', '.join(sorted(ASPECT_RATIOS))}")
    if args.resolution and args.resolution not in RESOLUTIONS and not PIXEL_RE.fullmatch(args.resolution):
        die(f"invalid --resolution '{args.resolution}'; use a tier "
            f"({', '.join(sorted(RESOLUTIONS))}) or explicit pixels like 2560x1440")
    if args.format not in FORMATS:
        die(f"invalid --format '{args.format}'; allowed: {', '.join(sorted(FORMATS))}")

    model = args.model or (DRAFT_MODEL if args.draft else DEFAULT_MODEL)
    if args.draft and args.model and "seedream" in model:
        print("note: Seedream bills a flat rate per image — --draft saves time here, not money",
              file=sys.stderr)

    prompts = read_batch(args.batch) if args.batch else [args.prompt]
    outdir = Path(args.outdir).expanduser()

    print(f"model:  {model}")
    if args.style:
        print(f"style:  {args.style}")
    if args.draft:
        print(f"size:   {draft_size(model, args.aspect)}   [draft]")
    elif args.resolution:
        print(f"size:   {args.resolution}")

    # A batch multiplies a per-image charge; say the number before spending it.
    if len(prompts) > 1:
        est = 0.015 if args.draft else 0.040
        total_est = est * len(prompts) * args.n
        print(f"batch:  {len(prompts)} prompts x {args.n} = {len(prompts) * args.n} images"
              f"  (~USD {total_est:.2f})")
        if not args.yes and sys.stdin.isatty():
            if input("proceed? [y/N] ").strip().lower() not in ("y", "yes"):
                print("aborted"); return
    print()

    refs = list(args.ref)
    spent, made, failed = 0.0, [], []
    for i, prompt in enumerate(prompts, 1):
        try:
            saved, cost = generate(
                prompt, args, model, key, outdir, refs,
                index=i if len(prompts) > 1 else None,
                total=len(prompts) if len(prompts) > 1 else None,
            )
            spent += cost
            made.extend(saved)
            if args.anchor and i == 1 and saved:
                refs = [str(saved[0])]
                print("  (anchored — remaining prompts will reference this image)")
        except RuntimeError as e:
            print(f"  FAILED: {e}", file=sys.stderr)
            failed.append(prompt)
        if i < len(prompts):
            print()

    if len(prompts) > 1:
        print(f"\n{'=' * 52}")
        print(f"{len(made)} images  |  USD {spent:.4f} total  ->  {outdir.resolve()}")
        if failed:
            print(f"{len(failed)} failed:")
            for p in failed:
                print(f"  - {p}")
    if failed and not made:
        sys.exit(1)

    if args.draft and not args.batch:
        rerun = f"  gen.py '{args.prompt}' --resolution 4K"
        if args.aspect:
            rerun += f" --aspect {args.aspect}"
        if args.style:
            rerun += f" --style {args.style}"
        if args.model:
            rerun += f" -m {args.model}"
        print(f"\ndraft ({model}) — composition only; style will differ.")
        print(f"once the framing works, rerun on {args.model or DEFAULT_MODEL}:")
        print(rerun)


if __name__ == "__main__":
    main()
