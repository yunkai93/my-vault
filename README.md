# AI知识库说明

这是一个由 Codex 协助维护的个人 AI知识库，目标不是手工做复杂整理，而是把素材逐步加工成真正有用的内容。

## 核心思路

这套仓库按内容阶段分层，而不是按作者分层：

- `drop/`：原始素材
- `distill/`：从素材提炼出来的半成品
- `notes/`：最终知识笔记
- `outputs/`：可对外发布的内容
- `news/`：滚动 AI 早报
- `life/`：生活随笔，不参与默认整理

## 你平时怎么用

### 1. 往 `drop/` 扔素材
你不用考虑分类，也不用管格式统一。

可以直接往里面放：
- 文章片段
- 文章链接
- GitHub 仓库链接
- AI相关碎碎念
- 代码片段

### 2. 让 Codex 整理
常用说法：
- “整理 drop”
- “把 drop 里的内容整理成专题笔记”
- “从最近素材里提炼一篇总结”

Codex 默认会：
- 读取 `drop/` 下所有未归档文件
- 提炼和聚合相近主题
- 生成少而精的结果
- 把结果写到 `distill/`
- 再把已处理素材移到 `drop/_archive/`
- 在合适的 `distill/` / `notes/` 笔记中补充必要的 `[[wikilink]]`
- 在需要时维护笔记开头的 `> [!abstract]` 摘要块

### 3. 从 `distill/` 进入下一阶段
- 值得长期保留的内容，进入 `notes/`
- 值得对外发布的内容，进入 `outputs/`

## 各目录职责

### `drop/`
原始素材入口。  
除 `_archive/` 外，其余内容默认都视为待处理。

### `distill/`
内部半成品区。  
这里是 Codex 对素材的第一次整理结果，不代表已经是最终知识或可发布内容。

`distill/` 采用按主题长期滚动更新的方式，而不是每次整理生成新文件。

这里以及 `notes/`、`outputs/` 都统一允许保留一个极简 frontmatter：

```yaml
---
updated: YYYY-MM-DD
---
```

每次更新时：
- 同步更新 `updated`
- 在正文新增一个时间标题，例如 `## 2026-05-12`
- 新增内容按时间倒序追加

### `notes/`
最终知识沉淀区。  
放那些你认可、准备长期保留的 AI知识笔记。

`notes/` 也允许使用同样的极简 `updated` frontmatter，由 Codex 维护。

### `outputs/`
发布区。  
放对外可用的内容，比如文章、分享稿、公开总结、周报等。

`outputs/` 同样允许使用极简 `updated` frontmatter，由 Codex 维护。

### `news/`
只负责新闻。  
目前约定使用单一滚动文件 `news/AI早报.md`。

### `life/`
生活随笔区。  
默认不参与 Codex 的整理和归档流程。

## 归档规则

每个主要工作目录都有自己的归档区：

- `drop/_archive/`
- `distill/_archive/`
- `notes/_archive/`
- `outputs/_archive/`
- `news/_archive/`

归档时只移动文件，不改写内容，也不跨目录归档。

## 已定原则

- 不要求你手工写 frontmatter
- 不要求标签系统
- 不要求你手动归档和分类
- 不要求你手工维护双向链接
- `drop/` 的产物先进入 `distill/`
- 新闻默认只进 `news/`
- `life/` 默认不参与整理
- Codex 会在 `distill/` 和 `notes/` 中维护轻量级链接与摘要块
- `distill/`、`notes/`、`outputs/` 统一使用极简 `updated` frontmatter
- `distill/` 按主题滚动维护，并记录最后更新时间

## 当前适合的工作方式

你只需要做两件事：

1. 把 AI素材扔到 `drop/`
2. 在需要时让 Codex 整理

其他结构维护都不应该成为你的负担。
