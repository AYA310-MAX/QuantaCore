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

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 5 — Learning Log

This version:

- Runs in the terminal.
- Uses an AyAstra personality style.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Saves learning topics to a long-term JSON learning log.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar and Crossref fallback.

If no LLM API is configured, AyAstra still runs with local fallback replies. No panic. The lab lights stay on.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Optional: connect the AI brain

1. Copy `.env.example` to a new private file called `.env`.
2. Fill in your LLM settings:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

3. Run AyAstra:

```bash
python main.py
```

4. Inside AyAstra, check:

```text
/brain status
```

Important: never commit `.env` to GitHub. API keys are private.

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
/tutor TOPIC                  Explain a topic beginner-style
/learn add TOPIC | NOTE       Save something you studied
/learn list                   List saved learning topics
/learn review                 Show topics to review
/learn reviewed ID            Mark a topic as reviewed
/task add DESCRIPTION         Add a task
/task list                    List tasks
/task done TASK_ID            Mark a task complete
/remind add YYYY-MM-DD HH:MM MESSAGE
/remind list                  List reminders
/news TOPIC                   Fetch source-backed headlines from verified RSS feeds
/news sources                 List configured news feeds
/research TOPIC               Search academic paper metadata with source links
/research sources             Show configured research sources
```

## Learning log examples

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

Learning log entries are saved in:

```text
data/learning_log.json
```

## News examples

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

News output includes:

```text
headline
source feed name
publication date from feed
summary from feed
article link
```

## Research examples

```text
/research AI agents in education
/research CRISPR gene editing
/research machine learning cybersecurity
/research sources
```

Research output includes:

```text
title
authors
year/date
venue
citation count
abstract/summary from source
source link
open-access PDF link when available
```

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 6 — Quiz Mode

This version:

- Runs in the terminal.
- Uses an AyAstra personality style.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Saves learning topics to a long-term JSON learning log.
- Quizzes you on learning-log topics using active recall.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar and Crossref fallback.

If no LLM API is configured, AyAstra still runs with local fallback replies. No panic. The lab lights stay on.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Optional: connect the AI brain

1. Copy `.env.example` to a new private file called `.env`.
2. Fill in your LLM settings:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

3. Run AyAstra:

```bash
python main.py
```

4. Inside AyAstra, check:

```text
/brain status
```

Important: never commit `.env` to GitHub. API keys are private.

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
/tutor TOPIC                  Explain a topic beginner-style
/learn add TOPIC | NOTE       Save something you studied
/learn list                   List saved learning topics
/learn review                 Show topics to review
/learn reviewed ID            Mark a topic as reviewed
/quiz start                   Start a quiz from your learning log
/quiz topic TOPIC             Start a quiz on any topic
/quiz current                 Show the current quiz question
/quiz answer YOUR ANSWER      Answer the current quiz question
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
```

## Learning log examples

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

Learning log entries are saved in:

```text
data/learning_log.json
```

## Quiz examples

```text
/quiz help
/quiz start
/quiz topic APIs
/quiz answer An API is a set of rules that lets apps communicate.
/quiz current
/quiz stop
```

## News examples

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

News output includes:

```text
headline
source feed name
publication date from feed
summary from feed
article link
```

## Research examples

```text
/research AI agents in education
/research CRISPR gene editing
/research machine learning cybersecurity
/research sources
```

Research output includes:

```text
title
authors
year/date
venue
citation count
abstract/summary from source
source link
open-access PDF link when available
```

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 7 — Optional Voice Output

This version:

- Runs in the terminal.
- Uses an AyAstra personality style.
- Supports optional local voice output with `pyttsx3`.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Saves learning topics to a long-term JSON learning log.
- Quizzes you on learning-log topics using active recall.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar and Crossref fallback.

If no LLM API or voice package is configured, AyAstra still runs with local fallback replies. No panic. The lab lights stay on.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Install requirements

Activate your virtual environment first, then run:

```bash
pip install -r requirements.txt
```

This installs voice support through `pyttsx3`.

## Optional: connect the AI brain

1. Copy `.env.example` to a new private file called `.env`.
2. Fill in your LLM settings:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

3. Run AyAstra:

```bash
python main.py
```

4. Inside AyAstra, check:

```text
/brain status
```

