# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint

This starter version is deliberately simple:

- Runs in the terminal.
- Uses an AyAstra personality style.
- Supports basic task commands.
- Supports basic reminder commands.
- Includes tutor/research/news placeholders with a strict no-hallucination rule.

No real LLM or news API is connected yet. That is intentional: AyAstra must not pretend to know live facts until source tools are connected.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/tutor TOPIC                  Explain a topic beginner-style
/task add DESCRIPTION         Add a task
/task list                    List tasks
/task done TASK_ID            Mark a task complete
/remind add YYYY-MM-DD HH:MM MESSAGE
/remind list                  List reminders
/news TOPIC                   Placeholder for future verified news
/research TOPIC               Placeholder for future source-based research mode
```

## Example

```text
You: /task add Finish AI assignment
AyAstra: Task logged. Future-you owes present-you a thank you.

You: /tutor APIs
AyAstra: Alright Ayanda, lab coat on. Let's simplify APIs...
```

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.
