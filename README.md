# AIggySkills

个人 Claude Skills 收藏仓库。

## 目录

- [skills/de-ai-flavor](skills/de-ai-flavor/SKILL.md) —— 中文写作降AI味：句子结构、AI套话黑名单、叙事结构三层诊断与修改方法
- [skills/distill-to-skill](skills/distill-to-skill/SKILL.md) —— 蒸馏成技能：把书/资料/视频或自己的经验，转成可加载、可验收的 Skill（目标句 → 标源 → 三类分流 → 双案例验证 → 落盘）
- [skills/media-sourcing](skills/media-sourcing/SKILL.md) —— 取料：把网页/视频/音频/PDF/扫描件/图片转成可复核文本，带 integrity 分级与 9 类故障判定（不总结、不蒸馏）

## 技能链

```
media-sourcing（取料 + 质量分级）
   ├→ video-learning-handbook（产出学习手册）
   └→ distill-to-skill（产出可执行 skill）
```

取料与加工分离：前者保证材料可信，后者保证产出可用。

## 安装

```bash
cp -R skills/<name> ~/.agents/skills/
```

## 依赖（media-sourcing 需要）

`scrapling` / `yt-dlp` / `ffmpeg` / `pandoc` / `poppler` / `tesseract`+`chi_sim` / `mlx-whisper`。
详见 [skills/media-sourcing/references/media-matrix.md](skills/media-sourcing/references/media-matrix.md)。
