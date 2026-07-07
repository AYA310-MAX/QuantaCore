"""Command router for AyAstra.

Beginner explanation:
This file decides what to do with the user's message.
If the message starts with /task, it sends it to the task tool.
If it starts with /tutor, it sends it to Tutor Mode.
If it is normal conversation, it can use AyAstra's optional AI brain.
Later, this router will decide when to call web search, news APIs, or smart-home APIs.
"""

from __future__ import annotations

from ay_astra.brain import AIBrain
from ay_astra.personality import style_reply
from ay_astra.tools.learning import handle_learning_command
from ay_astra.tools.news import get_news_brief
from ay_astra.tools.quiz import handle_quiz_command
from ay_astra.tools.reminders import add_reminder, list_reminders
from ay_astra.tools.voice import handle_voice_command
from ay_astra.tools.research import get_research_brief
from ay_astra.tools.tasks import add_task, complete_task, list_tasks

HELP_TEXT = """
Commands available:
/help                         Show this help menu
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
/ui                           Show how to launch the Siri-like assistant UI
/voice status                 Check voice output setup
/voice on                     Turn voice output on for this session
/voice off                    Turn voice output off
/voice test                   Speak a short test line
/tutor TOPIC                  Explain a topic beginner-style
/learn add TOPIC | NOTE       Save something you studied
/learn list                   List saved learning topics
/learn review                 Show topics to review
/learn reviewed ID            Mark a topic as reviewed
/quiz start                   Start a quiz from your learning log
/quiz topic TOPIC             Start a quiz on any topic
/quiz current                 Show the current quiz question
/quiz answer YOUR ANSWER      Answer the current quiz question
/quiz feedback                Get feedback on your last completed quiz
/quiz stop                    Stop the current quiz
/task add DESCRIPTION         Add a task
/task list                    List tasks
/task done TASK_ID            Mark a task complete
/remind add YYYY-MM-DD HH:MM MESSAGE
/remind list                  List reminders
/news TOPIC                   Fetch source-backed headlines from verified RSS feeds
/news sources                 List configured news feeds
/research TOPIC               Search academic paper metadata with source links
/research sources             Show configured research sources

Examples:
/task add Finish software engineering assignment
/remind add 2026-07-02 18:00 Review AI agents notes
/tutor APIs
/learn add APIs | Learned that APIs let apps talk to each other
/quiz start
/voice status
/research AI agents in education
/brain status
""".strip()

# This is short-term memory. It resets when you close the program.
# Later, we can add long-term memory with a database.
_SESSION_HISTORY: list[dict[str, str]] = []
_BRAIN = AIBrain()


def handle_message(message: str) -> str:
    message = message.strip()

    if not message:
        return style_reply("I received silence. Very mysterious. Type /help if you need commands.")

    lower_message = message.lower()

    if lower_message in {"/help", "help"}:
        return style_reply(HELP_TEXT)

    if lower_message in {"/exit", "exit", "quit"}:
        return "__EXIT__"

    if lower_message == "/brain status":
        return style_reply(_BRAIN.status_text())

    if lower_message == "/memory clear":
        _SESSION_HISTORY.clear()
        return style_reply("Session memory cleared. Fresh lab board, fewer fingerprints.")

    if lower_message == "/ui":
        return style_reply(_ui_instructions())

    if message.startswith("/voice"):
        return style_reply(handle_voice_command(message))

    if message.startswith("/task"):
        return style_reply(_handle_task(message))

    if message.startswith("/remind"):
        return style_reply(_handle_reminder(message))

    if message.startswith("/tutor"):
        topic = message.removeprefix("/tutor").strip()
        return style_reply(_tutor_mode(topic))

    if message.startswith("/learn"):
        return style_reply(handle_learning_command(message))

    if message.startswith("/quiz"):
        return style_reply(handle_quiz_command(message))

    if message.startswith("/news"):
        topic = message.removeprefix("/news").strip() or "technology"
        return style_reply(get_news_brief(topic))

    if message.startswith("/research"):
        topic = message.removeprefix("/research").strip()
        return style_reply(get_research_brief(topic))

    if _looks_like_live_or_recent_info_request(message):
        return style_reply(_needs_verified_sources_message(message))

    return style_reply(_basic_chat(message))


def _ui_instructions() -> str:
    return """
AyAstra's focused LLM-style assistant UI is a separate local web app.

To launch it:
1. Exit terminal AyAstra with /exit.
2. In the same terminal, run: python assistant_ui.py
3. Open this address in your browser: http://127.0.0.1:8765

This UI has AyAstra at the top, a greeting/motivational prompt, a large ask box, and quick action chips.
It runs locally on your computer. Very private. Very lab-coded.
""".strip()


def _handle_task(message: str) -> str:
    if message.startswith("/task add "):
        description = message.removeprefix("/task add ")
        return add_task(description)

    if message == "/task list":
        return list_tasks()

    if message.startswith("/task done "):
        task_id = message.removeprefix("/task done ")
        return complete_task(task_id)

    return "Task command not recognized. Try /task add DESCRIPTION, /task list, or /task done TASK_ID."


def _handle_reminder(message: str) -> str:
    if message == "/remind list":
        return list_reminders()

    if message.startswith("/remind add "):
        rest = message.removeprefix("/remind add ").strip()
        parts = rest.split(maxsplit=2)
        if len(parts) < 3:
            return "Use: /remind add YYYY-MM-DD HH:MM MESSAGE"
        date_time_text = f"{parts[0]} {parts[1]}"
        reminder_message = parts[2]
        return add_reminder(date_time_text, reminder_message)

    return "Reminder command not recognized. Try /remind add YYYY-MM-DD HH:MM MESSAGE or /remind list."


def _tutor_mode(topic: str) -> str:
    if not topic:
        return "Tell me what to teach. Example: /tutor APIs"

    reply = _BRAIN.generate(topic, mode="tutor", history=_SESSION_HISTORY)
    _remember("user", f"Tutor request: {topic}")
    _remember("assistant", reply.text)
    return reply.text


def _basic_chat(message: str) -> str:
    lower = message.lower()

    if "hello" in lower or "hi" in lower:
        greeting = "Hello Ayanda. QuantaCore is awake. What are we building, learning, or avoiding today?"
        _remember("user", message)
        _remember("assistant", greeting)
        return greeting

    reply = _BRAIN.generate(message, mode="chat", history=_SESSION_HISTORY)
    _remember("user", message)
    _remember("assistant", reply.text)
    return reply.text


def _remember(role: str, content: str) -> None:
    """Store a message in short-term memory for this session only."""

    if role not in {"user", "assistant"}:
        return

    _SESSION_HISTORY.append({"role": role, "content": content})

    # Keep memory small and beginner-friendly.
    del _SESSION_HISTORY[:-12]


def _looks_like_live_or_recent_info_request(message: str) -> bool:
    """Catch obvious current-info requests before they reach the LLM.

    This helps enforce AyAstra's no-hallucination rule.
    """

    text = message.lower()
    live_phrases = [
        "latest",
        "news",
        "today",
        "right now",
        "currently happening",
        "recent updates",
        "what happened",
        "this week",
        "this month",
        "new release",
        "just released",
    ]
    return any(phrase in text for phrase in live_phrases)


def _needs_verified_sources_message(message: str) -> str:
    return f"""
That sounds like it may need current or verified sources:
"{message}"

Truth protocol says I should not answer that from memory alone.
Use `/news TOPIC` for live updates or `/research TOPIC` for source-backed research once those tools are connected.

For now, I can help explain stable concepts, code, and study topics — but I will not freestyle facts from the digital mist.
""".strip()
