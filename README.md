# Simple Workflow MVP - 多 Agent 代码审查与修复流水线

## 一、 项目说明

本项目是基于大语言模型（LLM）构建的**多 Agent 协作 Workflow（工作流）**系统。通过模拟软件工程中真实的代码生产链路，实现了从“需求理解 -> 代码生成 -> 代码审查 -> 代码修复”的完整自动化闭环。

本项目在 Homework 1（单 Agent 代码助手）的基础上进行了架构升级，从单点交互进化为具备状态管理和流程控制的多节点流水线，旨在探索多 Agent 协作解决复杂任务的潜力。

## 二、 设计文档 (Design Document)

### 2.1 核心概念与架构
系统采用面向对象设计，各个 Agent 作为工作流中的独立节点。为了让各个节点解耦，系统引入了**全局状态管理 (State)** 和 **Agent 通信机制**。
*   **状态管理**：使用一个全局字典 `state`，存储需求、草稿代码、审查意见等上下文数据，随流程推进不断更新。
*   **Agent 通信**：上一个 Agent 的文本输出（`content`），作为下一个 Agent 的输入（`user` prompt），实现消息传递。

### 2.2 Agent 节点组成
基于 `BaseAgent` 基类，扩展出三个具体的执行节点：
1.  **编码 Agent (CoderAgent)**：接收用户需求，生成初始的完整代码。
2.  **审查 Agent (ReviewerAgent)**：严格检查代码逻辑、Bug或安全隐患。若完美则输出 `[PASS]`，否则输出具体的修改建议。
3.  **修复 Agent (FixerAgent)**：根据审查意见，对原始代码进行重构或修复。

### 2.3 Workflow 流程控制
系统实现了顺序执行与条件分支控制。流程图如下：

```text
       [ 用户需求 (User Input) ]
                 ↓
         [ 编码 Agent ] ──────> 产出 draft_code
                 ↓
         [ 审查 Agent ] ──────> 产出 review_comments
                 ↓
     { 检查意见中是否包含 '[PASS]' }
        ├── 是：流程结束，输出最终代码
        └── 否：[ 修复 Agent ] ──> 产出 final_code (覆盖 draft_code)
                                      └─────> (循环回到审查环节)
```

### 2.4 可扩展性设计 (Extensibility)
为了满足后续迭代需求，本架构具备良好的可扩展性：
*   **新增 Agent**：只需继承 `BaseAgent` 并配置新的 System Prompt，即可在主程序中插入新的工作流节点（如增加一个“测试用例生成 Agent”）。
*   **修改流程**：各 Agent 不直接耦合，仅通过 `state` 字典交互。这使得系统可以轻松从“顺序执行”修改为“并行执行”或“多轮循环”。

## 三、 使用方法 (Usage Guide)

### 3.1 环境准备
确保本地已安装 Python 3.8+。在终端中执行以下命令安装依赖包：

```bash
pip install openai python-dotenv
```

### 3.2 配置大模型 API
1. 找到项目根目录下的 `.env.example` 文件，将其重命名为 `.env`。
2. 打开 `.env` 文件，填入你所用服务商的 API Key 和 Base URL。*(默认兼容支持 OpenAI 格式的接口，如 DeepSeek、通义千问、Kimi等)*

**以 DeepSeek 为例，`.env` 内容如下：**

```env
LLM_API_KEY=sk-替换为你自己的真实API_KEY
LLM_BASE_URL=https://api.deepseek.com/v1
```

*(注：若使用其他平台，请同步修改 `workflow.py` 中 `client.chat.completions.create` 的 `model` 参数为对应的模型名)*。

### 3.3 运行程序
在终端中执行主程序：

```bash
python workflow.py
```

根据终端提示，输入你的开发需求，例如：
> `写一个计算两数相除的函数，要求处理除数为 0 的异常。`

程序将自动开始执行，你可以在终端观察到三个 Agent 依次“思考”、“通信”并流转的过程，最终输出通过审查的完美代码。
