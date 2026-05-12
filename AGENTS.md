# Codex 协作规则

这个仓库是一套由 Codex 代管的 AI知识加工流水线。

## 目录
- `drop/`：原始素材入口。文章片段、文章链接、GitHub 仓库链接、碎碎念、代码片段都放这里。
- `distill/`：Codex 从 `drop/` 提炼出的第一阶段半成品。默认少而精，按主题聚合。
- `notes/`：最终知识笔记。
- `outputs/`：可对外发布的成品内容。
- `news/`：新闻内容，仅用于滚动 AI 早报。
- `life/`：生活随笔，不参与默认整理。

## 归档
以下目录都带自己的归档区：
- `drop/_archive/`
- `distill/_archive/`
- `notes/_archive/`
- `outputs/_archive/`
- `news/_archive/`

规则：
- 归档时只移动文件，不改写内容。
- 默认归档到当前目录自己的 `_archive/`。
- 不跨目录归档。
- `life/` 默认不参与自动归档。

## 处理规则
- `drop/` 下除 `_archive/` 外的所有文件，默认都视为待处理素材。
- 不需要待处理清单文件。
- 当用户要求“整理 drop”时，读取 `drop/` 内所有未归档文件。
- 链接类素材要尽量读取原文再整理；读不到时至少结合上下文保留价值判断。
- 整理结果默认写入 `distill/`，不要直接写入 `notes/`。
- 默认少而精，优先按主题聚合，不要机械地一条素材生成一篇文件。
- 在 `distill/` 和 `notes/` 中，由 Codex 维护轻量级 `[[wikilink]]`，优先链接稳定概念和已有笔记。
- 用户不需要手工维护双向链接。

## 分层规则
- `drop/`：原料层
- `distill/`：内部半成品层
- `notes/`：知识沉淀层
- `outputs/`：发布层

## 轻量 frontmatter 规则
- `distill/`、`notes/`、`outputs/` 统一允许使用极简 frontmatter，只保留：

```yaml
---
updated: YYYY-MM-DD
---
```

- 每次 Codex 更新这三个目录内的文件时，都要同步更新 `updated`
- `drop/` 原始素材默认不要求 frontmatter
- `life/` 默认不要求 frontmatter

## distill 规则
- `distill/` 内的文件按主题长期滚动更新，不按每次处理新建一堆文件。
- 每次新增内容时，都要在正文里增加一个时间标题，默认使用：

```md
## YYYY-MM-DD
```

- 新增内容按时间倒序追加，新的更新时间段放在更靠前的位置

## 新闻规则
- 新闻默认只进入 `news/`
- 不默认把新闻直接写进 `distill/` 或 `notes/`
- `news/AI早报.md` 是滚动文件，不按日期拆成多个文件
- 新内容按日期倒序追加
- 输出以提炼为主，只保留必要链接

## life 规则
- `life/` 只放用户自己的生活随笔
- 不默认整理
- 不默认归档
- 只有用户明确要求时才处理

## 写作和维护原则
- 不要求用户写 frontmatter，`distill/`、`notes/`、`outputs/` 的极简 `updated` 由 Codex 维护
- 不要求用户维护标签、分类、导航页
- 不为了整齐增加维护负担
- 能用目录表达的，就不要用额外元数据表达
- 默认中文输出
- 笔记开头的 `> [!abstract]` 摘要块由 Codex 视内容成熟度决定是否添加和更新
