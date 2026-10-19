# Simple Workflow MVP - 代码审查与修复流水线

## 1. 项目说明
本项目基于大模型（LLM）构建了一个多 Agent 协作的简单 Workflow。通过模拟软件工程中的“编码 -> 审查 -> 修复”流程，实现了 Agent 之间的消息传递、状态共享以及基础的条件分支控制。

## 2. 架构设计
系统采用面向对象设计，包含三个核心 Agent：
*   **编码Agent (CoderAgent)**：根据用户需求生成初始代码。
*   **审查Agent (ReviewerAgent)**：检查代码的逻辑错误和安全性。若代码完美则返回 `[PASS]`，否则输出修改建议。
*   **修复Agent (FixerAgent)**：根据审查意见，对代码进行修复和完善。

### 状态管理与通信机制
使用全局字典 `state` 进行状态管理。各 Agent 的输入输出通过 `state` 字典中的 `draft_code`、`review_comments` 等字段进行传递，实现解耦。

### 流程图
```text
[用户需求] 
   ↓
[编码Agent] -> (输出 draft_code)
   ↓
[审查Agent] -> (输出 review_comments)
   ↓
(判断是否包含 '[PASS]')
 ├── 是：流程结束，输出最终代码
 └── 否：[修复Agent] -> (输出 final_code) -> 覆盖 draft_code -> 重新进入审查环节
