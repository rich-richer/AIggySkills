# image-gen（生图）

经 OpenRouter 调用真实图片模型，**出图与改图**：照片、插画、角色、场景、产品图、Logo、纹理。
默认用 Seedream 4.5，按需换成 Nano Banana / GPT-Image / FLUX / Recraft。
它不画流程图、架构图、数据图表或 UI 草图——那些手写 SVG/HTML，不花 API 费用。

## 为什么需要它

Claude 自己不能产出位图，只能借外部模型出图。真正的难处不是"调得通"，而是**"调通了也白花钱"**：
Seedream 4.5 的 `--seed` 被静默忽略，同一个 seed 跑两次是两张完全不同的图；
`--resolution 2K` 配宽比例会被 Seedream 以 HTTP 400 拒绝（下限 2560×1440 像素）；
FLUX 拿到分辨率档位后会丢掉 `aspect_ratio`，悄悄返回正方形；
一套十张的配图，若不加锚定，会像来自十个不同的图库。

这个 skill 用三件事防住：

1. **`--draft` 先预览**：换成 FLUX 小模型约 1MP，约 USD 0.015、7 秒，先定方向再出正式图（Seedream 约 USD 0.04、23 秒）。
2. **`--ref` 锁构图**：seed 不可靠，把满意的图当参考图回喂，主体位置、光线方向会跟着走。
3. **`--style` 统一成套风格**：给每条提示词追加同一段风格锚点（business / tech / illustration / warm / minimal），整套图色调、光线一致。

## 能做的事

文生图、图生图（改图、换风格、扩图）、批量配图（PPT、网页主视觉与卡片图、社交素材）、矢量 SVG（Recraft）。
批量时先报预估费用再执行，文件按 `01-`、`02-` 编号对应页序，单条失败不影响其余，最后报实际总花费。

## 安装

```bash
cp -R image-gen ~/.claude/skills/
```

然后自己把 OpenRouter 密钥写进 `~/.zshenv`（**不是** `~/.zshrc`：Claude Code 的命令在非交互 shell 里跑，只读 `.zshenv`）。在终端执行，贴上时不显示、也不留在历史记录：

```bash
read -s "k?贴上 OpenRouter 密钥后按 Enter: " && echo "export OPENROUTER_API_KEY='$k'" >> ~/.zshenv && unset k && chmod 600 ~/.zshenv
```

不要把密钥贴进对话，也不要写进 skill 的任何文件。

## 用法

```
先用草稿模式画一张橘猫坐在窗台上看雨，水彩风格。
```

```
就用刚才那张草稿当参考，出 4K 正式版。
```

```
给这份 PPT 的 8 页各配一张图，tech 风格，16:9，先出草稿给我看。
```

```
把这张照片改成水彩画。
```

## 依赖

| 能力 | 工具 |
|---|---|
| 运行脚本 | `python3`（只用标准库；装了 `certifi` 就用它的证书，否则用系统证书） |
| 出图 | OpenRouter 账户与密钥（`OPENROUTER_API_KEY`），需要有余额 |
| 费用 | 按张计费：Seedream 约 USD 0.04/张（与分辨率无关，所以一律出 4K），`--draft` 约 USD 0.015/张；脚本每次打印实际扣费 |

## 适用范围

| 场景 | 是否可用 |
|---|---|
| Claude Code（终端与桌面版 Code） | ✅ 读得到 `~/.zshenv` 里的密钥 |
| Claude Chat / Cowork | ⚠️ 未验证：沙盒读不到本机 `~/.zshenv`，也可能连不上 `openrouter.ai` |

## 与相邻做法的边界

| 需求 | 用什么 |
|---|---|
| 照片、插画、角色、场景、产品图、纹理 | `image-gen` |
| 改图、换风格、扩图 | `image-gen`（`--ref`） |
| 流程图、架构图、数据图表、UI 草图 | 手写 SVG / HTML，不调用本 skill |
