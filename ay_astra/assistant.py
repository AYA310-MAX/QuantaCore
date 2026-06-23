"""Command router for AyAstra.

Beginner explanation:
This file decides what to do with the user's message.
If the message starts with /task, it sends it to the task tool.
If it starts with /tutor, it gives a learning-style explanation.
Later, this router will decide when to call an LLM, web search, news APIs, or smart-home APIs.
"""

from __future__ import annotations

from ay_astra.personality import style_reply
from ay_astra.tools.reminders import add_reminder, list_reminders
from ay_astra.tools.tasks import add_task, complete_task, list_tasks

HELP_TEXT = """
Commands available:
/help                         Show this help menu
/exit                         Close AyAstra
/tutor TOPIC                  Explain a topic beginner-style
/task add DESCRIPTION         Add a task
/task list                    List tasks
/task done TASK_ID            Mark a task complete
/remind add YYYY-MM-DD HH:MM MESSAGE
/remind list                  List reminders
/news TOPIC                   Future verified news mode placeholder
/research TOPIC               Future source-based research mode placeholder

Examples:
/task add Finish software engineering assignment
/remind add 2026-06-14 18:00 Review AI agents notes
/tutor APIs
""".strip()


def handle_message(message: str) -> str:
    message = message.strip()

    if not message:
        return style_reply("I received silence. Very mysterious. Type /help if you need commands.")

    if message.lower() in {"/help", "help"}:
        return style_reply(HELP_TEXT)

    if message.lower() in {"/exit", "exit", "quit"}:
        return "__EXIT__"

    if message.startswith("/task"):
        return style_reply(_handle_task(message))

    if message.startswith("/remind"):
        return style_reply(_handle_reminder(message))

    if message.startswith("/tutor"):
        topic = message.removeprefix("/tutor").strip()
        return style_reply(_tutor_mode(topic))

    if message.startswith("/news"):
        topic = message.removeprefix("/news").strip() or "technology"
        return style_reply(_news_mode_placeholder(topic))

    if message.startswith("/research"):
        topic = message.removeprefix("/research").strip()
        return style_reply(_research_mode_placeholder(topic))

    return style_reply(_basic_chat(message))


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

    return f"""
Alright Ayanda, lab coat on. Let's simplify **{topic}**.

1. Simple idea:
   {topic} is a concept we can break into smaller parts instead of trying to swallow the textbook whole like a stressed student before exams.

2. How we will study it:
   - Define it in plain English.
   - Look at one real example.
   - Write a tiny code/example if relevant.
   - Test your understanding with a mini quiz.

3. Your next move:
   Ask: "explain {topic} with an example" or "quiz me on {topic}".

Note: In the next sprint, we will connect an LLM so Tutor Mode can generate deeper explanations dynamically.
""".strip()


def _news_mode_placeholder(topic: str) -> str:
    return f"""
News mode requested for: {topic}

Truth protocol active: I will not invent live news.
This starter app does not have a news/search API connected yet, so I cannot verify current updates from inside the program.

Future version will return:
- headline
- short summary
- why it matters
- source link
- publication date

For now: we need to connect a verified news/search source in the next sprint. No hallucinations in this lab.
""".strip()


def _research_mode_placeholder(topic: str) -> str:
    if not topic:
        return "Give me a research topic. Example: /research AI agents in education"

    return f"""
Research mode requested for: {topic}

Truth protocol active: I need source tools before giving source-backed research answers.
Future Research Mode will:
- find reliable sources
- summarize them
- explain key terms
- separate facts from interpretation
- cite every important claim
- help you understand the research like a patient tutor with better lighting

For now, I will not pretend to have verified sources. Shiny confidence without evidence is just decoration.
""".strip()


def _basic_chat(message: str) -> str:
    lower = message.lower()

    if "hello" in lower or "hi" in lower:
        return "Hello Ayanda. QuantaCore is awake. What are we building, learning, or avoiding today?"

    if "what can you do" in lower:
        return "I can manage simple tasks/reminders and guide learning basics right now. Use /help. Soon: LLM conversation, verified news, research mode, voice, and smart-home control. Step by step — we are not building Wakanda in one afternoon."

    return "I hear you. For now I understand commands best. Type /help to see my current tools. Soon we connect the bigger brain."
