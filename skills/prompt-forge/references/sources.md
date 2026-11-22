# 来源与置信度（Sources & Confidence）

**什么时候读这个文件**：想知道某个结论到底靠不靠谱；交付时要标出处；或者怀疑"这条说法是不是网上抄来的"。
**读完你会得到什么**：三组来源（用户学习笔记 / 厂商官方文档 / 研究证据）的清单、每条的置信度标签、一条引用纪律，以及本目录所有文件共用的核对日期。

> **核对日期：2026-11。** 厂商建议变化很快，本目录里的版本门槛、参数行为、废弃情况**使用前建议复核**——尤其是 models.md 里"哪个版本开始报错/忽略参数"这类论断。
> **置信度三级**：**已核** = 链接可打开，且我直接读到了原文对应段落；**摘要** = 链接可打开 / 来源存在，但结论来自二手转述或我的摘要，未逐字核对原文；**未验证** = 只有笔记里的一句话，找不到可靠出处，只能当经验规则。

## 1. 用户学习笔记（个人学习整理，非官方）

这一组是用户自己收集/整理的资料，**不是权威来源**。可以用于提炼判断规则与提问方式，但**不要用来支撑具体数字、模型行为或因果结论**。

| # | 来源 | 提供什么 | 置信度 |
|---|---|---|---|
| 1 | 孔老師 AI 研習社《2026 最新提示工程指南》（Gemini 3.0 / ChatGPT 5.1 主题）Gem 指令原文 | TCREI 五段模板（任务主题 / 上下文 / 具体信息 / 目标 / 格式要求）+ "可加示例"的位置感；本目录多处骨架的母本 | 已核（原文在手） |
| 2 | 李厂长《15 分钟学会提示词 9 大秘籍》学习笔记 | 背景信息 > 技巧；框架是脚手架不产生信息；乔哈里视窗四象限决定喂多少信息；推理模型不指定思考步骤；创造性任务用"乒乓球"迭代；例子是另一种背景信息（2–3 个）；单次用 vs 反复用；指令过多要拆 | 摘要（视频内容经人转述成笔记） |
| 3 | Axton《重构个体》第 5 章"提示词工程：人机对话艺术" | RCARE / RICE 要素；引用锚定（`【文件名\|页码】`）；反思校对先自评可信度；Token 优化对比（243 → 93 tokens，省约 62%）；分步引导三轮；自动化场景的参数化提示词 | 摘要（书摘整理） |
| 4 | 《通用附加指令清单》（本地笔记，7 条附加条款） | 澄清模糊点、时效信源、多顾问视角、双语术语、任务类型判定、多模态、准确性核查 | 未验证（经验规则，无外部出处） |
| 5 | 提示词杂记中的"Claude 五招"（`/ghost`、`/artifacts`、OODA、`L99`、`/god mode`） | 只能作为**反模式素材**：其中 `/ghost`、`L99`、`/god mode` 并非官方指令，笔记作者本人已自我辟谣，效果等同直接描述语气/深度 | 未验证（已标注为民间叫法） |
| 6 | 笔记里转述的 OpenAI 面向用户的提示词建议（outline task / 给上下文 / 描述理想输出 / 拆任务 / 具体但简单 / 要选项 / 控语气格式） | 用户向写法的通俗版本，与官方文档方向一致 | 摘要 |
| 7 | Felix Rieseberg（Anthropic，Claude 工程负责人）*How to be more ambitious: A tutorial for humans with models*，2026-10-13，https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models | 速度／高度／深度／范围四维度；三步升级；深度五技巧与元提示词；名词换动词（引自 Kelley & Littman《创新的艺术》）；借方法不扮角色；外部裁判 | 摘要（作者原文，经联网读取的中文转述，非逐字） |
| 8 | 二次创作短视频《Claude 主管的 AI 用法：4 大维度》（TikTok @qi.zhang978），用户转录稿 | 深度元提示词的中文版本；把名词换动词归在「高度」下（与原文归类不同） | 摘要（二手转述） |
| 9 | Boris Cherny（Anthropic，Claude Code 作者）*Mastering Claude Code in 30 minutes* 演讲，用户转录稿（中英对照，ASR 校正） | 先计划后写码；说目标不指定工具；可运行反馈 + 迭代；三种工作流；CLAUDE.md 宜短、分层加载、反复纠正固化；`claude -p` 管道 | 摘要（一手演讲转录，integrity 降级见转录稿） |

引用纪律：写「孔老師 AI 研習社」「李厂长《15 分钟学会提示词 9 大秘籍》」「Axton《重构个体》第 5 章」即可；**不要写成"某研究表明"**。没有出处的经验性内容一律标「经验规则（非实测）」。

## 2. 厂商官方文档（8–12 条，2026-11 全部实测可打开）

