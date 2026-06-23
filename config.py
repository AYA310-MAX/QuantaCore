"""Configuration loader for AyAstra.

Beginner explanation:
Configuration means "settings the app can read without hard-coding them".
For example, API keys should never be written directly inside Python files.
Instead, we put them in a private `.env` file on your computer.

This file includes a tiny `.env` loader so the project does not need extra
packages just to read environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Settings AyAstra needs to know about."""

    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: int


def load_dotenv_file(path: str | Path = ".env") -> None:
    """Load KEY=VALUE pairs from a local .env file into environment variables.

    This is a small beginner-friendly alternative to the `python-dotenv` package.
    It ignores blank lines and comments. Existing environment variables win.
    """

    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def load_config() -> AppConfig:
    """Load AyAstra's settings from `.env` and environment variables."""

    load_dotenv_file()

    return AppConfig(
        llm_api_key=os.getenv("LLM_API_KEY", "").strip(),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/"),
        llm_model=os.getenv("LLM_MODEL", "").strip(),
        llm_timeout_seconds=_get_int_env("LLM_TIMEOUT_SECONDS", 30),
    )

