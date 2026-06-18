
# Evan Platform

> 一个可复用的 AI Agent / 管家平台后端骨架。

## 项目定位

`evan-platform` 是一个面向个人 AI 助理场景的后端平台，目标是提供：

- **会话与消息管理**（sessions / messages）
- **用户认证与多设备支持**（JWT）
- **长期记忆与用户画像**（memories，后续接入）
- **任务与日程**（tasks / events，后续接入）
- **工具调用与审计**（tool_runs，后续接入）
- **多模型适配**（ChatAnywhere / OpenAI / Ollama）

多端客户端（Web / Electron / 未来耳机设备）通过统一 API 与平台交互。

---

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 后端框架 | Flask 3.0 |
| ORM / 数据库 | SQLAlchemy + Flask-Migrate（开发用 SQLite，生产用 PostgreSQL） |
| 认证 | Flask-JWT-Extended（access token + refresh token） |
| 前端 | Vue 3（待接入） |
| 桌面端 | Electron（待接入） |
| 网关 | Caddy（HTTPS + Basic Auth + 反向代理） |
| 进程管理 | Gunicorn（生产环境） |

---

## 项目结构

```
evan-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # create_app 应用工厂
│   │   ├── config.py            # 配置（dev / prod / testing）
│   │   ├── extensions.py        # 扩展初始化（db / jwt / cors）
│   │   ├── common/              # 平台通用模块（可跨项目复用）
│   │   │   ├── errors.py        #   统一错误码 + AppError 异常
│   │   │   ├── resp.py          #   统一响应格式 ok() / fail()
│   │   │   ├── trace.py         #   请求级 trace_id
│   │   │   └── logging.py       #   结构化日志
│   │   ├── models/              # SQLAlchemy 数据模型
│   │   │   └── user.py          #   User 模型
│   │   ├── services/            # 业务逻辑层
│   │   │   └── auth_service.py  #   认证服务
│   │   ├── api/                 # API 蓝图（路由层）
│   │   │   ├── health.py        #   健康检查
│   │   │   └── auth.py          #   认证接口
│   │   └── utils/               # 工具函数
│   │       └── decorators.py    #   通用装饰器
│   ├── migrations/              # 数据库迁移（Alembic）
│   ├── scripts/
│   │   └── init_user.py         # 首次部署：创建管理员
│   ├── tests/                   # 测试（预留）
│   ├── requirements.txt
│   ├── .env.example             # 环境变量模板
│   ├── .flaskenv                # Flask CLI 配置
│   └── wsgi.py                  # WSGI 入口（Gunicorn 用）
├── frontend/                    # Vue 3 前端（待接入）
├── desktop/                     # Electron 桌面端（待接入）
└── README.md
```

### 分层架构

```
请求 → API 层（参数校验）→ Service 层（业务逻辑）→ Model 层（数据访问）→ 数据库
         ↑                                              ↓
     统一响应 ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

- **API 层**：只做参数校验和调用 service，不写业务逻辑
- **Service 层**：业务编排，可被 API / CLI / 定时任务复用
- **Model 层**：数据定义与查询封装
- **Common 层**：统一响应、错误码、trace、日志，与业务无关

---

## 快速开始

### 环境要求

- Python 3.10+
- pip

### 1. 克隆仓库

```bash
git https://github.com/six-feet-under-0122/evan-platform.git
cd evan-platform/backend
```

### 2. 创建虚拟环境

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，至少修改以下两项：

```bash
SECRET_KEY=<随机字符串>
JWT_SECRET_KEY=<另一个随机字符串>
```

生成随机密钥：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. 初始化数据库

```bash
# 初始化迁移系统（仅首次）
flask db init

# 生成迁移
flask db migrate -m "create users table"

# 应用迁移
flask db upgrade
```

### 6. 创建管理员用户

```bash
# 方法 1：交互式 CLI
flask create-user

# 方法 2：脚本
python scripts/init_user.py
```

### 7. 启动开发服务器

```bash
python wsgi.py
# 或
flask run --host=0.0.0.0 --port=5000
```

服务器运行在 `http://localhost:5000`

---

## API 文档

### 统一响应格式

所有接口返回统一结构：

**成功**：
```json
{
  "ok": true,
  "data": { ... },
  "message": "Success",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**失败**：
```json
{
  "ok": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid username or password"
  },
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 当前可用接口

#### 健康检查

| 方法 | 路径 | 鉴权 | 说明 |
| --- | --- | --- | --- |
| GET | `/api/health` | ✗ | 基础健康检查 |
| GET | `/api/health/db` | ✗ | 数据库连通性检查 |

#### 认证

| 方法 | 路径 | 鉴权 | 说明 |
| --- | --- | --- | --- |
| POST | `/api/auth/login` | ✗ | 登录，获取 token |
| POST | `/api/auth/refresh` | refresh token | 刷新 access token |
| GET | `/api/auth/me` | access token | 获取当前用户信息 |
| POST | `/api/auth/logout` | access token | 登出（占位） |

##### POST /api/auth/login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

响应：
```json
{
  "ok": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {
      "id": "uuid",
      "username": "admin",
      "role": "admin",
      "display_name": "Admin",
      "is_active": true,
      "created_at": "2026-06-11T06:00:00",
      "last_login_at": "2026-06-11T06:31:00"
    }
  },
  "message": "Login successful",
  "trace_id": "..."
}
```

##### GET /api/auth/me

```bash
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer <access_token>"
```

##### POST /api/auth/refresh

```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

## CLI 命令

```bash
# 创建用户（交互式）
flask create-user

# 列出所有用户
flask list-users

# 数据库迁移
flask db migrate -m "描述"
flask db upgrade
flask db downgrade
```

---

## 部署

### 生产环境部署

```bash
# 1. 安装 Gunicorn
pip install gunicorn

# 2. 设置环境变量
export FLASK_ENV=production

# 3. 启动（4 个 worker 进程）
gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app
```

### Caddy 反向代理（推荐）

```
api.yourdomain.com {
    basicauth {
        admin $2a$14$...   # caddy hash-password 生成
    }
    reverse_proxy 127.0.0.1:8000
}
```

链路：`客户端 → Caddy (HTTPS + Basic Auth) → Gunicorn → Flask`

---

## 开发路线

### Week 1 ✅ 工程化骨架
- [x] 应用工厂模式（create_app）
- [x] 配置分环境（dev / prod / testing）
- [x] SQLAlchemy + Flask-Migrate
- [x] 统一响应格式 + 错误码
- [x] trace_id + 结构化日志
- [x] JWT 认证（login / refresh / me）
- [x] User 模型 + CLI 创建用户

### Week 2 🔲 核心业务
- [ ] Session 模型 + CRUD API
- [ ] Message 模型（content_json blocks 结构）
- [ ] File 模型 + 图片上传
- [ ] ChatService（非流式）
- [ ] LLM Provider 适配层（ChatAnywhere）

### Week 3 🔲 上线与可观测性
- [ ] VPS + Caddy + Gunicorn 部署
- [ ] ToolRun 模型（LLM 调用审计）
- [ ] SSE 流式输出
- [ ] PostgreSQL 迁移（可选）

### 后续 🔲
- [ ] 长期记忆（memories）
- [ ] Dynamic Rule Formation（规则提炼与执行）
- [ ] 任务与日程（tasks / events）
- [ ] Ollama 本地模型接入
- [ ] 设备控制（家电 / 灯光）

---

## License

Private project. All rights reserved.



