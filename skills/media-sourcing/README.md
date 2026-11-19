# media-sourcing（取料）

把任意来源转成**可复核的文本材料**，并给出质量判据。
它不总结、不蒸馏——只负责"把料取干净"，下游交给 `distill-to-skill` 或 `video-learning-handbook`。

## 为什么需要它

取料最常见的失败不是"抓不到"，而是**"看起来抓到了"**：
小红书返回 200 + 32KB，内容全是登录弹窗和页脚；
`scrapling` 被 Cloudflare 挡掉时照样打印 "Content successfully saved"、退出码 0；
ASR 转写流畅但把「蒸馏」听成「征流」——直接喂给下游，就会蒸馏出一套带错别字的规则。

这个 skill 用三件事防住：

1. **三查**：HTTP 状态 / 输出体积 / 内容特征，缺一不算成功。
2. **integrity 分级**：`pass` / `degraded` / `fail`，降级必须写明缺什么。
3. **强制交叉校正**：视频转写必须用画面（PPT、字幕、标题）校正术语。

## 覆盖的来源

网页、公众号、反爬站、需登录站、视频、音频/播客、PDF（文本层与扫描件）、EPUB、DOCX/PPTX、图片、本地笔记。

## 安装

```bash
cp -R media-sourcing ~/.agents/skills/
```

## 用法

```
把这个链接的正文取下来，别总结，给我原文和出处。
```

```
这个视频转成带时间戳的文字，并把 PPT 上的术语一起校一遍。
```

```
这份 PDF 是扫描版，帮我把第 3 章 OCR 出来，标注页码。
```

## 依赖（本机已配）

| 能力 | 工具 |
|---|---|
| 网页抓取 / 过盾 | `scrapling`（skill 已有，不改） |
| 视频下载 | `yt-dlp` |
| 抽音频 / 抽帧 | `ffmpeg` / `ffprobe` |
| PDF 文本层 | `pdftotext`（poppler） |
| OCR | `tesseract` 5.5.4 + `chi_sim`/`chi_tra` 语言包 |
| EPUB / DOCX 转换 | `pandoc` / `office` 技能 |
| ASR | `~/.local/share/asr/venv`（mlx-whisper + `large-v3-turbo` 缓存，实测 26s/6min，离线可用） |

## 与相邻 skill 的边界

| skill | 负责 |
|---|---|
| `media-sourcing` | 拿到可信材料 + 质量判据 |
| `video-learning-handbook` | 材料 → 学习手册（复习卡、自测题、爆款拆解） |
| `distill-to-skill` | 材料 → 可执行 skill（判断规则、验收） |
| `scrapling` | 网页抓取的具体命令与坑（本 skill 只做路由） |

四者是**串联**关系，不合并：合并会让每个 skill 的触发词互相干扰。
