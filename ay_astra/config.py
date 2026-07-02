"""Configuration loader for AyAstra.

Beginner explanation:
Configuration means app settings.

For example:
- Which AI model should AyAstra use?
- What API key should it use?
- What API URL should it call?

We do not write secret API keys directly in Python files.
Later, we put them inside a private `.env` file.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Settings AyAstra needs for the optional AI brain."""

    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: int


def load_dotenv_file(path: str | Path = ".env") -> None:
    """Load settings from a local `.env` file if it exists.

    Example `.env` file:

    LLM_API_KEY=your_key_here
    LLM_MODEL=your_model_here
    LLM_BASE_URL=https://api.openai.com/v1
    """

    env_path = Path(path)

    if not env_path.exists():
        return

    lines = env_path.read_text(encoding="utf-8").splitlines()

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def _get_int_env(name: str, default: int) -> int:
    """Read an environment variable as a number."""

    value = os.getenv(name, "").strip()

    if not value:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def load_config() -> AppConfig:
    """Load AyAstra settings from `.env` and environment variables."""

    load_dotenv_file()

    return AppConfig(
        llm_api_key=os.getenv("LLM_API_KEY", "").strip(),
        llm_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/"),
        llm_model=os.getenv("LLM_MODEL", "").strip(),
        llm_timeout_seconds=_get_int_env("LLM_TIMEOUT_SECONDS", 30),
    )