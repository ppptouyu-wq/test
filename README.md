# 学生管理系统

前后端分离的学生信息管理示例：**Flask** 提供 REST API，**Vue 3 + Vite + Element Plus** 作为管理端界面。

数据库支持两种模式：

- **SQLite（默认）**：开箱即用，`backend/.env` 里默认 `DATABASE_URL=sqlite:///dev.db`
- **MySQL（可选）**：适合多端共享数据/更贴近生产；仓库提供 `deploy/docker-compose.yml` 一键启动

## 技术栈

- **后端**：Python、Flask、Flask-SQLAlchemy、Flask-Migrate（Alembic）
- **前端**：Vue 3、Vite、Axios、Element Plus
- **数据库**：SQLite（默认）/ MySQL（可选）

## 环境要求

- **Python 3.10+**（用于后端虚拟环境与依赖安装）
- **Node.js 20+** 与 **npm**（用于前端开发与构建）
- **Docker Desktop**（可选，仅当你要用 MySQL 时需要）

## 仓库结构

```
backend/    Flask API、数据模型、迁移脚本
frontend/   Vue 管理端（Vite 工程）
deploy/     MySQL 的 docker-compose 与初始化 SQL（可选）
```

### 1. 启动后端（Flask）

你可以把后端启动理解为两件事：

- **第一次运行**：装依赖 + **建表**（必须做一次）
- **之后每次运行**：直接启动服务即可（除非你改了数据模型）

在 `backend` 目录执行（PowerShell 窗口 1）：

```powershell
cd d:\workspace\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

准备环境变量（如果你已经有 `backend/.env`，确认 `DATABASE_URL` 后可跳过复制）：

```powershell
copy .env.example .env
notepad .env
```

#### 第一次运行：建表（推荐用迁移）

> 这一步做完后，SQLite 会生成 `backend/dev.db` 文件，并在里面创建表；若使用 MySQL，则会在 MySQL 中创建表。

```powershell
python manage.py db init
python manage.py db migrate -m "init"
python manage.py db upgrade
```

#### 启动后端服务（每次都要做）

```powershell
cd d:\workspace\backend
.\.venv\Scripts\Activate.ps1
python manage.py run -h 0.0.0.0 -p 5000
```

健康检查：`GET http://localhost:5000/api/health`

首次运行数据为 0 条是正常的（只建表不插数据）。可手动在页面新增；或在虚拟环境已激活、且已 `upgrade` 后执行演示数据写入：

```powershell
python manage.py seed-demo
```


### 2. 启动前端（Vue）

在另一个终端打开前端（PowerShell 窗口 2）。

注意：`package.json` 在 **`frontend`** 目录，不要在仓库根目录直接运行 `npm`。

```powershell
cd d:\workspace\frontend
copy .env.example .env
npm install
npm run dev
```

前端会读取 `VITE_API_BASE`，默认是 `http://localhost:5000`，需要与后端地址一致。

生产构建：

```powershell
cd d:\workspace\frontend
npm run build
```

产物在 `frontend/dist`。

#### 以后再启动（不改模型的情况下）

- **后端**：直接运行 `python manage.py run ...` 即可
- **前端**：直接运行 `npm run dev` 即可
- **只有当你修改了后端模型/字段** 才需要再次执行：

```powershell
python manage.py db migrate -m "xxx"
python manage.py db upgrade
```

> 如果执行 `Activate.ps1` 被策略阻止，可在当前用户范围放开：
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```



## 说明

- 后端更多命令与可选启动方式见 `backend/README.md`
- 请勿将包含真实密码的 `.env` 提交到版本库；仓库内仅保留 `.env.example` 作为模板
