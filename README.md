# 智能笔记（Notebook RAG）

一个以「人为主、AI 为辅」的笔记 + 知识库问答应用：笔记支持 AI 辅助写作，知识库文档分类管理，对话基于知识库做 RAG（检索增强生成）。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | React 19 + Vite 6 + TypeScript + Tailwind CSS 4 |
| 后端 | FastAPI + Pydantic v2 + SQLAlchemy 2（async） |
| RAG | LangChain + Chroma（本地持久化向量库） |
| 关系数据库 | PostgreSQL（async，懒连接，可选） |
| 对话模型 | DeepSeek（OpenAI 兼容，默认） |
| 嵌入模型 | DashScope text-embedding-v4 / 阿里云百炼（OpenAI 兼容，默认） |

## 功能

- **笔记**：独立笔记管理，AI 辅助写作（续写 / 扩写 / 改写，流式输出），编辑器右侧相关文档推荐
- **知识库**：文档分类管理（上传选分类、分类筛选、一键改分类），支持 PDF / docx / pptx / txt / md
- **对话**：基于「全部文档或某个分类」的 RAG 问答，会话历史落库
- **设置**：每用户可覆盖对话 / 嵌入模型、接口地址（Base URL，适配网关 / One API）、API Key；模型列表在线拉取

## 界面展示

### 笔记

笔记列表：

![note](./pic/note.png)

AI 辅助写作（续写 / 扩写 / 改写，流式）：

![noteWrite](./pic/noteWrite.png)

### 知识库

文档分类管理（上传选分类、分类筛选、改分类）：

![konwledgeBase](./pic/konwledgeBase.png)

### 对话

基于知识库分类的 RAG 问答：

![chat](./pic/chat.png)

### 设置

AI 提供商配置（对话 / 嵌入模型、接口地址、API Key、在线模型拉取）：

![aiProviderSetting](./pic/aiProviderSetting.png)

用户设置（账号、外观偏好等）：

![userSetting](./pic/userSetting.png)

## 快速开始

### 1. 后端

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate      # Git Bash；cmd 用 .venv\Scripts\activate.bat
pip install -r requirements.txt

cp .env.example .env               # 按模板填入真实 API Key（见下）
uvicorn app.main:app --reload --port 8000
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev                        # `http://localhost:5173`，/api 自动代理到 :8000
```

打开 `http://localhost:5173`，注册账号后即可使用。

## 配置说明（backend/.env）

配置统一放 `backend/.env`（**已 gitignore，不会上传**），`.env.example` 为模板。统一前缀：`LLM_*` = 对话模型，`EMBED_*` = 嵌入模型。

```ini
# 对话模型（默认 DeepSeek）
LLM_API_KEY="<你的 DeepSeek API Key>"
LLM_BASE_URL="https://api.deepseek.com"
LLM_MODEL="deepseek-v4-flash"
LLM_TEMPERATURE=0.2

# 嵌入模型（默认阿里云百炼 DashScope）
EMBED_MODEL="text-embedding-v4"
EMBED_API_KEY="<你的百炼 API Key>"
EMBED_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
EMBED_BATCH_SIZE=20

# PostgreSQL（可选）：不配置也能启动，仅对话历史与文档元数据不落库
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/note_book

# JWT 签名 + 用户级 API Key 加密派生密钥（生产环境必须换强随机值）
SECRET_KEY="<至少32位随机字符串>"

# LangSmith 链路追踪（可选）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=notebook_rag
LANGCHAIN_API_KEY="<你的 LangSmith Key>"
```

### 默认提供商与密钥获取

本项目默认使用两家厂商的 OpenAI 兼容接口：

- **对话模型 → DeepSeek**：官方 API 平台 <https://platform.deepseek.com/> 注册并创建 API Key，填到 `LLM_API_KEY`。
- **嵌入模型 → 阿里云百炼（DashScope）**：<https://bailian.console.aliyun.com/cn-beijing#/home> 开通百炼并创建 API Key（用 **DashScope OpenAI 兼容模式** 地址），填到 `EMBED_API_KEY`。

想快速尝试，拿到上面两个 Key 填进 `.env` 即可启动。

### 运行时自定义

登录后在「设置」页可覆盖系统默认：切换对话 / 嵌入提供商、填自己的 API Key、自定义接口地址（网关 / One API 填 `/v1` 地址）、在线拉取该提供商的模型列表。用户级 API Key 用 `SECRET_KEY` 派生密钥加密后存库。

## 验证接口

```bash
# 健康检查（进程活着即 200）
curl http://localhost:8000/api/v1/health
```

## 目录结构

```text
notebook/
├── backend/                  # FastAPI 后端
│   ├── .env.example          # 配置模板（复制为 .env）
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py           # 应用工厂：lifespan、CORS、路由、异常处理
│   │   ├── core/config.py    # 统一前缀 LLM_*/EMBED_* 配置
│   │   ├── api/v1/           # 路由：health / auth / notes / documents / rag / chat / settings
│   │   ├── schemas/          # Pydantic 出入参
│   │   ├── models/           # SQLAlchemy ORM（notes / documents / chat / user_settings）
│   │   ├── db/               # 引擎、会话、幂等迁移
│   │   └── services/rag/     # RAG 流水线 + 用户设置折叠解析
│   ├── scripts/              # 冒烟脚本 / RAG 评测
│   └── sample_data/          # 样例文档
├── frontend/                 # React 19 + Vite 6 前端
│   └── src/
│       ├── api/              # axios 客户端（相对路径，dev 走 Vite 代理）
│       ├── components/       # 通用组件（Modal / Pill / ModelPicker 等）
│       ├── pages/            # 笔记 / 知识库 / 对话 / 设置
│       ├── hooks/            # stores + 流式 / 健康检查
│       ├── layout/           # 侧边栏
│       └── utils/
└── README.md
```

## 开发约定

- 配置一律走 `backend/.env`，代码不出现硬编码密钥；`.env` / `node_modules` / `.venv` / `dist` / `backend/data/` 等均已 gitignore。
- `log/` 为本机开发日志，已 gitignore，不上传。

## License

[MIT](LICENSE)，开源自由使用。
