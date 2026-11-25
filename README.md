# AIggySkills

个人 Claude Skills 收藏仓库。

## 目录

- [skills/de-ai-flavor](skills/de-ai-flavor/SKILL.md) —— 中文写作降AI味：句子结构、AI套话黑名单、叙事结构三层诊断与修改方法
- [skills/distill-to-skill](skills/distill-to-skill/SKILL.md) —— 蒸馏成技能：把书/资料/视频或自己的经验，转成可加载、可验收的 Skill（目标句 → 标源 → 三类分流 → 双案例验证 → 落盘）
- [skills/image-gen](skills/image-gen/SKILL.md) —— 生图：经 OpenRouter 调用真实图片模型（默认 Seedream 4.5，另有 Nano Banana / GPT-Image / FLUX / Recraft）出图与改图；`--draft` 低价预览、`--ref` 锁构图、`--batch` + `--style` 成套配图
- [skills/media-sourcing](skills/media-sourcing/SKILL.md) —— 取料：把网页/视频/音频/PDF/扫描件/图片转成可复核文本，带 integrity 分级与 9 类故障判定（不总结、不蒸馏）
- [skills/prompt-forge](skills/prompt-forge/SKILL.md) —— 提示词生成器：严格采访 → 选模板 → 组装 → 自检 → 交付六件套；含雄心四维度（速度/高度/深度/范围）与名词换动词判定规则、Claude Code 编程与 `claude -p` 写法

## 文档

- [docs/取料加工资产-操作说明.md](docs/取料加工资产-操作说明.md) —— 全链路 SOP：取料 → 结构 → 观点 → 岔路 → 提炼 → 资产；含每级工具映射、可复制指令、回退表与速查卡

## 技能链

```
media-sourcing（取料 + 质量分级）
   ├→ video-learning-handbook（产出学习手册）
   └→ distill-to-skill（产出可执行 skill）
```

取料与加工分离：前者保证材料可信，后者保证产出可用。

## 分级工具映射

| 级 | 谁来做 |
|---|---|
| L0 取料 | `media-sourcing`（+ `smart-search` / `ego` / `web_fetch`） |
| L1 结构 | **和 AI 对话**，无 skill |
| L2 观点 | **和 AI 对话**，无 skill |
| L3 提炼 | `distill-to-skill` |
| L4 资产 | 按出口：`distill-to-skill` / `video-learning-handbook` / `deep-research-explainer` / `infographic-builder` / `office-docx` |

## 内容加工纪律

本仓库（与 `docs/` 的 SOP、各 skill 内的交接说明）统一遵循：

- **加工分三级，不许跳**：L1 只切结构不评价 → L2 每条结论带出处并标 `[明确]`/`[推断]` → L3 用 `distill-to-skill` 落盘。
- **取料 → 提炼的分工**：`media-sourcing` 拿可信材料并交接 `integrity`/`defects`；`distill-to-skill` 产出可执行规则；中间 L1/L2 用对话完成，**不建 skill**（同一模板用过 ≥3 次且反复出错，才考虑合并成一个 `note-structuring`）。
- **出口按用途选**：能验收→skill，能理解→手册，要传播→图文。

## 安装

```bash
cp -R skills/<name> ~/.agents/skills/
```

## 依赖（image-gen 需要）

`python3`，以及自己的 OpenRouter 密钥：放在环境变量 `OPENROUTER_API_KEY`（Claude Code 读 `~/.zshenv`，不是 `~/.zshrc`）。仓库里不含任何密钥。按张计费，Seedream 约 USD 0.04/张，`--draft` 约 USD 0.015/张。

## 依赖（media-sourcing 需要）

`scrapling` / `yt-dlp` / `ffmpeg` / `pandoc` / `poppler` / `tesseract`+`chi_sim` / `mlx-whisper`。
详见 [skills/media-sourcing/references/media-matrix.md](skills/media-sourcing/references/media-matrix.md)。
