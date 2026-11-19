# 取料记录模板

复制这份模板作为交付物的头部。缺项不要留空，写「未获取」并说明原因。

```markdown
# 取料记录

- **source**: <URL 或绝对路径>
- **type**: 网页 / 视频 / 音频 / PDF / EPUB / DOCX / 图片 / 本地笔记
- **fetched_at**: <YYYY-MM-DD HH:MM>
- **method**: <工具 + 关键参数，例：scrapling extract fetch --solve-cloudflare --network-idle>
- **integrity**: pass / degraded / fail
- **coverage**: <全文 / 第 1–3 章 / 00:00–06:17 / 第 1–20 页>
- **defects**: <同音错字 / 登录墙 / 漏页 / 画外信息 / 导航噪音 / 无>

## 交叉校验

| 检查项 | 结果 | 说明 |
|---|---|---|
| HTTP 状态 | 200 | |
| 输出体积 | 32 KB | |
| 内容特征 | 命中 | 含关键词「<目标词>」 |
| 二次核对 | 通过 | 抽样 3 处与画面/原文一致 |

## 交付

- 正文文件：`<path>`
- 时间戳/页码：<有 / 无>
- 已知缺口对下游的影响：<例：03:17 之后画面切换快，可能漏一页 PPT>

## 下一步建议

- 做成 skill → distill-to-skill
- 做成学习手册 → video-learning-handbook
- 写报告 → research
```

## 示例（本次小红书视频的真实记录）

```markdown
- source: https://www.xiaohongshu.com/explore/6ae332fe000000003500b7bf
- type: 视频（PPT 讲解 + 口播）
- fetched_at: 2026-11-19 04:36
- method: scrapling fetch（读 og 元信息取视频直链）→ curl 下载 → mlx_whisper small 转写 → ffmpeg 抽 19 帧
- integrity: degraded
- coverage: 00:00–06:17（全文口播）；画面 19 个采样点，非逐帧
- defects: 登录墙无法取正文（改走 og 元信息）；ASR 同音错字约 15 处，已用 PPT 画面校正；画面为抽样，短暂页可能遗漏
```