| # | 文档 | 用来支撑什么 | 置信度 |
|---|---|---|---|
| 1 | OpenAI：Prompt engineering — https://developers.openai.com/api/docs/guides/prompt-engineering | 分区（Markdown/XML）、指令具体化、示例与输出的基本写法 | 已核（标题与主题） |
| 2 | OpenAI：Reasoning models — https://developers.openai.com/api/docs/guides/reasoning | 推理模型不要手写 CoT、reasoning effort 档位、推理模式下移除采样参数 | 摘要 |
| 3 | OpenAI：Structured model outputs — https://developers.openai.com/api/docs/guides/structured-outputs | 格式靠 schema 而不是靠措辞 | 摘要 |
| 4 | OpenAI Cookbook：GPT-5.1 Prompting Guide — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide | `verbosity` 参数控制长度；effort 含 none 档；"具体长度指令效果好" | 已核（原文段落） |
| 5 | Anthropic：Prompt engineering overview — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | XML 分区、`<example>`、示例要典型多样、`think thoroughly` 优于手写步骤 | 摘要 |
| 6 | Anthropic：Extended thinking — https://platform.claude.com/docs/en/build-with-claude/extended-thinking | 内建思考与预算控制；对外只暴露推理摘要 | 摘要 |
| 7 | Anthropic：Structured outputs — https://platform.claude.com/docs/en/build-with-claude/structured-outputs | 格式保证的正确通道 | 摘要 |
| 8 | Anthropic Engineering：Effective context engineering for AI agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 最小高信号 token 集合、长任务的上下文管理 | 已核（标题与主题） |
| 9 | Anthropic Engineering：Building effective agents — https://www.anthropic.com/engineering/building-effective-agents | 何时拆成多步/多代理，而不是一条巨型提示词 | 已核（标题与主题） |
| 10 | Google：Prompt design strategies — https://ai.google.dev/gemini-api/docs/prompting-strategies | 明确建议"总是给 few-shot 示例"；示例格式需一致；仍推荐 response prefix | 已核（原文段落） |
| 11 | Google：Structured outputs — https://ai.google.dev/gemini-api/docs/structured-output | Gemini 侧格式保证通道 | 摘要 |
| 12 | Microsoft Learn：Azure OpenAI reasoning models — https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reasoning | 推理摘要（reasoning summary）是唯一受支持的过程可见形式；以其他方式提取推理可能违反可接受使用政策 | 摘要 |

补注：Claude 侧 prefill 的独立文档页在核对时已重定向到 prompt engineering 概览，且正文不再提及 prefill——这与"4.6+ 起废除 prefill"的结论一致；但**版本门槛本身仍属摘要**，上线前请用一次最小请求实测。

## 3. 研究证据（6–8 条，一句话结论）

| # | 论文 | 一句话结论 | 置信度 |
|---|---|---|---|
| 1 | Lost in the Middle (2023) — https://arxiv.org/abs/2307.03172 | 长上下文里"中间位置"的信息最容易被忽略：窗口大 ≠ 召回好 | 已核（标题）/ 摘要（结论） |
| 2 | When "A Helpful Assistant" Is Not Really Helpful: Personas in System Prompts… (2023) — https://arxiv.org/abs/2311.10054 | 角色人设不提升客观任务表现，部分任务上更差；persona 只适合定语气与边界 | 摘要 |
| 3 | Quantifying LMs' Sensitivity to Spurious Features in Prompt Design (2023) — https://arxiv.org/abs/2310.11324 | 提示词格式（分隔符、空格、示例排布）能造成巨大分数波动，跨模型不一致 | 摘要 |
| 4 | Premise Order Matters in Reasoning with LLMs (2024) — https://arxiv.org/abs/2402.08939 | 前提/示例的顺序会改变推理结论，所以顺序要显式声明 | 摘要 |
| 5 | Chain-of-Thought Prompting Elicits Reasoning in LLMs (2022) — https://arxiv.org/abs/2201.11903 | CoT 的原始价值在**非推理模型**上；对内置思考的模型不再适用 | 摘要 |
| 6 | Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs (2024) — https://arxiv.org/abs/2412.21187 | 推理模型会过度思考，硬加推理步骤会放大这个问题 | 摘要 |
| 7 | Reasoning Models Don't Always Say What They Think (2025) — https://arxiv.org/abs/2505.05410 | 模型说出来的推理不等于真实推理过程，不能当审计证据 | 摘要 |
| 8 | Not what you've signed up for: Indirect Prompt Injection (2023) — https://arxiv.org/abs/2302.12173 | 外部文档/网页里的指令会被当作任务执行：必须有注入边界 | 摘要 |

（"context rot" 现象在业界通称下常与上述 1 一起引用；本目录不单列链接，只作为"窗口大 ≠ 够用"的支持证据。）

## 4. 引用示例（交付物里怎么写）

一段合格的来源标注长这样，照抄结构即可：

```
> 依据：① 厂商文档（Anthropic《Prompt engineering overview》，2026-11 核对）——XML 分区与示例写法；
> ② 论文 Lost in the Middle（arXiv 2307.03172）——长上下文中段信息易被忽略；
> ③ 经验规则（李厂长《15 分钟学会提示词 9 大秘籍》，非实测）——任务多要拆。
> 置信度：①已核 ②摘要 ③未验证。厂商建议变化快，落地前建议复核。
```

注意三点：厂商文档写"文档名 + 核对日期"，论文写标题 + arXiv 编号，笔记写"人名 + 课程名 + 非实测"。

## 5. 常见坑

- 不要把用户学习笔记当权威：它可以解释"为什么这么问"，不能证明"模型一定这样"。
- 不要引"某研究表明""据统计"这类无出处说法；有论文就给 arXiv 链接，没有就标「经验规则（非实测）」。
- 不要给 2026-11 之后的版本行为下断言；`models.md` 里的版本门槛统一默认"摘要，需实测"。
- 不要只信标题：论文标题能确认存在，**具体数字（如 ±23%、71.6 → 66.3）仍需按摘要口径使用**，别写成精确实测。
- 不要把"官方文档说过"当永久事实：文档会改，改了就只更新本文件第 2 组，其它文件沿用"以官方文档为准"的表述。
