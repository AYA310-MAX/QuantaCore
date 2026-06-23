"""Tiny JSON storage helper.

Beginner explanation:
JSON is a simple file format for storing data like lists and dictionaries.
We use it here so AyAstra can remember tasks and reminders between runs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def ensure_file(path: str | Path, default_value: Any) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        save_json(file_path, default_value)
    return file_path


def load_json(path: str | Path, default_value: Any) -> Any:
    file_path = ensure_file(path, default_value)
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If the file gets corrupted while learning, reset safely.
        save_json(file_path, default_value)
        return default_value


def save_json(path: str | Path, data: Any) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