Important: never commit `.env` to GitHub. API keys are private.

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
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
```

## Voice examples

```text
/voice status
/voice test
/voice on
hello
/voice off
```

Voice starts off every time you open AyAstra. This prevents surprise laptop speeches in public. Very thoughtful, obviously.

## Learning log examples

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

Learning log entries are saved in:

```text
data/learning_log.json
```

## Quiz examples

```text
/quiz help
/quiz start
/quiz topic APIs
/quiz answer An API is a set of rules that lets apps communicate.
/quiz current
/quiz stop
```

## News examples

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

News output includes:

```text
headline
source feed name
publication date from feed
summary from feed
article link
```

## Research examples

```text
/research AI agents in education
/research CRISPR gene editing
/research machine learning cybersecurity
/research sources
```

Research output includes:

```text
title
authors
year/date
venue
citation count
abstract/summary from source
source link
open-access PDF link when available
```

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 8 — Quiz Feedback

This version:

- Runs in the terminal.
- Uses an AyAstra personality style.
- Supports optional local voice output with `pyttsx3`.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Saves learning topics to a long-term JSON learning log.
- Quizzes you on learning-log topics using active recall.
- Gives feedback on completed quiz answers using the optional AI brain when connected, or rule-based feedback when not connected.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar and Crossref fallback.

If no LLM API or voice package is configured, AyAstra still runs with local fallback replies. No panic. The lab lights stay on.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Install requirements

Activate your virtual environment first, then run:

```bash
pip install -r requirements.txt
```

This installs voice support through `pyttsx3`.

## Optional: connect the AI brain

1. Copy `.env.example` to a new private file called `.env`.
2. Fill in your LLM settings:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

3. Run AyAstra:

```bash
python main.py
```

4. Inside AyAstra, check:

```text
/brain status
```

Important: never commit `.env` to GitHub. API keys are private.

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
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
```

## Voice examples

```text
/voice status
/voice test
/voice on
hello
/voice off
```

Voice starts off every time you open AyAstra. This prevents surprise laptop speeches in public. Very thoughtful, obviously.

## Learning log examples

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

Learning log entries are saved in:

```text
data/learning_log.json
```

## Quiz examples

```text
/quiz help
/quiz start
/quiz topic APIs
/quiz answer An API is a set of rules that lets apps communicate.
/quiz current
/quiz feedback
/quiz stop
```

## News examples

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

News output includes:

```text
headline
source feed name
publication date from feed
summary from feed
article link
```

## Research examples

```text
/research AI agents in education
/research CRISPR gene editing
/research machine learning cybersecurity
/research sources
```

Research output includes:

```text
title
authors
year/date
venue
citation count
abstract/summary from source
source link
open-access PDF link when available
```

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 9 — Dashboard UI

This version:

- Runs in the terminal.
- Includes a local futuristic dashboard UI at `http://127.0.0.1:8765`.
- Uses an AyAstra personality style.
- Supports optional local voice output with `pyttsx3`.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Saves learning topics to a long-term JSON learning log.
- Quizzes you on learning-log topics using active recall.
- Gives feedback on completed quiz answers using the optional AI brain when connected, or rule-based feedback when not connected.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar and Crossref fallback.

If no LLM API or voice package is configured, AyAstra still runs with local fallback replies. No panic. The lab lights stay on.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Dashboard quick start

Run the dashboard server:

```bash
python dashboard.py
```

Then open this in your browser:

```text
http://127.0.0.1:8765
```

The dashboard is local-only. It reads and updates your JSON files for tasks, reminders, and learning logs.

## Install requirements

Activate your virtual environment first, then run:

```bash
pip install -r requirements.txt
```

This installs voice support through `pyttsx3`.

## Optional: connect the AI brain

1. Copy `.env.example` to a new private file called `.env`.
2. Fill in your LLM settings:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

3. Run AyAstra:

```bash
python main.py
```

4. Inside AyAstra, check:

```text
/brain status
```

Important: never commit `.env` to GitHub. API keys are private.

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
/dashboard                    Show how to launch the local web dashboard
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
```

## Dashboard examples

```bash
python dashboard.py
```

Then open:

```text
http://127.0.0.1:8765
```

Inside terminal AyAstra, you can also type:

```text
/dashboard
```

## Voice examples

```text
/voice status
/voice test
/voice on
hello
/voice off
```

Voice starts off every time you open AyAstra. This prevents surprise laptop speeches in public. Very thoughtful, obviously.

## Learning log examples

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

Learning log entries are saved in:

```text
data/learning_log.json
```

## Quiz examples

```text
/quiz help
/quiz start
/quiz topic APIs
/quiz answer An API is a set of rules that lets apps communicate.
/quiz current
/quiz feedback
/quiz stop
```

## News examples

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

News output includes:

```text
headline
source feed name
publication date from feed
summary from feed
article link
```

## Research examples

```text
/research AI agents in education
/research CRISPR gene editing
/research machine learning cybersecurity
/research sources
```

Research output includes:

```text
title
authors
year/date
venue
citation count
abstract/summary from source
source link
open-access PDF link when available
```

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 11 — Geometric Depth Dashboard

This version:

- Runs in the terminal.
- Includes a local futuristic glassmorphism dashboard UI at `http://127.0.0.1:8765`.
- Adds geometric depth: cosmic mesh, holographic panels, angular framing, and layered 3D visual structure.
- Includes an animated QuantaCore orb that moves while AyAstra thinks/responds/speaks.
- Supports optional browser speech for dashboard replies.
- Uses an AyAstra personality style.
- Supports optional local voice output with `pyttsx3`.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Saves learning topics to a long-term JSON learning log.
- Quizzes you on learning-log topics using active recall.
- Gives feedback on completed quiz answers using the optional AI brain when connected, or rule-based feedback when not connected.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar and Crossref fallback.

