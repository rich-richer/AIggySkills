---
name: image-gen
description: Generate or edit raster images (photos, illustrations, characters, scenes, product shots, logos, textures) by calling real image models through OpenRouter — Seedream 4.5 by default, plus Nano Banana / GPT-Image / FLUX / Recraft. Use whenever the user asks to "draw", "generate an image", "make a picture", "画一张", "生成图片", "做张图", or wants an existing image edited, restyled, or extended. Also use for whole sets of images — slide decks, website hero and card art, social assets, "给PPT配图", "网页配图" — via --batch with a shared --style anchor. Do NOT use for diagrams, flowcharts, charts, or UI mockups — hand-write SVG/HTML for those instead.
---

# Image generation via OpenRouter

Claude cannot natively produce raster images. This skill shells out to real
diffusion models so it can.

## When to use this vs. writing code

| Need | Use |
|---|---|
| Photo, illustration, character, scene, texture, product shot | **This skill** |
| Editing / restyling / extending an existing image | **This skill** (`--ref`) |
| Flowchart, architecture diagram, data chart, UI mockup | Hand-write SVG / HTML — do *not* burn API credits |

## Setup check

The script needs `OPENROUTER_API_KEY` in the environment. If it errors that the
key is missing, tell the user to add it to **`~/.zshenv`** themselves — never ask
them to paste the key into chat, and never write the key into a file.

It must be `~/.zshenv`, not `~/.zshrc`: the Bash tool runs a *non-interactive*
shell, and zsh only reads `.zshrc` for interactive ones. A key in `.zshrc` works
in the user's terminal but stays invisible here.

## Usage

```bash
python3 ~/.claude/skills/image-gen/scripts/gen.py "PROMPT" [options]
```

| Option | Values | Notes |
|---|---|---|
| `-m, --model` | see table below | default `bytedance-seed/seedream-4.5` |
| `-o, --outdir` | path | default `./generated-images` |
| `-n` | int | number of images |
| `--aspect` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `4:5` `21:9` `auto` … | |
| `--resolution` | `512` `1K` `2K` `4K`, or `2560x1440` | Seedream: use `4K`, see below |
| `--draft` | flag | cheap fast preview; see below. Excludes `--resolution` |
| `--style` | `business` `tech` `illustration` `warm` `minimal` | shared style anchor; see *Sets* |
| `--list-styles` | flag | print the presets and exit |
| `--batch` | path to .txt | one prompt per line; replaces the positional prompt |
| `--anchor` | flag | `--batch` only: reuse image 1 as a reference for the rest |
| `--yes` | flag | skip the batch cost confirmation |
| `--format` | `png` `jpeg` `webp` `svg` | `svg` only for Recraft vector models |
| `--seed` | int | **ignored by Seedream** — see below |
| `--ref` | path or URL | reference image for editing / img2img; repeatable |

Examples:

```bash
# text to image
python3 ~/.claude/skills/image-gen/scripts/gen.py "a red panda astronaut, studio lighting" --aspect 16:9 --resolution 4K

# cheap composition preview first
python3 ~/.claude/skills/image-gen/scripts/gen.py "a red panda astronaut, studio lighting" --aspect 16:9 --draft

# edit an existing image
python3 ~/.claude/skills/image-gen/scripts/gen.py "turn this into a watercolor painting" --ref ./photo.jpg --resolution 4K
```

## `--draft`: preview the composition, not the final

Swaps in `black-forest-labs/flux.2-klein-4b` at ~1MP. Measured against a
Seedream 4K run: **USD 0.015 / 7s vs USD 0.040 / 23s** — ~3x cheaper, ~3x faster.

Use it to settle framing, camera angle, and subject placement, then rerun the
same prompt without `--draft` for the real image. The script prints the exact
rerun command when a draft finishes.

Two things a draft will **not** do:

- **Render text.** Budget models invent fake glyphs. Never judge CJK or any
  in-image lettering from a draft — that is precisely what Seedream is for.
- **Predict the final composition.** Measured on an identical prompt: FLUX
  centered a symmetrical lone peak with a lens-flare sun; Seedream put the peak
  on the left third with backlit rim light and a ridgeline running right.
  Subject placement, camera angle, and light direction all changed. **Nothing
  carries over on its own.**

So a draft answers *"is this prompt pointing the right direction?"* — not
*"is this the shot?"*. Use it to try several wordings cheaply, then commit.

### Locking a composition

**`--seed` does not work on Seedream 4.5 — it is silently ignored.** Verified:
two runs of one prompt at `--seed 12345` gave entirely different images (mean
pixel difference 48.6/255, *zero* identical pixels — one cat sitting upright in
profile, one lying down asleep beside a coffee mug). The parameter is accepted
without error, so the failure is invisible. Untested on other models.

That leaves **`--ref` as the only working composition lock.** Feeding an image
back in does carry its layout across, even across models: subject placement, sun
position, and background arrangement all followed the reference, where the same
prompt without `--ref` reframed the scene entirely.

Two costs to weigh:

- Upscaling a ~1MP reference to 4K leaves background detail soft and mushy. Pass
  the largest reference you have.
- Wording like "enhance detail / layering" pushes the result toward an
  oversaturated HDR look, away from the naturalistic tone the same model
  produces from text alone.

**Practical consequence:** with flat pricing *and* dead seeds, Seedream has no
cheap iteration path — every attempt costs the same USD 0.04. So iterate prompt
wording on FLUX (`--draft`, USD 0.015), and once a Seedream result is close,
refine it through `--ref` instead of re-rolling from text and losing the framing.

