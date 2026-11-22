# 13 套提示词框架速查（APE / BROKE / COAST / TAG / RISE / TRACE / ERA / CARE / ROSES / ICIO / CRISPE / RACE / CREATE）

**什么时候读这个文件**：你知道"提示词框架"这东西，但面对 13 个缩写不知道选哪个；或者写完提示词想用框架做一次漏项体检。
**读完你会得到什么**：一张能按"缺什么"反查的速查表、13 套框架的要素释义与最强场景、以及一份"什么时候别用框架"的判断清单。

## 什么时候用

- 用户说"有没有提示词模板/框架""套哪个公式比较好"。
- 你要检查一条提示词漏了什么（框架当 checklist 用，不是当表格填）。
- 要给团队或学员讲清这 13 个缩写的差别。
- 同一任务要固化成模板，需要选一套当骨架。

## 怎么做

1. **按"缺什么"选，不按"哪个更高级"选**：缺背景 → BROKE / COAST / ICIO / CRISPE；缺角色 → RACE / RISE / CREATE / ERA / CARE；缺示例 → CREATE / TRACE / CARE；缺交付形态 → CREATE（Type of Output）/ ICIO（Output Indicator）；要留迭代位 → BROKE（Evolve）/ CRISPE（Experiment）。
2. **只填 3–4 个关键字段**。13 套里没有一套要求每个字母都写满；框架是脚手架，不是表单（笔记秘籍 2）。
3. **框架名不必出现在提示词里**。用小标题或自然语言分块即可——模型读的是内容，不是缩写。
4. **反过来当体检表**：写完提示词后逐字段问"删掉这段，输出会变吗？"不变就是装饰性槽位，删。
5. **一次性任务不套框架**；反复用的任务才值得选一套固化下来。

| 框架 | 要素 | 最强场景 | 提醒 |
|---|---|---|---|
| APE | Action 行动 / Purpose 目的 / Expectation 期望 | 最短的"干活型"提示词 | 没有角色和示例位，风格类任务不够用 |
| BROKE | Background 背景 / Role 角色 / Objectives 目标 / Key Result 关键结果 / Evolve 试验改进 | 需要反复调优的任务 | 唯一内建"迭代"位，适合会被改五遍的方案 |
| COAST | Context 上下文 / Objective 目标 / Action 行动 / Scenario 场景 / Task 任务 | 咨询、方案类长任务 | 四格都在讲"做什么"，容易重复；留 Context + Objective + Task 往往就够 |
| TAG | Task 任务 / Action 行动 / Goal 目标 | 快速澄清需求 | 与 APE 高度重叠，选一个即可 |
| RISE | Role 角色 / Input 输入 / Steps 步骤 / Expectation 期望 | 有明确步骤的操作任务 | **不要给推理模型**（内含 Steps，等于指定思考步骤） |
| TRACE | Task 任务 / Request 请求 / Action 行动 / Context 上下文 / Example 示例 | 要风格示例的写作任务 | Task / Request / Action 三格同义，删到一格即可 |
| ERA | Expectation 期望 / Role 角色 / Action 行动 | 极简任务 | 三格就够，别硬凑 |
| CARE | Context 上下文 / Action 行动 / Result 结果 / Example 示例 | 交付格式卡得很死的任务 | Result + Example 是它最大的价值 |
| ROSES | Role 角色 / Objective 目标 / Scenario 场景 / Expected Solution 期望方案 / Steps 步骤 | 要"方案 + 步骤"的咨询任务 | 同样含 Steps，推理模型慎用 |
| ICIO | Instruction 指令 / Context 背景 / Input Data 输入数据 / Output Indicator 输出引导 | 数据处理、抽取任务 | 处理"喂进去的材料"时最好用的一套 |
| CRISPE | Capacity & Role 角色 / Insight 见解 / Statement 声明 / Personality 个性 / Experiment 实验 | 要"多版本方案"的探索任务 | Experiment 位是特色：直接要求给多个方案 |
| RACE | Role 角色 / Action 行动 / Context 上下文 / Expectation 期望 | 通用商务写作 | 与 ERA 只差 Context，别两套都填 |
| CREATE | Character 角色 / Request 要求 / Examples 示例 / Adjustments 调整 / Type of Output 输出类型 / Extras 额外补充 | 内容创作、营销文案 | 示例位 + 输出形态位最全；笔记里被点名的代表框架 |

