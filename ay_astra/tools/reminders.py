"""Reminder manager tool for AyAstra."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ay_astra.storage.json_store import load_json, save_json

REMINDERS_PATH = Path("data/reminders.json")
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def _load_reminders() -> list[dict]:
    return load_json(REMINDERS_PATH, [])


def _save_reminders(reminders: list[dict]) -> None:
    save_json(REMINDERS_PATH, reminders)


def add_reminder(date_time_text: str, message: str) -> str:
    message = message.strip()
    if not message:
        return "Reminder message missing. Even futuristic assistants need details."

    try:
        remind_at = datetime.strptime(date_time_text.strip(), DATETIME_FORMAT)
    except ValueError:
        return "Use this format: /remind add YYYY-MM-DD HH:MM MESSAGE. Example: /remind add 2026-06-14 18:00 Study AI agents"

    reminders = _load_reminders()
    next_id = 1 if not reminders else max(reminder["id"] for reminder in reminders) + 1
    reminders.append(
        {
            "id": next_id,
            "message": message,
            "remind_at": remind_at.isoformat(timespec="minutes"),
            "delivered": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    _save_reminders(reminders)
    return f"Reminder #{next_id} set for {remind_at.strftime('%Y-%m-%d %H:%M')}. I will keep an eye on it while this app is running."


def list_reminders() -> str:
    reminders = _load_reminders()
    if not reminders:
        return "No reminders yet. Your timeline is clean. Suspicious, but clean."

    lines = ["Your reminders:"]
    for reminder in reminders:
        status = "✅ delivered" if reminder["delivered"] else "⏰ pending"
        lines.append(f"{status} #{reminder['id']}: {reminder['remind_at']} — {reminder['message']}")
    return "\n".join(lines)


def get_due_reminders() -> list[str]:
    """Return messages for reminders that are due and mark them delivered.

    This only checks reminders while the app is running. Later, we can connect OS notifications.
    """
    reminders = _load_reminders()
    now = datetime.now()
    due_messages: list[str] = []
    changed = False

    for reminder in reminders:
        if reminder["delivered"]:
            continue
        remind_at = datetime.fromisoformat(reminder["remind_at"])
        if remind_at <= now:
            reminder["delivered"] = True
            due_messages.append(f"Reminder #{reminder['id']}: {reminder['message']}")
            changed = True

    if changed:
        _save_reminders(reminders)

    return due_messages
