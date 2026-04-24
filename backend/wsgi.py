import os

from app import create_app


def _load_dotenv_if_present() -> None:
    # Optional: lets users run without exporting env vars
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    load_dotenv()


_load_dotenv_if_present()

app = create_app(os.getenv("FLASK_ENV", "development"))

