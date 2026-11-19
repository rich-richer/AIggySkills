---
name: media-sourcing
description: >-
  把任意来源转成可复核的文本材料：网页/文章、视频、音频、PDF/EPUB/DOCX、扫描件、图片、本地文件。
  当用户说「抓这个链接」「把这个视频/这本书/这篇公众号转成文字」「提取字幕」「读一下这份 PDF」
  「取料」时使用。它只负责取料与质量校验，不负责总结或蒸馏——下游交给 distill-to-skill
  或 video-learning-handbook。
  Triggers: 取料, 转成文字, 提取字幕, 抓正文, 读PDF, read this PDF, extract transcript, sourcing.
---

# 取料（media-sourcing）

取料的目标**不是"拿到一堆字"，而是拿到可复核、可定位、可追溯的材料**。
没有校验的取料 = 把垃圾喂给下游。

## 三条边界

1. **不总结、不蒸馏。** 摘要是下游的事。这里只交原文/转写 + 元信息。
2. **不臆测缺失内容。** 抓不到就说抓不到，列出缺什么，不要用"大概是……"补齐。
3. **不绕过访问控制。** 登录墙、付费墙、验证码一律交给人处理；不挖 cookie、不猜密码、不爆破。

## 输出契约（每次取料都要给）

```markdown
- source: <URL 或文件路径>
- type: 网页 / 视频 / 音频 / PDF / EPUB / DOCX / 图片 / 本地笔记
- method: <工具 + 关键参数>
- integrity: pass / degraded / fail　（理由）
- coverage: <全文 / 第 1–3 章 / 时间 00:00–06:17 / 第 1–20 页>
- text: <正文或转写，带时间戳/页码>
- defects: <已知缺陷：同音错字、漏页、画外信息、导航噪音>
```

`integrity` 判定标准见 [references/failure-modes.md](references/failure-modes.md)。
**降级（degraded）必须写明降在哪**，否则下游会把它当全文用。

## 路由：先判媒介，再选工具

| 来源 | 首选 | 何时换 |
|---|---|---|
| 普通网页 / 公众号 | `web_fetch` / `read_page` | 要批量、要 CSS 选区、要过反爬 → `scrapling` |
| 反爬 / Cloudflare | `scrapling extract fetch … --solve-cloudflare` | 拖到交互式挑战就 `--timeout 120000` |
| 需登录的站（小红书、朋友圈、付费专栏） | `ego` 浏览器 + 请用户登录 | 绝不抓 cookie 复用 |
| 视频（公开平台） | `yt-dlp` 取音轨 + `ffmpeg` 抽帧 + ASR | 平台不支持 → 抓页面里的 `og:video` 直链 |
| 音频 / 播客 | `yt-dlp -x` → ASR | 无画面，无法交叉校术语 |
| PDF（有文本层） | `pdftotext -layout` | 抽出来是乱码/字符极少 → 当扫描件处理 |
| PDF（扫描件） | `pdftoppm` → `tesseract -l chi_sim` | 中文语言包缺失 → `read_image` 逐页 |
| EPUB | `pandoc -f epub -t gfm` | 结构丢失就转 html 再抽正文 |
| DOCX / PPTX | `office` 技能 | — |
| 图片 / 截图 | `read_image`（多模态直读） | 要批量 → `tesseract` |
| 你已有的 Obsidian 笔记 / 本地文件 | `read` 直接读 | 这是最省成本的一层，先检查 |

完整命令与判据见 [references/media-matrix.md](references/media-matrix.md)。

## 高频链路（按这四步走）

### A. 网页正文

```bash
scrapling extract get "URL" out.md --ai-targeted
wc -c < out.md
```

判据：日志出现 `Fetched (200)` **且** 字节数 > 1KB **且** 正文含目标关键词。
**退出码恒为 0，不能当成败依据。** 403 + 0 字节也算"成功保存"。

### B. 视频（有口播）

```bash
# 1) 取音频
yt-dlp -f bestaudio -x --audio-format m4a -o "video.%(ext)s" "URL"
# 2) 转写（长期复用环境，见 references/media-matrix.md）
#    实测：6 分 17 秒视频 26 秒转完，完全离线；不要设 HF_HOME
HF_HUB_OFFLINE=1 "$HOME/.local/share/asr/venv/bin/mlx_whisper" video.m4a \
  --model mlx-community/whisper-large-v3-turbo --language zh \
  --output-dir . --output-format srt
# 3) 抽关键帧做交叉校正
ffmpeg -v error -ss 10 -i video.mp4 -frames:v 1 -q:v 2 frame_010.jpg
```

**强制步骤：转写必须用画面交叉校正。** ASR 会稳定产出同音错字
（实测：蒸馏→征流、Skill→Skew、复用→附用、验收→键售），
纯转写文本不可直接交给下游。

### C. 需登录的站

1. 用 `ego` 打开页面，告诉用户「请在浏览器里登录，我等你」→ `ego_wait_for_human`。
2. 登录后读 DOM 或截全页，再用 `read_image` 取正文。
3. **不要**从浏览器导出 cookie 给 curl/scrapling 复用。

### D. PDF / 电子书

```bash
# 先判断有没有文本层
pdftotext -layout in.pdf out.txt && wc -c < out.txt
# 字符数 / 页数 < 100 ≈ 扫描件，转 OCR
pdftoppm -r 200 -png in.pdf page
# OCR 实测有效组合：放大 2 倍 + 灰度 + psm 3（直接跑常输出空）
ffmpeg -v error -i page-01.png -vf "scale=iw*2:-1,format=gray" -q:v 1 p1.png -y
tesseract p1.png stdout -l chi_sim+eng --psm 3
```

`chi_sim` 语言包已装（实测能识别 PPT 标题级文字）。若 OCR 输出为空，先按上面的
「放大 + 灰度 + `--psm 3`」调参，仍为空再改用 `read_image` 逐页读。

## 交接给下游

- 要**做成可复用 skill** → 交给 [distill-to-skill](../distill-to-skill/SKILL.md)，附 `integrity` 与 `defects`。
- 要**做成学习手册** → 交给 `video-learning-handbook`，附时间戳转写与关键帧。
- 要**写研究报告** → 交给 `research`，附 `coverage`（证明覆盖到哪）。

交接时**必须传递 `integrity` 与 `defects`**。下游最常见的事故，是把「登录墙返回的 32KB 页脚」
当成整篇文章去蒸馏。

**中间不要建 skill**：取料之后的结构（L1）与观点（L2）直接用对话完成——
「只切结构不评价」「每条结论带出处并标 [明确]/[推断]」两句就够了。
只有提炼（L3）需要 skill，那是 `distill-to-skill` 的事。

## 反模式

| 反模式 | 后果 |
|---|---|
| 只看退出码 0 | 把 403 当成功 |
| 不查字节数 | 把空文件当"页面没内容" |
| 转写不校画面 | 专有名词全错，下游蒸馏出错误规则 |
| 抓不到就"根据标题推测内容" | 编造原料 |
| 把登录墙页脚当正文 | 下游蒸馏出垃圾 skill |
| 一本书整本塞进去 | 超出上下文，被截断且不自知 |
