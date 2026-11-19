# 媒介 × 命令 × 判据

所有阈值基于本机实测（macOS, arm64）。命令可直接复制。

## 环境前提（本机已具备，均已实测）

| 组件 | 位置 / 版本 | 备注 |
|---|---|---|
| `scrapling` | `~/.local/bin/scrapling`（uv tool，v0.5） | 用 `uv tool upgrade scrapling` 升级，别 pip |
| `yt-dlp` | `/opt/homebrew/bin/yt-dlp` | 通用视频/音频下载 |
| `ffmpeg` / `ffprobe` | `/opt/homebrew/bin/` | 抽音频、抽帧、拼联系表 |
| `pandoc` | `/opt/homebrew/bin/pandoc` | epub/docx/html 互转 |
| `pdftotext` / `pdfinfo` / `pdftoppm` | Homebrew `poppler` | PDF 文本层与页面渲染 |
| `tesseract` | 5.5.4 + `tesseract-lang` | 已含 `chi_sim` / `chi_tra` |
| `pypdf` / `trafilatura` | 系统 python3 | PDF 结构读取、网页正文抽取 |
| **ASR 环境（长期复用）** | `~/.local/share/asr/venv` | `mlx-whisper`；模型走**默认缓存** `~/.cache/huggingface`（已有 `whisper-large-v3-turbo`，1.5GB） |

> ⚠️ **不要设置 `HF_HOME`**。默认缓存里已有可用模型；覆盖 `HF_HOME` 会让它去重新下载，
> 而 HF 主站在本机被 SSL 阻断（`SSL_ERROR_SYSCALL`），只有 `hf-mirror.com` 可通。

### ASR 已装好，直接复用

```bash
# 实测：6 分 17 秒视频，26 秒转完，完全离线
HF_HUB_OFFLINE=1 ~/.local/share/asr/venv/bin/mlx_whisper audio.m4a \
  --model mlx-community/whisper-large-v3-turbo \
  --language zh --output-dir . --output-format srt
```

- `HF_HUB_OFFLINE=1` 强制只读本地缓存——缓存存在时**避免任何联网**，也就避开了 SSL 失败。
- `large-v3-turbo` 质量优于 `small`，速度接近；**优先用它**。
- 若换机器需要重建环境：
  ```bash
  uv venv ~/.local/share/asr/venv --python /opt/homebrew/bin/python3
  uv pip install --python ~/.local/share/asr/venv/bin/python mlx-whisper
  ```
  然后首次运行会下载模型；下载失败时设 `export HF_ENDPOINT=https://hf-mirror.com` 重试。
- 非 Apple Silicon：改用 `faster-whisper`（CPU / `ct2` 后端）。

## 逐媒介命令

### 网页

```bash
# 快路径
web_fetch / read_page（工具）

# 需要选区或批量
scrapling extract get "URL" out.md --ai-targeted
scrapling extract get "URL" out.md -s "article.main" --ai-targeted
scrapling extract get "URL" out.md --impersonate chrome -H "Accept-Language: zh-CN"
```

判据：`Fetched (200)` + 字节数 > 1KB + 含目标关键词。`-s` 返回 0 字节 = 选择器没匹配。

### 反爬 / Cloudflare

```bash
scrapling extract fetch "URL" out.md --solve-cloudflare --network-idle --timeout 120000 --ai-targeted
```

- `--solve-cloudflare` 是**必须显式加**的开关，只开隐身不解盾。
- 普通挑战约 34s，交互式 Turnstile 实测约 118s → 默认 30s 超时不够。
- 判断是否真过盾：对照跑一次 `get`（预期 403 + 0 字节）。

### 视频

```bash
# 1) 平台支持
yt-dlp -f "bv*+ba/b" -o "v.%(ext)s" "URL"
yt-dlp -f bestaudio -x --audio-format m4a -o "a.%(ext)s" "URL"

# 2) 平台不支持（如小红书）→ 从页面 og 元信息取直链
scrapling extract fetch "URL" page.html --network-idle --timeout 90000
grep -oE '<meta[^>]*og:(video|title|description)[^>]*>' page.html
curl -sS -L --max-time 180 -A "Mozilla/5.0 …" -e "https://<site>/" -o v.mp4 "<直链>"

# 3) 转写 + 抽帧 + 交叉校正
ffprobe -v error -show_entries format=duration:stream=codec_type -of default=nw=1 v.mp4
ffmpeg -v error -ss 30 -i v.mp4 -frames:v 1 -q:v 2 f_030.jpg
```

判据：`file v.mp4` 显示 ISO Media；`ffprobe` 有 `codec_type=audio`；SRT 段数 / 时长 ≈ 0.5–1 段/秒。

### 音频 / 播客

```bash
yt-dlp -x --audio-format m4a -o "a.%(ext)s" "URL"
# 然后同上 ASR；无画面，术语错误无法交叉校正，需人工抽检
```

### PDF

```bash
pdfinfo in.pdf | head            # 页数、是否加密
pdftotext -layout in.pdf out.txt # 文本层
wc -c < out.txt                  # 字符数 / 页数 < 100 ≈ 扫描件
```

### OCR（实测可用参数，照抄）

**直接 `tesseract img.png -l chi_sim` 在 PPT/截图上经常输出空**。实测有效的组合是
**放大 2 倍 + 灰度 + `--psm 3`**：

```bash
# 图片已就绪时
ffmpeg -v error -i in.png -vf "scale=iw*2:-1,format=gray" -q:v 1 ocr_in.png -y
tesseract ocr_in.png stdout -l chi_sim+eng --psm 3

# 扫描版 PDF
pdftoppm -r 200 -png in.pdf page
# 再对每页做上面的放大+灰度+psm 3
```

实测效果（PPT 页）：能稳定识别出「01 把资料与经验提炼成 Skill」「别把临时发挥，当作原文方法」等标题级文字。
`--psm 6` 也可用，但行分割更差；`--psm 3` 优先。

### EPUB

```bash
pandoc -f epub -t gfm in.epub -o out.md
# 结构丢失时
unzip -o in.epub -d epub_src && pandoc -f html -t gfm epub_src/*.xhtml -o out.md
```

### DOCX / PPTX

用 `office` 技能（保留标题层级、表格、批注），比 pandoc 更稳。

### 图片

- 少图：`read_image`（多模态直接认字、识图表）。
- 批量中文：上面的 OCR 组合。

### 本地已有材料

先 `glob` / `grep` 找你自己的笔记库与下载目录 —— **先复用，再抓取**。

## 上下文预算

| 材料 | 粗略 token | 处理建议 |
|---|---|---|
| 公众号文章 | 1–3k | 直接进下游 |
| 6 分钟视频转写 | 1.5–2k | 直接进下游 |
| 1 小时播客 | 12–15k | 先分段，按目标句截取 |
| 300 页书 | 150k+ | **禁止整本**；先选章 |
| 扫描版整本 | 更大 | 只 OCR 目标章节 |

超过 20k token 的材料，先按目标句圈定范围，再交给下游。
