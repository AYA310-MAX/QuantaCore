"""Learning log tool for AyAstra.

Beginner explanation:
This tool helps Ayanda track topics studied over time.
It stores learning items in `data/learning_log.json` so they remain saved after
AyAstra closes.

This is different from short-term chat memory:
- Short-term memory disappears when the app closes.
- Learning log entries are saved in a JSON file.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ay_astra.storage.json_store import load_json, save_json

LEARNING_LOG_PATH = Path("data/learning_log.json")


def learning_help() -> str:
    return """
Learning Log commands:
/learn add TOPIC                         Save a topic you studied
/learn add TOPIC | NOTE                  Save a topic with a note
/learn list                              List saved learning topics
/learn review                            Show topics to review
/learn reviewed ID                       Mark a topic as reviewed
/learn help                              Show this menu

Examples:
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes
/learn list
/learn review
/learn reviewed 1
""".strip()


def add_learning_topic(raw_text: str) -> str:
    """Add a topic to the learning log."""

    topic, note = _split_topic_and_note(raw_text)

    if not topic:
        return "Give me a topic to log. Example: /learn add APIs | Learned what endpoints are."

    entries = _load_entries()
    next_id = 1 if not entries else max(entry["id"] for entry in entries) + 1

    entry = {
        "id": next_id,
        "topic": topic,
        "note": note,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "times_reviewed": 0,
        "last_reviewed_at": None,
    }

    entries.append(entry)
    _save_entries(entries)

    if note:
        return f"Learning topic #{next_id} logged: {topic}. Note saved. Your future brain says thank you."

    return f"Learning topic #{next_id} logged: {topic}. Small knowledge crystal added to the archive."


def list_learning_topics() -> str:
    """List all learning log entries."""

    entries = _load_entries()

    if not entries:
        return "Your learning log is empty. Add one with /learn add TOPIC. The archive awaits, scholar."

    lines = ["Learning Log:", ""]

    for entry in entries:
        note = entry.get("note") or "no note"
        last_reviewed = entry.get("last_reviewed_at") or "never"
        lines.extend(
            [
                f"#{entry['id']}: {entry['topic']}",
                f"   Note: {note}",
                f"   Reviews: {entry.get('times_reviewed', 0)}",
                f"   Last reviewed: {last_reviewed}",
                "",
            ]
        )

    return "\n".join(lines).strip()


def review_learning_topics(limit: int = 3) -> str:
    """Show topics that should be reviewed."""

    entries = _load_entries()

    if not entries:
        return "No learning topics to review yet. Add one with /learn add TOPIC."

    sorted_entries = sorted(
        entries,
        key=lambda entry: (
            entry.get("times_reviewed", 0),
            entry.get("last_reviewed_at") or "",
            entry.get("created_at") or "",
        ),
    )

    selected_entries = sorted_entries[:limit]

    lines = [
        "Review Queue:",
        "",
        "AyAstra strategy: review weak/older topics first. We are not memorising by vibes only.",
        "",
    ]

    for entry in selected_entries:
        note = entry.get("note") or "no note saved"
        lines.extend(
            [
                f"#{entry['id']}: {entry['topic']}",
                f"   Note: {note}",
                f"   Reviews so far: {entry.get('times_reviewed', 0)}",
                f"   Try now: /tutor {entry['topic']}",
                f"   After reviewing: /learn reviewed {entry['id']}",
                "",
            ]
        )

    lines.extend(
        [
            "Mini review method:",
            "1. Explain the topic out loud in simple words.",
            "2. Give one example.",
            "3. Ask AyAstra to quiz you.",
            "4. Mark it reviewed.",
        ]
    )

    return "\n".join(lines).strip()


def mark_learning_reviewed(entry_id_text: str) -> str:
    """Mark a learning entry as reviewed."""

    try:
        entry_id = int(entry_id_text.strip())
    except ValueError:
        return "Learning log ID must be a number. Example: /learn reviewed 1"

    entries = _load_entries()

    for entry in entries:
        if entry["id"] == entry_id:
            entry["times_reviewed"] = entry.get("times_reviewed", 0) + 1
            entry["last_reviewed_at"] = datetime.now().isoformat(timespec="seconds")
            _save_entries(entries)
            return (
                f"Marked #{entry_id} as reviewed: {entry['topic']}. "
                "Repetition logged. Neural pathways doing push-ups."
            )

    return f"I could not find learning topic #{entry_id}. Check /learn list."


def handle_learning_command(message: str) -> str:
    """Route `/learn` commands to the correct learning-log function."""

    if message in {"/learn", "/learn help"}:
        return learning_help()

    if message.startswith("/learn add "):
        raw_text = message.removeprefix("/learn add ").strip()
        return add_learning_topic(raw_text)

    if message == "/learn list":
        return list_learning_topics()

    if message == "/learn review":
        return review_learning_topics()

    if message.startswith("/learn reviewed "):
        entry_id_text = message.removeprefix("/learn reviewed ").strip()
        return mark_learning_reviewed(entry_id_text)

    return "Learning command not recognized. Try /learn help."


def _split_topic_and_note(raw_text: str) -> tuple[str, str]:
    """Split `TOPIC | NOTE` into topic and note."""

    if "|" not in raw_text:
        return raw_text.strip(), ""

    topic, note = raw_text.split("|", 1)
    return topic.strip(), note.strip()


def _load_entries() -> list[dict]:
    return load_json(LEARNING_LOG_PATH, [])


def _save_entries(entries: list[dict]) -> None:
    save_json(LEARNING_LOG_PATH, entries)