### 什么时候别用框架

这一节比上面的表更重要——框架的失败案例比成功案例多：

1. **常识问题、单次闲聊**。问"北京到上海高铁多久"套 BROKE，既是浪费 token 也是浪费注意力。
2. **创造性任务的第一轮**。先给个大概让 AI 出初稿；框架留到第 2–3 轮、你已经知道要什么了再用（见[乒乓球迭代](./pingpong-iteration.md)）。
3. **推理模型**。内置思考的模型只吃目标、成功标准、边界；RISE / ROSES 这类含 Steps 的框架会限制它，属于官方明确反对的"指定思考步骤"。
4. **字段互相重复的框架混用**。COAST 的 Context/Scenario、TRACE 的 Task/Request/Action、APE 与 TAG 几乎同义；一次只用一套，混两套会出现重复或冲突的约束。
5. **你已经有稳定模板了**。模板是终点，框架是起点；能直接填槽位就别回头想缩写。
6. **字段填满但内容空转**。写了"角色：世界级专家"却没有任何行为差异，不如删掉——头衔对语气有用，对事实召回有害。

## 示例

同一个需求（SaaS 落地页首屏文案），两套框架的差别：

用 APE（最短，够用）：

```text
【行动】写 SaaS 落地页首屏：主标题 + 副标题 + 按钮文字。
【目的】让用 Excel 管客户的中小团队点进免费试用。
【期望】主标题 ≤14 字，副标题 ≤40 字，按钮 4 字以内；
不用"赋能""闭环""一站式"这类词。
```

用 CREATE（要示例和多方向时更合适）：

```text
【角色】B2B SaaS 落地页文案，写给中小团队老板看。
【要求】首屏三件套：主标题 / 副标题 / 按钮。
痛点：客户线索散在 Excel、微信、邮件里，销售每天花 1 小时找资料。
【示例】参考这种句式（不要照抄）：主标题"客户不再漏在微信里"；
副标题"把微信、Excel、邮件里的客户线索收进一个看板"。
【输出类型】Markdown 三行，每行前加标签。
【额外】给 2 个方向：一个主打"不漏客户"，一个主打"少花时间"。
```

说明：这条需求里有明显的"痛点 + 语气 + 要多方向"成分，所以 CREATE 的 Examples / Type of Output / Extras 三个位都用得上。APE 版更快，但拿不到示例对齐和双方向。

## 常见坑

- 不要把 13 个缩写当质量等级。它们是同一批信息的不同排布方式，选错框架不会让提示词变差，填满框架才会。
- 不要为凑字母编内容。填不出 Key Result 就空着，硬写的"关键结果"会让模型追一个你其实不想要的目标。
- 不要给推理模型套带 Steps 的框架（RISE / ROSES）。需要步骤的是执行类、有严格顺序的操作任务。
- 不要在一条提示词里混两套框架。字段重叠带来重复约束，模型会在两条冲突的指令之间随机选一条。
- 不要把框架当交付物。用户要的是能用的提示词，不是一张填好的框架表。

## 出处

李厂长《15分钟学会提示词9大秘籍》配套的 13 套框架表（APE / BROKE / COAST / TAG / RISE / TRACE / ERA / CARE / ROSES / ICIO / CRISPE / RACE / CREATE 及各字段释义），以及该笔记秘籍 2「框架是脚手架，可自由增删」。框架本身是社区流传的通用写法，无单一原始出处；"别给推理模型写步骤"的依据见 `../models.md` 的判断规则。
