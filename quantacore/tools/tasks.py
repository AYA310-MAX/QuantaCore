"""Task manager tool for AyAstra."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from quantacore.storage.json_store import load_json, save_json

TASKS_PATH = Path("data/tasks.json")


def _load_tasks() -> list[dict]:
    return load_json(TASKS_PATH, [])


def _save_tasks(tasks: list[dict]) -> None:
    save_json(TASKS_PATH, tasks)


def add_task(description: str) -> str:
    description = description.strip()
    if not description:
        return "Give me the task description, genius. I cannot schedule invisible homework."

    tasks = _load_tasks()
    next_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    task = {
        "id": next_id,
        "description": description,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "completed_at": None,
    }
    tasks.append(task)
    _save_tasks(tasks)
    return f"Task logged as #{next_id}. Future-you owes present-you a thank you."


def list_tasks() -> str:
    tasks = _load_tasks()
    if not tasks:
        return "No tasks yet. Suspiciously peaceful. Add one with /task add DESCRIPTION."

    lines = ["Here are your tasks, Ayanda:"]
    for task in tasks:
        status = "✅" if task["done"] else "⬜"
        lines.append(f"{status} #{task['id']}: {task['description']}")
    return "\n".join(lines)


def complete_task(task_id_text: str) -> str:
    try:
        task_id = int(task_id_text.strip())
    except ValueError:
        return "Task ID must be a number. The lab requires precision, Ayanda."

    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                return f"Task #{task_id} was already complete. Efficient. Almost suspicious."
            task["done"] = True
            task["completed_at"] = datetime.now().isoformat(timespec="seconds")
            _save_tasks(tasks)
            return f"Task #{task_id} complete. Tiny victory logged."

    return f"I could not find task #{task_id}. Either it escaped, or the ID is wrong."
