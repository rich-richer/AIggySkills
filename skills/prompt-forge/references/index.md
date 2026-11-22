# 总索引（Index）

**路由顺序**：用户原话 → ① 匹配「任务形态」选一个模式 → ② 匹配「行业」选一个领域 → ③ 按默认技法组合选 2–4 张卡 → 读对应文件组装。

匹配不到就兜底：`modes/creative.md`（创造类）或 `modes/research.md`（分析类），并告诉用户你选了哪个、为什么。

---

## ① 任务形态 → 模式（选 1 个）

| 用户会这样说 | 模式文件 | 一句话判据 |
|---|---|---|
| 写文案 / 起名 / 想标题 / 头脑风暴 / 写故事 / 写口播 | `modes/creative.md` | 答案不唯一，靠方向与品味 |
| 做调研 / 竞品分析 / 行业研究 / 查清楚某件事 | `modes/research.md` | 答案依赖外部事实与信源 |
| 写方案 / 可行性 / 汇报 / BP / 复盘 | `modes/report.md` | 要支撑一个决策或结论 |
| 提取字段 / 打标 / 转 JSON / 批量清洗 / 分类 | `modes/extraction.md` | 输出结构固定、可校验 |
| 解释概念 / 教我 / 出题 / 费曼 / 苏格拉底 | `modes/learning.md` | 目标是让人理解 |
| 怎么操作 / 排错 / 配置 / 装环境 | `modes/procedure.md` | 有确定的步骤与验证点 |
| 写代码 / 做 Agent / 调工具 / 多步自动化任务 | `modes/agentic.md` | 需要模型自己动手做多步 |
| 文生图 / 分镜 / 短视频脚本 / 海报 | `modes/image-video.md` | 目标是视觉产出 |
| 工作流节点 / Make / n8n / API 里的提示词 | `modes/automation.md` | 提示词是流水线零件，输出要被程序消费 |

**多义时怎么办**：取"用户最终要的那份东西"。
- "写个项目报告，先做点调研" → 主 `report`，副 `research`（把调研作为报告的第一阶段，串成提示词链）。
- "帮我把这些评论分类并总结" → 主 `extraction`，副 `research`（总结部分）。
- 一次只主导一个模式，其余作为该模式里的"子步骤"。

---

## ② 行业 → 领域（选 1 个，最多 2 个）

| 触发词 | 领域文件 | 关键补充 |
|---|---|---|
| 行业研究 / 市场 / 竞品 / 咨询 / 战略 | `domains/research-consulting.md` | 信源、市场规模、竞争格局、政策 |
| 方案 / 可行性 / 立项 / BP / 汇报 / 复盘 | `domains/project-report.md` | 决策者、成本、风险、结论倾向 |
| 自学 / 学习笔记 / 读书 / 考试 | `domains/self-learning.md` | 水平、目标、复习与自测 |
| 课程 / 讲师 / 学员 / 招生 / 教培 | `domains/education-training.md` | 学员画像、课时、合规宣传 |
| 短视频 / 公众号 / 小红书 / 抖音 / 涨粉 | `domains/media-content.md` | 平台、账号定位、钩子、转化 |
| 邮件 / 汇报 / 述职 / 跨部门 / 客户沟通 | `domains/workplace-communication.md` | 关系、台阶、结论先行 |
| 产品 / 需求 / PRD / 技术方案 / 评测 | `domains/tech-product.md` | 用户场景、技术栈、验收标准 |
| 投资 / 财报 / 估值 / 理财 | `domains/finance.md` | 读者专业度、免责声明、数据来源 |
| 健康 / 医疗 / 用药 / 康复 | `domains/health.md` | 科普 vs 个人建议、就医边界 |
| 合同 / 合规 / 劳动 / 条款 | `domains/legal.md` | 法域、"不构成法律意见" |
| 电商 / 详情页 / 直播 / 选品 / 投放 | `domains/ecommerce.md` | 平台、客单价、转化目标 |
| 论文 / 文献 / 综述 / 期刊 | `domains/academic.md` | 学科、引用格式、学术诚信 |
| 教育行业 / EdTech / 教育赛道值不值得进 | `domains/research-consulting.md`（**不是** education-training） | 行业判断用研究包；做课招生才用 education-training |
| 生活服务 / 旅行 / 装修 / 育儿 / 健身 | `domains/life-service.md` | 预算、时间、替代方案 |

**匹配不到行业**：不选领域文件，只用模式 + 技法；并在提示词里补两个缺口：① 受众未知 → 先问或在变量槽留 `{{受众}}`；② 术语未知 → 第一次出现给白话解释。

### 领域消歧（同句需求两个领域都像时，按这四条判）

1. **先看"研究对象是什么"，再看"给谁看"。** "给投资人看的 AI 教育行业调研"——研究对象是**教育行业**→ `research-consulting`；"投资人"只是**交付用途**，不等于 `finance`。只有研究内容本身是投资/财报/估值时才用 `finance`。
2. **"研究一个行业" ≠ "在这个行业里干活"。** `education-training` 是"做课/招生/教案"的操作包；问"教育行业值不值得进"属于研究，走 `research-consulting`，最多借 education-training 的政策合规那 2–3 条。
3. **一个领域为主，最多借第二个领域的一个小节。** 借的时候明说借了什么（如"只借教培的广告法红线"）。
4. **拿不准就问一句**，不要替用户选：`这个需求你更关心「行业判断」还是「具体怎么做」？`

---

## ③ 技法卡（2–4 张）

