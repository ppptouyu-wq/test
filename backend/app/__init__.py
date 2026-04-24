from __future__ import annotations

from datetime import date

import click
from flask import Flask, jsonify

from .config import get_config
from .extensions import cors, db, migrate
from .routes import api_bp


def create_app(env_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env_name))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Ensure models are registered for migrations / create_all
    from . import models  # noqa: F401

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})

    @app.cli.command("seed-demo")
    def seed_demo_command():
        """若学生表为空，则写入几条演示数据（便于本地看列表效果）。"""
        from .extensions import db
        from .models import Student

        with app.app_context():
            if Student.query.first() is not None:
                click.echo("已有学生数据，跳过 seed-demo。")
                return
            samples = [
                Student(
                    student_no="2026001",
                    name="张三",
                    gender="男",
                    birth_date=date(2008, 3, 12),
                    grade="初二",
                    class_name="2班",
                    phone="13800000001",
                ),
                Student(
                    student_no="2026002",
                    name="李四",
                    gender="女",
                    birth_date=date(2008, 7, 21),
                    grade="初二",
                    class_name="1班",
                    phone="13800000002",
                ),
                Student(
                    student_no="2026003",
                    name="王五",
                    gender="男",
                    birth_date=date(2007, 11, 5),
                    grade="初三",
                    class_name="3班",
                    phone="13800000003",
                ),
            ]
            db.session.add_all(samples)
            db.session.commit()
            click.echo(f"已写入 {len(samples)} 条演示数据。")

    return app

