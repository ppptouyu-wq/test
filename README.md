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
## 运行效果截图
### 首页
会显示一些关键信息与快捷入口
<img width="1860" height="883" alt="11f982d5ac58eb96519805d045d719e7" src="https://github.com/user-attachments/assets/e2749372-1ebe-4e29-a5ee-07ad2df255cd" />
### 学生档案
会显示已经添加的学生档案信息，并且可以查询和新增学生信息
<img width="1860" height="883" alt="9f6cc08e2e9d0aedf57f36935eae8825" src="https://github.com/user-attachments/assets/79ffe579-b54d-4e84-b242-306c84ae9595" />
<img width="1860" height="883" alt="609af4222dbe3c3386ac10057edc8001" src="https://github.com/user-attachments/assets/b5b79d46-8b20-4797-a249-f618706bb34c" />
<img width="1860" height="883" alt="3dcec4fac86f92341435fd26e2d7bba3" src="https://github.com/user-attachments/assets/bb37aa03-188f-410b-8775-3415caeb7c9d" />
### 班级概览
根据年级和班级会显示每个班的人数，并且可以查看该班有多少学生  
<img width="1860" height="883" alt="ef5698231e76d3bc5b5f1a65aa10e9ca" src="https://github.com/user-attachments/assets/9247cc16-82c3-4bbc-90cd-1069179b18a0" />
### 关于系统
显示这个简单系统所用到的技术，可以一键检查后端是否连接成功
<img width="1860" height="883" alt="5a53ac6b78b1cd1ff3359a9cc3e2468c" src="https://github.com/user-attachments/assets/4f71ad70-64de-4e6b-9966-7318b014479a" />


### 

## 说明

- 后端更多命令与可选启动方式见 `backend/README.md`
- 请勿将包含真实密码的 `.env` 提交到版本库；仓库内仅保留 `.env.example` 作为模板