| 技法文件 | 什么时候必须加 |
|---|---|
| `techniques/johari.md` | 判断"该喂多少背景"——用户信息多但不知道给什么 |
| `techniques/pingpong-iteration.md` | 创造类任务，方向模糊，一次写不好 |
| `techniques/frameworks-13.md` | 用户明确要框架名，或需要一个填空脚手架 |
| `techniques/rcare.md` | 复杂多维任务，需要角色/上下文/目标/规则/示例五件套 |
| `techniques/citation-anchoring.md` | 调研、报告、任何基于资料写作、任何要求"别编" |
| `techniques/self-critique.md` | 高风险输出（对外发布、要决策、怕幻觉） |
| `techniques/decomposition.md` | 任务太大、一条提示词塞不下、或要反复执行的流程 |
| `techniques/five-advisors.md` | 用户要评审一个现成方案 |
| `techniques/addon-checklist.md` | 严肃场景（顾问级、要时效核查、要双语术语） |
| `techniques/token-economy.md` | 自动化节点、大批量、成本敏感 |
| `techniques/structured-output.md` | 抽取、分类、API、任何下游要解析的输出 |
| `techniques/context-engineering.md` | 输入很长（>1 万字）、多轮、要喂资料库 |
| `techniques/ambition-4d.md` | 请求是要给人看的交付物名词／用户用形容词代替标准／涉及开会汇报决策／需要借跨领域方法（判定规则见卡内第 2 节） |

### 默认技法组合（按模式）

| 模式 | 默认配对 |
|---|---|
| creative | pingpong-iteration + johari（有转化或决策目标时 + ambition-4d） |
| research | citation-anchoring + self-critique + context-engineering + ambition-4d |
| report | citation-anchoring + rcare + self-critique + ambition-4d |
| extraction | structured-output + token-economy |
| learning | johari + self-critique |
| procedure | decomposition + self-critique |
| agentic | decomposition + context-engineering（目标是长期结果时 + ambition-4d，只用高度与外部验证） |
| image-video | 无（视觉提示词规则在模式文件里） |
| automation | structured-output + token-economy |

**默认不加 ambition-4d**：extraction、automation、image-video、procedure、learning——动作已固定或目标本就是动词，加了只多耗 token（见卡内 2.2）。

---

## ④ 组合示例（照着选）

| 用户请求 | 组合 |
|---|---|
| "帮我写个提示词，让 AI 做一份 AI 教育行业深度调研报告（给投资人看）" | `modes/research.md` + `domains/research-consulting.md`（**不选** education-training，它讲的是做课招生；也不选 finance，投资人只是交付用途）+ citation-anchoring + self-critique + context-engineering |
| "我要给老板汇报今年增长，帮我写提示词" | `modes/report.md` + `domains/workplace-communication.md` + rcare + citation-anchoring |
| "把一千条用户反馈分类打标" | `modes/extraction.md` + `domains/tech-product.md` + structured-output + token-economy |
| "小红书爆款标题，帮我想 20 个" | `modes/creative.md` + `domains/media-content.md` + pingpong-iteration |
| "这条提示词为什么输出总跑偏" | 诊断模式：`rubric.md` → 三档 + 问题清单 + 改写 |

---

## ⑤ 素材来源对照（用户笔记 → 落到哪）

| 素材 | 内容 | 落到 |
|---|---|---|
| 李厂长《15分钟学会提示词9大秘籍》 | 乔哈里视窗、框架脚手架、推理模型禁 CoT、乒乓球迭代、例子即背景、单次 vs 复用、拆任务、具象化 | `techniques/johari.md`、`techniques/pingpong-iteration.md`、`anti-patterns.md`、`modes/creative.md` |
| 孔老師 AI 研習社 Gem 指令 | TCREI 五段模板（任务主题/上下文/具体信息/目标/格式） | `modes/creative.md` 骨架、`gallery.md` |
| 李厂长 13 套框架 | APE/BROKE/COAST/TAG/RISE/TRACE/ERA/CARE/ROSES/ICIO/CRISPE/RACE/CREATE | `techniques/frameworks-13.md` |
| Axton《重构个体》26 模板 | RCARE/RICE、引用锚定、反思校对、Token 优化、分步引导、三段论、多模态、Make 自动化 | `techniques/rcare.md`、`citation-anchoring.md`、`self-critique.md`、`token-economy.md`、`decomposition.md`、`modes/image-video.md`、`modes/automation.md` |
| 通用附加指令清单 | 澄清模糊点、时效信源、顾问视角、双语术语、任务类型判定、多模态、准确性核查 | `techniques/addon-checklist.md` |
| 提示词杂记（五顾问、元提示、六段位、Claude 五招） | 五顾问评审、元提示、进阶路径；/ghost、L99、/god mode 已辟谣 | `techniques/five-advisors.md`、`anti-patterns.md` |
| Gemini 视频分析专家配置 | 两套视频人设（全能学习型 / 自媒体拆解型） | `domains/media-content.md` |
| 个人学习笔记原文 | 全部素材 | `sources.md` 署名与置信度 |
| Felix Rieseberg《How to be more ambitious》原文 + 二次创作短视频《Claude 主管的 AI 用法：4 大维度》 | 速度／高度／深度／范围；名词换动词；三步升级；深度元提示词；借方法不扮角色；外部裁判 | `techniques/ambition-4d.md`、`interview.md`、`rubric.md` 第 7 节、`anti-patterns.md` 第 17 条 |
| Boris Cherny《Mastering Claude Code in 30 minutes》演讲 | 先计划再写码；说目标不指定工具；给可运行的反馈让它迭代；三种工作流；CLAUDE.md 要短、反复纠正固化；`claude -p` 管道 | `modes/agentic.md`、`modes/automation.md`、`techniques/context-engineering.md` |