If no LLM API or voice package is configured, AyAstra still runs with local fallback replies. No panic. The lab lights stay on.

## Quick start

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Dashboard quick start

Run the dashboard server:

```bash
python dashboard.py
```

Then open this in your browser:

```text
http://127.0.0.1:8765
```

The dashboard is local-only. It reads and updates your JSON files for tasks, reminders, and learning logs.

## Install requirements

Activate your virtual environment first, then run:

```bash
pip install -r requirements.txt
```

This installs voice support through `pyttsx3`.

## Optional: connect the AI brain

1. Copy `.env.example` to a new private file called `.env`.
2. Fill in your LLM settings:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

3. Run AyAstra:

```bash
python main.py
```

4. Inside AyAstra, check:

```text
/brain status
```

Important: never commit `.env` to GitHub. API keys are private.

## Commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
/dashboard                    Show how to launch the local web dashboard
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
```

## Dashboard examples

```bash
python dashboard.py
```

Then open:

```text
http://127.0.0.1:8765
```

Inside terminal AyAstra, you can also type:

```text
/dashboard
```

## Voice examples

```text
/voice status
/voice test
/voice on
hello
/voice off
```

Voice starts off every time you open AyAstra. This prevents surprise laptop speeches in public. Very thoughtful, obviously.

## Learning log examples

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

Learning log entries are saved in:

```text
data/learning_log.json
```

## Quiz examples

```text
/quiz help
/quiz start
/quiz topic APIs
/quiz answer An API is a set of rules that lets apps communicate.
/quiz current
/quiz feedback
/quiz stop
```

## News examples

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

News output includes:

```text
headline
source feed name
publication date from feed
summary from feed
article link
```

## Research examples

```text
/research AI agents in education
/research CRISPR gene editing
/research machine learning cybersecurity
/research sources
```

Research output includes:

```text
title
authors
year/date
venue
citation count
abstract/summary from source
source link
open-access PDF link when available
```

## Sprint history checkpoint

Recent dashboard-related sprints:

```text
Sprint 9  — Basic local dashboard UI
Sprint 10 — Visual Core Dashboard with animated QuantaCore orb
Sprint 11 — Geometric Depth Dashboard upgrade
```

Sprint 10 specifically added the animated Siri/JARVIS-style visual core and browser voice toggle. Sprint 11 then pushed the design further with geometric depth and a more out-of-this-world interface.

## Project rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite them. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart-home control.

## Current sprint: Sprint 12 — LLM-style Assistant Chat UI

The dashboard-style interface has been removed. The current UI direction is a focused LLM/chat assistant screen, closer to Claude/ChatGPT/Siri-style chat:

- **AyAstra** at the top.
- Greeting or motivational quote in the centre.
- Large ask box near the bottom.
- Quick action chips like Write, Learn, Code, Life stuff, AI updates, Research.
- Conversation appears after the first message.
- Responsive layout for phone, tablet, and desktop browsers.
- Browser speech output and browser microphone input where supported.

The backend tools still exist, so you can ask:

```text
/news ai
/research AI agents in education
/tutor APIs
/task add Finish assignment
/learn add APIs | APIs let apps talk to each other
```

## Important project workflow rule

When we are still refining one feature, we keep it in the same sprint until Ayanda is satisfied. We do **not** create a new sprint for every visual tweak.

Current UI work stays in:

```text
Sprint 12 — LLM-style Assistant Chat UI
```

## Terminal quick start

```bash
python main.py
```

## Assistant UI quick start

Run the focused assistant interface:

```bash
python assistant_ui.py
```

Then open:

```text
http://127.0.0.1:8765
```

## Install requirements

Activate your virtual environment first, then run:

```bash
pip install -r requirements.txt
```

## Optional: connect the AI brain

Create a private `.env` file from `.env.example` and fill in:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
```

Never commit `.env` to GitHub.

## Terminal commands

```text
/help                         Show commands
/exit                         Close AyAstra
/brain status                 Check whether the optional LLM brain is connected
/memory clear                 Clear this session's conversation memory
/ui                           Show how to launch the assistant chat UI
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
```

## Source/truth rule

For news, research, recent tech, health, law, finance, or any current fact, AyAstra must use valid sources and cite/return source links. If sources are unavailable, AyAstra must say it cannot verify the answer.

No fake facts in this lab.

## Device-lock reality check

A browser-based UI cannot reliably respond while your phone/laptop is locked or closed. For true Siri-like background behaviour, AyAstra will later need a native app, PWA/background service, wake word listener, notifications, and OS permissions.
