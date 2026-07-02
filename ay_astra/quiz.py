"""Quiz Mode for AyAstra.

Beginner explanation:
Quiz Mode uses your saved learning log to ask study questions.
For now, it does not automatically grade answers like a human teacher would.
Instead, it helps you practise active recall: pulling knowledge from your brain
instead of just rereading notes.

Future upgrade:
When the optional AI brain is connected, AyAstra can grade answers and give
more detailed feedback.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ay_astra.storage.json_store import load_json
from ay_astra.tools.learning import LEARNING_LOG_PATH


@dataclass
class QuizSession:
    """In-memory quiz session.

    This resets when AyAstra closes. That is okay for now.
    """

    topic: str
    questions: list[str]
    learning_entry_id: int | None = None
    note: str = ""
    current_index: int = 0
    answers: list[dict[str, str]] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


_ACTIVE_QUIZ: QuizSession | None = None


def handle_quiz_command(message: str) -> str:
    """Route `/quiz` commands."""

    if message in {"/quiz", "/quiz help"}:
        return quiz_help()

    if message == "/quiz start":
        return start_quiz_from_learning_log()

    if message.startswith("/quiz topic "):
        topic = message.removeprefix("/quiz topic ").strip()
        return start_quiz_for_topic(topic)

    if message in {"/quiz current", "/quiz show"}:
        return show_current_question()

    if message.startswith("/quiz answer "):
        answer = message.removeprefix("/quiz answer ").strip()
        return answer_current_question(answer)

    if message == "/quiz stop":
        return stop_quiz()

    return "Quiz command not recognized. Try /quiz help."


def quiz_help() -> str:
    return """
Quiz Mode commands:
/quiz help                         Show this menu
/quiz start                        Start a quiz from your learning log
/quiz topic TOPIC                  Start a quiz on any topic
/quiz current                      Show the current question
/quiz answer YOUR ANSWER           Answer the current question
/quiz stop                         Stop the current quiz

Examples:
/quiz start
/quiz topic APIs
/quiz answer An API lets two programs communicate using agreed rules.
""".strip()


def start_quiz_from_learning_log() -> str:
    """Start a quiz using the weakest/oldest topic from the learning log."""

    entry = _choose_learning_entry()

    if not entry:
        return (
            "Your learning log is empty, so I cannot pick a topic yet.\n"
            "Add one first: /learn add APIs | Learned that APIs let apps talk to each other\n"
            "Then run: /quiz start"
        )

    topic = str(entry.get("topic") or "").strip()
    note = str(entry.get("note") or "").strip()
    entry_id = int(entry.get("id"))

    return _start_quiz(topic=topic, note=note, learning_entry_id=entry_id)


def start_quiz_for_topic(topic: str) -> str:
    """Start a quiz for any topic, even if it is not saved."""

    topic = topic.strip()

    if not topic:
        return "Give me a topic. Example: /quiz topic APIs"

    return _start_quiz(topic=topic, note="", learning_entry_id=None)


def show_current_question() -> str:
    """Show the active quiz question."""

    if _ACTIVE_QUIZ is None:
        return "No active quiz. Start one with /quiz start or /quiz topic TOPIC."

    return _format_current_question(_ACTIVE_QUIZ)


def answer_current_question(answer: str) -> str:
    """Save an answer and move to the next question."""

    global _ACTIVE_QUIZ

    if _ACTIVE_QUIZ is None:
        return "No active quiz. Start one with /quiz start or /quiz topic TOPIC."

    answer = answer.strip()

    if not answer:
        return "Give me your answer after the command. Example: /quiz answer An API lets apps talk."

    session = _ACTIVE_QUIZ
    question = session.questions[session.current_index]
    session.answers.append({"question": question, "answer": answer})
    session.current_index += 1

    if session.current_index >= len(session.questions):
        completed_session = session
        _ACTIVE_QUIZ = None
        return _quiz_finished_message(completed_session)

    return (
        "Answer saved. I am not grading automatically yet, but active recall is already doing the work.\n\n"
        + _format_current_question(session)
    )


def stop_quiz() -> str:
    """Stop the active quiz."""

    global _ACTIVE_QUIZ

    if _ACTIVE_QUIZ is None:
        return "No active quiz to stop. Very peaceful."

    stopped_topic = _ACTIVE_QUIZ.topic
    _ACTIVE_QUIZ = None
    return f"Quiz stopped for: {stopped_topic}. Tactical retreat accepted."


def _start_quiz(topic: str, note: str, learning_entry_id: int | None) -> str:
    global _ACTIVE_QUIZ

    questions = _build_questions(topic=topic, note=note)
    _ACTIVE_QUIZ = QuizSession(
        topic=topic,
        note=note,
        learning_entry_id=learning_entry_id,
        questions=questions,
    )

    source_text = (
        f"Learning log entry #{learning_entry_id}" if learning_entry_id is not None else "Custom topic"
    )

    lines = [
        f"Quiz started — {topic}",
        f"Source: {source_text}",
        "Mode: active recall practice",
        "",
    ]

    if note:
        lines.extend([f"Your saved note: {note}", ""])

    lines.append(_format_current_question(_ACTIVE_QUIZ))
    return "\n".join(lines).strip()


def _format_current_question(session: QuizSession) -> str:
    question_number = session.current_index + 1
    total_questions = len(session.questions)
    question = session.questions[session.current_index]

    return (
        f"Question {question_number}/{total_questions}:\n"
        f"{question}\n\n"
        "Reply with:\n"
        "/quiz answer YOUR ANSWER"
    )


def _quiz_finished_message(session: QuizSession) -> str:
    lines = [
        f"Quiz complete — {session.topic}",
        "",
        "Your answers were saved for this session:",
        "",
    ]

    for index, answer_data in enumerate(session.answers, start=1):
        lines.extend(
            [
                f"{index}. Q: {answer_data['question']}",
                f"   A: {answer_data['answer']}",
                "",
            ]
        )

    lines.extend(
        [
            "Self-check:",
            "- Could you explain it without reading notes?",
            "- Did you give a concrete example?",
            "- Do you know one common mistake?",
            "",
        ]
    )

    if session.learning_entry_id is not None:
        lines.append(f"If you reviewed it properly, mark it: /learn reviewed {session.learning_entry_id}")
    else:
        lines.append("If this is worth tracking, save it: /learn add TOPIC | NOTE")

    lines.append("AyAstra note: excellent. The brain grows by retrieval, not by staring at notes like they owe you money.")
    return "\n".join(lines).strip()


def _build_questions(topic: str, note: str) -> list[str]:
    questions = [
        f"Explain {topic} in your own words, as if teaching a first-year student.",
        f"Give one practical example of {topic}. If it is coding-related, describe or write a tiny code example.",
        f"What is one common mistake or confusion someone might have about {topic}?",
    ]

    if note:
        questions.insert(1, f"Your note says: '{note}'. Why does that matter?")

    return questions


def _choose_learning_entry() -> dict[str, Any] | None:
    entries = load_json(LEARNING_LOG_PATH, [])

    if not entries:
        return None

    valid_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("topic")]

    if not valid_entries:
        return None

    sorted_entries = sorted(
        valid_entries,
        key=lambda entry: (
            entry.get("times_reviewed", 0),
            entry.get("last_reviewed_at") or "",
            entry.get("created_at") or "",
        ),
    )

    return sorted_entries[0]