`-m` overrides the model swap and keeps yours at its smallest size. On Seedream
that saves time but *not* money (see below), and the script says so.

## Sets: decks, websites, anything needing more than one image

The hard part of a multi-image job is not cost, it is **consistency**. Seeds do
not work (above), so the same prompt style twice gives two unrelated looks. Ten
images for one deck will read as ten different stock libraries unless anchored.

**`--style` is the main lever.** It appends one shared wording anchor — lighting,
palette, rendering, composition tendency — to every prompt in the run. Verified
on a 3-prompt batch with `--style tech`: subjects were entirely different (server
racks, an engineer at monitors, an abstract topology) yet all three came back on
dark charcoal with the same cyan rim-light and contrast. Good enough to sit on
consecutive slides.

```bash
# prompts.txt — one per line, # comments and blank lines ignored
gen.py --batch prompts.txt --style tech --aspect 16:9 --resolution 4K
```

Batch runs print an estimate and ask before spending, number the files `01-`,
`02-`, … in input order so they map to slides, keep going if one prompt fails,
and report the real total at the end.

**`--anchor` is the stronger, riskier option.** It passes image 1 back as a
reference for every later prompt. Consistency is tighter, but `--ref` carries
*composition* too, so a set of unrelated subjects tends to collapse into variants
of the first image. Reach for `--style` first; add `--anchor` only when a set
still looks disjointed.

Recommended order — preview the whole set cheaply, then commit:

```bash
gen.py --batch prompts.txt --style tech --aspect 16:9 --draft        # ~USD 0.015 each
gen.py --batch prompts.txt --style tech --aspect 16:9 --resolution 4K # ~USD 0.040 each
```

For a deck, hand the numbered output straight to python-pptx; for a site, point
`-o` at the project's asset directory.

### Making illustrations sit on a tinted background

Illustration-style output arrives on a **pure white** canvas. Dropped onto any
tinted slide or page background it reads as a white sheet taped on, with a hard
rectangular seam. Repaint the background before placing:

```python
from PIL import Image, ImageDraw
CREAM, THRESH = (250, 247, 240), 24
im = Image.open(src).convert("RGB")
w, h = im.size
for corner in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    if min(im.getpixel(corner)) > 225:   # skip full-bleed art
        ImageDraw.floodfill(im, corner, CREAM, thresh=THRESH)
```

Seed from the corners, not a global colour swap — that preserves whites *inside*
the artwork (a blank canvas, a page, a highlight).

**`thresh` must stay below the distance between the fill colour and the original.**
`ImageDraw.floodfill` opens with:

```python
if _color_diff(value, background) <= thresh:
    return   # treats the seed as already filled
```

`_color_diff` is the **sum** of channel deltas. White to cream is 5+8+15 = 28, so
`thresh=28` makes the call a silent no-op — no error, no warning, unchanged image.
24 works. Always verify by sampling a pixel afterwards rather than trusting the call.

## Gotcha: pricing is flat per image, not per pixel

Seedream 4.5 bills **USD 0.04 per image regardless of resolution** — a 2560×1440
and a 4096×2304 cost exactly the same (measured). The `image_token` price in
`/api/v1/models` does not predict actual cost, and the `completion_tokens` in
the response does not reconcile with it either. **Never reason about cost from
the pricing metadata — read the `cost` field the script prints.**

Consequence: with Seedream there is no reason to render small. Always use `4K`.

## Gotcha: tiers can silently drop your aspect ratio

`resolution` accepts only the four tiers; explicit pixels must go in a separate
`size` field (the script routes this automatically). Tiers get normalized
per-provider, and FLUX then **ignores `aspect_ratio` and returns a square**.
When the aspect ratio matters, pass explicit pixels rather than a tier.

## Gotcha: Seedream has a *minimum* size

Seedream 4.5 rejects anything under **3,686,400 pixels** (2560×1440) with:

```
HTTP 400 ... image size must be at least 3686400 pixels
```

`--resolution 2K` at a wide aspect is only ~2.36M px and **fails**. Use
`--resolution 4K` with Seedream unless the aspect is near-square. Other models
(Gemini, FLUX, GPT-Image) have no such floor. A 400 costs nothing, so a failed
call is safe to retry with a larger size.

## Models

`bytedance-seed/seedream-4.5` is the default: strong at photorealism, Chinese
text rendering, and edit consistency (preserves subject details across edits).

Swap with `-m` when the job calls for it:

| Model | Good for |
|---|---|
| `bytedance-seed/seedream-4.5` | default — photoreal, Chinese text, faithful edits |
| `google/gemini-3-pro-image` | Nano Banana Pro — strongest prompt adherence, complex scenes |
| `google/gemini-2.5-flash-image` | cheapest quick drafts |
| `black-forest-labs/flux.2-pro` | artistic / stylized illustration |
| `openai/gpt-image-2` | clean graphic design, reliable English text in-image |
| `recraft/recraft-v4.1-vector` | true **SVG vector** output (logos, icons) |

Full current list:

```bash
curl -s "https://openrouter.ai/api/v1/models?output_modalities=image" | python3 -c "import json,sys; [print(m['id']) for m in json.load(sys.stdin)['data']]"
```

Note: these models are **not** in the default `/api/v1/models` response — the
`?output_modalities=image` filter is required to see them.

## After generating

Always `Read` the saved file so the image renders for the user and you can
verify it actually matches the request. If it missed, adjust the prompt and
retry rather than reporting success.

## Cost

Roughly **USD 0.04 per image** on Seedream 4.5; the script prints the exact charged
cost per run. For multi-image explorations, say the expected cost first. Don't
loop generations unattended.
