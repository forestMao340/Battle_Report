# AI 智能翻译与战报生成 API

基于 FastAPI + DeepSeek 构建的多功能 AI 服务，提供通用翻译、文言文翻译、战报生成功能，并支持流式输出（SSE）。

## 🚀 公网访问地址

- **Swagger API 文档**: [http://39.106.78.243/docs](http://39.106.78.243/docs)
- **流式演示界面**: [http://39.106.78.243/static/index.html](http://39.106.78.243/static/index.html)

> 公网已部署，可直接体验流式输出效果。
> 服务部署于阿里云 ECS（2核 4GB），已稳定运行。

---

## ✨ 功能列表

| 功能 | 描述 | 端点 |
| :--- | :--- | :--- |
| 通用翻译 | 支持中英日法德等多语言互译 | `POST /translate`<br>`POST /translate/stream` (流式) |
| 文言文翻译 | 将文言文翻译为现代白话文 | `POST /translate/classical`<br>`POST /translate/classical/stream` (流式) |
| 战报生成（RAG 增强） | 基于 ChromaDB 检索知识库，更准确、有考据地生成三种风格战报（古典白话、北欧史诗、黑暗哥特） | `POST /battle_report`<br>`POST /battle_report/stream` (流式) |

所有流式接口均使用 `text/event-stream` 响应，可实时逐字输出。

---

## 🛠️ 技术栈

- **框架**: FastAPI 0.115+
- **服务器**: Uvicorn (ASGI)
- **AI 模型**: DeepSeek V4 Pro (OpenAI SDK)
- **数据校验**: Pydantic 2.10+
- **容器化**: Docker & Docker Compose
- **前端**: HTML + Tailwind CSS + 原生 JavaScript

---

## 📦 本地开发环境搭建

### 1. 克隆项目
```bash
git clone https://github.com/forestMao340/Battle_Report.git
cd my_api_project

---

### 2. 创建并激活虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

---

### 3.安装依赖

```bash
pip install -r requirements.txt

---

### 4.配置环境变量

创建 .env 文件（参考 .env.example）：

```text
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥

---

### 5.启动服务

```bash
uvicorn app.main:app --reload

访问 http://localhost:8000/docs 查看 API 文档，访问 http://localhost:8000/static/index.html 体验流式界面。

---

## 🧠 RAG（检索增强生成）架构

本项目在战报生成中集成了 RAG 技术：

1. **知识库构建**：将《西游记》原著、北欧神话、战锤40K背景等文本切块，使用 `sentence-transformers` 生成向量，存入 ChromaDB。
2. **检索增强**：用户请求战报时，系统先根据输入（进攻方、防守方、地点、风格）检索最相关的 3 个知识块。
3. **生成增强**：将检索到的知识块作为上下文，连同提示词一起发送给 DeepSeek，生成更准确、有考据的战报。

**技术组件**：
- **向量数据库**：ChromaDB（持久化存储）
- **Embedding 模型**：`paraphrase-multilingual-MiniLM-L12-v2`（支持中文）
- **生成模型**：DeepSeek V4（通过 OpenAI SDK 调用）

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t my-fastapi-api .

---

### 运行容器

```bash
docker run -d -p 80:8000 --restart always --name fastapi-app \
  -e DEEPSEEK_API_KEY="你的密钥" \
  -e PYTHONUTF8=1 \
  my-fastapi-api

---

### 使用 Docker Compose（推荐）

```bash
docker-compose up -d

---

## ☁️ 公网部署说明

项目已部署至公网服务器，通过 Docker 容器运行。

### ☁️ 部署要求

- **最低配置**：2核 4GB 内存（推荐，用于支持 ChromaDB + PyTorch）
- **操作系统**：Alibaba Cloud Linux 3 / Ubuntu 20.04+
- **依赖**：Docker 20.10+、Python 3.10+

### 本地构建与推送
```bash
docker build -t my-fastapi-api .
docker tag my-fastapi-api <your-registry>/<your-repo>:latest
docker push <your-registry>/<your-repo>:latest

### 服务器拉取与重启
ssh root@<your-server-ip>
docker pull <your-registry>/<your-repo>:latest
docker stop fastapi-app && docker rm fastapi-app
docker run -d -p 80:8000 --restart always --name fastapi-app \
  -e DEEPSEEK_API_KEY="你的密钥" \
  -e PYTHONUTF8=1 \
  <your-registry>/<your-repo>:latest

---

## 📁 项目结构

```text

my_api_project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置类
│   ├── models.py               # Pydantic 模型
│   ├── routers/                # 路由层
│   │   ├── translate.py
│   │   └── battle.py
│   ├── services/               # 业务逻辑层
│   │   ├── ai_client.py        # DeepSeek 调用（含流式）
│   │   ├── translate.py
│   │   └── battle.py
|   |   └── rag_indexer.py 
│   ├── static/                 # 前端静态文件
│   │   └── index.html          # 流式演示界面
│   └── utils/
│       └── helpers.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

---

## 🧪 API 使用示例

### 通用翻译（非流式）

```bash 
curl -X POST http://39.106.78.243/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","target_lang":"zh"}'

---

### 流式战报生成

```bash
curl -X POST http://39.106.78.243/battle_report/stream \
  -H "Content-Type: application/json" \
  -d '{"attacker":"孙悟空","defender":"二郎神","location":"花果山","plot":"大战三百回合","style":"classical"}' \
  --no-buffer

---

## 📌 环境变量说明

变量名	            必填	      描述
DEEPSEEK_API_KEY	✅	 DeepSeek API 密钥
PYTHONUTF8	        ❌	 设为 1 避免中文乱码

---

## 🧹 代码注释规范

---

所有函数、类、接口均包含清晰的 docstring，关键逻辑有行内注释，便于维护。

---

## 🤝 贡献指南

欢迎提交 issue 或 PR，请确保代码符合 PEP 8，并更新相应文档

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

DeepSeek 官网 https://www.deepseek.com/
FastAPI  文档 https://fastapi.tiangolo.com/
项目仓库  https://github.com/forestMao340/Battle_Report