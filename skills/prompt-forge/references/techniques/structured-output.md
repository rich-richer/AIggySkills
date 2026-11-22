# 结构化输出（Structured Output）

**什么时候读这个文件**：输出要直接进程序、表格或数据库；字段固定；批量抽取；或者你正打算靠"强烈要求它只输出 JSON"来控格式。
**读完你会得到什么**：schema + enum + unknown 逃生口的三件套写法、一份完整可复制的抽取提示词，以及为什么措辞威胁已经过时。

## 什么时候用

- 输出会被下游代码消费（解析、入库、路由、渲染）。
- 批量抽取同一批字段（招聘 JD、发票、竞品页面、会议纪要）。
- 需要固定枚举值做分支判断（通过 / 驳回、重要 / 推广 / 其他）。
- 输出要进表格，字段顺序与命名必须稳定。
- 要给模型打分并做统计（分数必须可解析）。

## 怎么做

1. **优先用原生结构化输出**：模型或 API 提供的 JSON schema、严格模式、function calling，都比提示词措辞可靠。有 structured outputs 就不需要"你必须只输出 JSON，否则……"这类强措辞。
2. **三件套写全**：字段名 + 类型 + 允许值（enum）。缺任何一个，输出就会漂。
3. **留 unknown 逃生口**：每个字段允许 `"unknown"`，或加 `confidence: high|medium|low`。不给出口，模型会为了填满而编造——这是结构化抽取最主要的幻觉来源。
4. **定好空值语义**：没有值用 `null` 还是 `[]`？数字是整数还是字符串？日期用 ISO 8601？单位写在哪里？这些不定，下游解析就会崩。
5. **给两个示例**：一个"正常填充"的完整样例，一个"unknown 怎么填"的样例。这两个示例比十条规则有效。
6. **校验而不是重问**：用 schema 校验器检查；失败时只重试一次，并把错误信息回传（"上次输出违反了 work_mode 的 enum，请只修这一处"）。不要用"再问一遍模型"当验证手段。

骨架：

```text
请把输入内容抽取为下面的 JSON。只输出 JSON 本身，不要围栏、不要解释。

schema：
{
  "type": "object",
  "properties": {
    "company":   {"type": "string"},
    "title":     {"type": "string"},
    "city":      {"type": "string"},
    "salary_min_cny_month": {"type": ["integer", "null"]},
    "salary_max_cny_month": {"type": ["integer", "null"]},
    "experience_years_min": {"type": ["integer", "null"]},
    "skills":    {"type": "array", "items": {"type": "string"}},
    "work_mode": {"type": "string", "enum": ["onsite", "hybrid", "remote", "unknown"]}
  },
  "required": ["company", "title", "city", "work_mode"],
  "additionalProperties": false
}

规则：
- 缺失信息用 null（数组用 []），判断不了用 "unknown"，不要推测或补全。
- 薪资统一换算成"千元人民币/月"的整数；原文是年薪时除以 12 后四舍五入。
- skills 只放原文明确提到的技能词，不要补同义词。
```

## 示例

完整可用的抽取提示词（从招聘 JD 抽结构化字段）：

```text
# 任务
从下面的招聘 JD 中抽取字段，输出 JSON。

# 字段
company（公司名，原文照抄）、title（岗位名，原文照抄）、city（城市名，
只留城市不带区）、salary_min_cny_month / salary_max_cny_month（整数，
千元人民币/月，缺失为 null）、experience_years_min（整数，缺失为 null）、
skills（数组，原文提到的技术或工具词）、work_mode（enum：onsite / hybrid /
remote / unknown）。

# 规则
1. 只输出 JSON 本身，不要加代码围栏、不要前后解释。
2. 原文没写的一律 null 或 unknown，禁止推测。
3. 薪资若写"面议"或未提，两个薪资字段都为 null，不要给区间。
4. 数字不要加单位后缀，单位已写在字段名里。

# 示例输出（正常）
{"company":"某某科技","title":"数据分析师","city":"杭州",
 "salary_min_cny_month":15,"salary_max_cny_month":25,
 "experience_years_min":3,"skills":["SQL","Python","Tableau"],
 "work_mode":"hybrid"}

# 示例输出（缺信息）
{"company":"某某科技","title":"运营专员","city":"成都",
 "salary_min_cny_month":null,"salary_max_cny_month":null,
 "experience_years_min":null,"skills":[],"work_mode":"unknown"}

# 输入
[JD 正文]
```

说明：两个示例里，第二条比第一条更重要——它演示了"不知道就留空"，模型会照着这个行为走。

固定枚举做分支判断的极简版（来自 Axton 的邮件分类 / 审核员写法）：

```text
请分析以下邮件正文，判断其类别。类别只能是"重要"、"推广"、"其他"中的一种。
请只回答这三个词中的一个，不要添加任何解释或标点符号。
邮件正文如下：
{{邮件正文}}
```

## 常见坑

- 不要用威胁或强调措辞保证 JSON，也不要在 JSON 前后留解释空间。"你必须只输出 JSON，否则会失败"这类写法已被证明没有必要；能用原生 schema / 严格模式约束就别靠自然语言。
- 不要写三层以上嵌套的 schema。小模型在深层嵌套上出错率极高；能摊平成一张表就摊平。
- 不要不给 unknown 出口。没有出口的字段会被编造，而且编得很像真的。
- 不要用 Claude 4.6+ 的 prefill 技巧控格式。以 assistant 开头的续写写法在 4.6+ 会直接 400，改用 system 指令或结构化输出。
- 不要 enum 写中文、下游按英文匹配。枚举值选定一种语言，上下游一致。
- 不要让字段名含糊（"备注""其他信息"）。字段名本身就是抽取指令，含糊的名字会抽出含糊的内容。

## 出处

`../anti-patterns.md`（"靠强措辞保证 JSON"已失效；prefill 在 Claude 4.6+ 已废除；显式声明格式约定可提升鲁棒性）；`../models.md`（输出契约要写成具体动词与可判定格式）；Axton《重构个体》第 5 章 5.3.2 节"控制输出规格"（固定 Markdown 输出模板）与第 6 章提示词 23、25（邮件三分类、审核员"只回答通过或驳回"的极简枚举写法）。
