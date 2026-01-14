💰 Financial AI Agent (Budget Assistant)
这是一个基于 Python 与 智谱AI (GLM-4) 开发的智能财务审计体（AI Agent）。它结合了确定性的数学计算逻辑与大语言模型的自然语言处理能力，为用户提供精准、人性化的财务建议。

🌟 项目亮点 (Project Highlights)
逻辑与语义解耦 (Decoupled Architecture)：核心财务计算由 Python 后端完成（Deterministic Logic），确保数据 100% 准确；语义理解与建议生成由 LLM 负责，规避了大模型的“幻觉”计算误差。

健壮的输入校验 (Robust Input Validation)：内置 read_float 函数，利用 try...except 机制处理异常输入，提升了系统的稳定性和容错性。

企业级 API 解析 (Standardized API Handling)：实现了对智谱AI chat.completions 接口的调用，并精准解析嵌套的 JSON 响应报文。

🏗️ 核心逻辑 (Core Logic)
数据采集：通过命令行交互获取用户的月收入、固定支出及储蓄目标。

业务核算：Python 函数根据输入计算资金结余、储蓄目标达成率，并根据预设业务规则生成结构化事实报告。

AI 推理：将结构化报告作为上下文（Context）传递给 GLM-4 模型，生成具有针对性、专业性且语感自然的理财策略。

🛠️ 技术栈 (Tech Stack)
Language: Python 3.x

AI SDK: ZhipuAI Python SDK

Environment: Virtual Environment (.venv)

🚀 快速开始 (Quick Start)
1.克隆项目到本地。

2.在 .venv 环境下安装依赖：pip install zhipuai sniffio。

3.在代码中配置您的 api_key。

4.运行程序：python Financial_AI_Agent_LLM.py。
