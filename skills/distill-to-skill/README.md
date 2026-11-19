# distill-to-skill

把**书籍 / 文章 / 视频 / 课程**或**你自己做成过的工作**，蒸馏成一个可加载、可验收的 Agent Skill。

> 蒸馏不是压缩文字，而是让「下次同类任务」能直接使用的判断规则。
> 判断标准只有一条：**下次碰到同类任务，它能不能真的用起来。**

## 它解决什么问题

大多数人从资料里得到的是「总结」：倾听、共情、识别需求——听着都对，明天却用不上。
更糟的是，把 AI 为了你的场景临时补的内容，误当成原作者的结论，还把它写进"标准"里。

这个 skill 用固定流程避免这两件事：

1. **先定任务**，再提炼（目标句 + 验收句）
2. **每条规则标源**（原文 / AI 补充 / 我的经验 / 单次）
3. **三类分流**（必查标准 / 情境做法 / 单次信息）
4. **双案例验证**（旧案例回归 + 新案例迁移 + 缺口检测 + 越界检测）
5. **落成 SKILL.md**（可被 Agent 加载）

## 安装

放在任意一个 Agent 搜索 skills 的目录即可：

```bash
# 全局（所有会话可用）
cp -R distill-to-skill ~/.agents/skills/

# 或项目级（只在该项目可用）
mkdir -p .agents/skills && cp -R distill-to-skill .agents/skills/
```

DSH / Claude Code 之类的 harness，会扫描 `SKILL.md` 的 `description` 决定何时调用。

## 用法

直接把来源丢给它，并说清用途：

```
把这本书蒸馏成 skill：<文件/链接>
我要用它帮销售在报价前判断需求有没有问清楚。
```

```
我们刚才一起改完这份客户方案，帮我把判断标准提炼成 skill，
单次客户的特殊要求不要写成通用规则。
```

```
这个 skill 我改了三条规则，帮我跑一遍回归：旧案例 + 一个新客户。
```

## 产出结构

```
<skill-name>/
├── SKILL.md            # frontmatter(name/description) + 必查/情境/示例 + 步骤 + 验收
├── references/         # 可选：判定表、清单
├── assets/             # 可选：模板、示例
└── README.md
```

交付时同时给出：**目标句 + 三类分流表（带理由）+ 验证记录**。

## 目录说明

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 主流程：五条铁律、Phase 0–6、输出契约、反模式 |
| `references/source-route.md` | 资料型路线：类型判定 → 五问 → 标源 → 空跑 |
| `references/experience-route.md` | 经验型路线：做完再复盘 → 三类分流 → 换任务验证 |
| `references/rule-triage.md` | 决定性环节：三类判定三问 + 危险信号 |
| `references/acceptance.md` | 四项必测 + 验证记录模板 + 修订原则 |
| `assets/skill-template.md` | 生成新 skill 的骨架 |
| `assets/example-quote-check.md` | 完整成品示例（报价前需求缺口检查） |

## 维护原则

- 每次修订都记录：**这次哪里做错 / 为什么改 / 什么结果被接受**。
- 改完必须**旧案例和新案例都重跑**，防止修好新问题、弄坏旧能力。
- 不要写"请自动成长"——成长来自记录与回归，不来自一句话。

## 发布到 GitHub

```bash
cd distill-to-skill
git init
git add -A
git commit -m "feat: add distill-to-skill skill"
gh repo create <owner>/<repo> --private --source=. --push   # 公开用 --public
```

如果放在一个 skills 合集仓库里，建议按 `skills/<skill-name>/` 组织，并在仓库根 README 建索引。

## 出处

- 方法来源：小红书「AI 工作方式」系列《怎么把一本书蒸馏成你的技能》（06:17）
- 本 skill 是把该视频的方法**改造成可执行流程**，不是对原文的复述；
  视频未涉及的环节（如越界检测、验证记录模板、GitHub 发布）属于工程化补充。
