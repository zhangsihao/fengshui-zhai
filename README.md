# 🏠 住宅户型分析 (Floor Plan Analyzer)

基于 AI Agent 架构的住宅户型分析工具。上传户型图，AI 结合传统风水知识库，为你生成专业的户型分析报告。

## ✨ 功能特点

- 🤖 **AI Agent 架构**：不是简单的 API 调用，而是具备感知、推理、决策能力的智能体
- 📚 **专业知识库**：基于《住宅风水图解》提取的结构化户型分析规则
- 🔧 **灵活配置**：支持任意兼容 OpenAI 格式的大模型 API（GPT-4o、Claude、通义千问等）
- 🖼️ **图片分析**：上传户型图即可获得分析报告
- 📋 **报告下载**：分析结果可一键下载保存

## 📁 项目结构

```
feng-shui-app/
├── README.md              # 项目说明
├── requirements.txt       # Python 依赖
├── config.yaml            # 配置模板
├── run.py                 # 一键启动脚本
├── backend/
│   ├── app.py             # Flask 后端服务
│   └── agent.py           # AI Agent 核心逻辑
├── frontend/
│   └── app.py             # Streamlit 前端界面
└── knowledge/
    └── feng_shui_skills.json  # 风水知识库
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/feng-shui-app.git
cd feng-shui-app
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置模型

复制配置模板并填入你的大模型 API 信息：

编辑 `config.yaml`：

```yaml
model:
  # 支持任意兼容 OpenAI 格式的 API
  base_url: "https://api.openai.com/v1"      # API 地址
  api_key: "sk-your-api-key-here"             # 你的 API Key
  model_name: "gpt-4o"                        # 模型名称
```

> ⚠️ 注意：模型需要支持视觉（Vision）能力，能够理解图片。

### 4. 一键启动

```bash
python run.py
```

启动后自动打开浏览器访问 `http://localhost:8501`。

### 5. 使用

1. 在页面上传一张户型图（支持 JPG、PNG、WebP）
2. 预览图片确认无误
3. 点击「分析户型」按钮
4. 等待 AI 分析，查看户型分析报告
5. 可点击「下载分析报告」保存结果

## 🧠 AI Agent 架构

本项目采用 AI Agent 模式，而非传统的直接 API 调用：

```
用户上传户型图
      ↓
  ┌─────────────┐
  │   Agent 感知  │  接收并理解户型图内容
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │   Agent 推理  │  结合知识库分析户型
  │  (知识库驱动) │  逐条对照风水规则
  └──────┬──────┘
         ↓
  ┌─────────────┐
  │   Agent 行动  │  生成结构化分析报告
  └─────────────┘
         ↓
  返回户型分析报告
```

**与传统调用的区别：**

- 🧩 **知识驱动**：Agent 加载专业知识库作为推理依据，不是凭空分析
- 🎯 **角色定义**：Agent 有明确的身份和能力定义，分析更专业
- 📐 **流程规范**：Agent 遵循固定的分析流程（识别→对照→评价→建议）
- 📊 **结构化输出**：Agent 按照固定格式输出报告，信息清晰完整

## 📄 许可证

MIT License

## ⚠️ 免责声明

本项目仅供学习和娱乐使用。户型分析结果由 AI 模型基于传统风水知识生成，不构成任何实际建议。请理性看待风水文化，不要将分析结果作为购房、装修等重大决策的依据。
