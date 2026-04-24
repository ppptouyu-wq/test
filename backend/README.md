# 学生管理系统（Flask 后端）

## 运行前准备

- 安装 Python 3.10+（推荐 3.11/3.12）
- 准备 MySQL（推荐直接用根目录 `deploy/docker-compose.yml`）

## 启动步骤（Windows PowerShell）

在 `d:\workspace\backend`：

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 复制并编辑环境变量
copy .env.example .env

# 初始化数据库表（两种方式二选一）
# 方式 A：用 migrate（推荐）
python manage.py db init
python manage.py db migrate -m "init"
python manage.py db upgrade

# 方式 B：不用 migrate（快速），直接在交互式里 create_all
# python -c "from wsgi import app; from app.extensions import db; app.app_context().push(); db.create_all(); print('ok')"

# 启动
python manage.py run -h 0.0.0.0 -p 5000
```

## API

- `GET /api/health`
- `GET /api/students?page=1&page_size=10&q=关键词&grade=年级&class_name=班级`
- `GET /api/students/:id`
- `POST /api/students`
- `PUT /api/students/:id`
- `DELETE /api/students/:id`

