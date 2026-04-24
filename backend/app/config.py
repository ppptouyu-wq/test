from __future__ import annotations

import os


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # Comma-separated list also supported
    _cors = os.getenv("CORS_ORIGINS", "*")
    if "," in _cors:
        CORS_ORIGINS = [x.strip() for x in _cors.split(",") if x.strip()]
    else:
        CORS_ORIGINS = _cors


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


def get_config(env_name: str | None):
    name = (env_name or os.getenv("FLASK_ENV") or "development").lower()
    if name in ("prod", "production"):
        return ProductionConfig
    return DevelopmentConfig

