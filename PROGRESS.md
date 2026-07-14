## Rebuild Phase — Clean Architecture Setup (2026-07-12)

- Renamed `ay_astra` package to `quantacore`.
- Fixed all broken imports.
- Created clean Flask backend (`app.py`).
- Separated frontend into:
  - templates/
  - static/css/
  - static/js/
- Confirmed Flask server runs successfully on port 8765.
- Established clean project architecture for AyAstra v2.

Learning:
- Folder names affect Python imports.
- Flask expects `templates/` at root level.
- Clean architecture prevents scaling problems later.


## Feature: Reconnect full Assistant router to Flask UI

- Removed temporary stub response from Assistant class.
- Connected Assistant.handle_message() to main router logic.
- Verified that web UI now supports commands like /help and normal chat.






































































# Progress Log — AyAstra / QuantaCore

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.

Progress Log — AyAstra / QuantaCore
2026-06-23 — Sprint 3 Verified News Mode Added
What changed
Added ay_astra/tools/news.py for source-backed RSS/Atom news fetching.
Replaced the old /news placeholder with a working verified news command.
Added /news sources to list configured feeds.
Added topic examples like /news tech, /news ai, /news south africa, /news software, and /news cybersecurity.
Updated README.md with news usage.
Added docs/SPRINT_3_VERIFIED_NEWS.md.
What I learned
RSS/Atom feeds are machine-readable official news feeds.
A source-backed news tool is safer than asking an LLM to invent current updates.
Good assistant design separates facts from guesses.
Tools should handle internet/feed errors gracefully.
Next steps
Test /news sources.
Test /news tech, /news ai, and /news south africa.
Commit the Sprint 3 changes.
Next sprint: build Research Mode using source-backed academic/web results.
2026-06-23 — Sprint 2 Optional AI Brain Added
What changed
Added ay_astra/config.py to load private settings from a local .env file.
Added ay_astra/brain.py, an optional OpenAI-compatible LLM client.
Updated ay_astra/assistant.py so normal chat and /tutor can use the optional AI brain.
Added /brain status to check whether the LLM brain is configured.
Added /memory clear to clear short-term session memory.
Added live/current-info detection so AyAstra does not answer news/current requests from memory.
Updated .env.example, README.md, and added docs/SPRINT_2_AI_BRAIN.md.
What I learned
An LLM brain is optional: AyAstra can still run without it.
API keys must be kept private in .env, never committed to GitHub.
The app can combine local tools, short-term memory, and optional AI responses.
Current facts still need verified source tools, not memory or guesses.
Next steps
Test python main.py.
Try /brain status.
If ready, create a private .env file and connect an LLM provider.
Commit the Sprint 2 changes.
Next sprint: add verified web/news search with citations.
2026-06-14 — Sprint 0/1 Starter Created
What changed
Created the initial Python project structure.
Added a terminal chat loop in main.py.
Added AyAstra's personality and truth/source rules.
Added basic task storage using JSON.
Added basic reminder storage using JSON.
Added placeholders for future verified news and research modes.
What I learned
An assistant is more than a chatbot: it needs tools that can actually do things.
A safe AI assistant should not pretend to know live/current facts without source tools.
JSON files are a simple beginner-friendly way to store tasks and reminders.
Next steps
Open the project in VS Code.
Run python main.py.
Test /help, /task add, /task list, /remind add, and /tutor.
Make the first Git commit.
Next sprint: connect an LLM API for better conversation while keeping source rules.

# Progress Log — AyAstra / QuantaCore

## 2026-07-02 — Sprint 4 Source-Backed Research Mode Added

### What changed
- Added `ay_astra/tools/research.py` for source-backed academic paper search.
- Connected `/research TOPIC` to Semantic Scholar paper metadata.
- Added `/research sources` to show the configured research source.
- Updated `README.md` with research examples.
- Added `docs/SPRINT_4_RESEARCH_MODE.md`.
- Updated the AI brain project date to 2026-07-02.

### What I learned
- Research mode should use sources and links, not guesses.
- Metadata and abstracts are useful starting points, but they are not the same as reading the full paper.
- A reliable assistant must explain what it knows and what it has not verified.
- Semantic Scholar can provide paper titles, authors, abstracts, citation counts, and links through an API.

### Next steps
- Test `/research sources`.
- Test `/research AI agents in education`.
- Commit the Sprint 4 changes.
- Next sprint: add learning logs or explain fetched abstracts using the optional AI brain.

## 2026-06-23 — Sprint 3 Verified News Mode Added

### What changed
- Added `ay_astra/tools/news.py` for source-backed RSS/Atom news fetching.
- Replaced the old `/news` placeholder with a working verified news command.
- Added `/news sources` to list configured feeds.
- Added topic examples like `/news tech`, `/news ai`, `/news south africa`, `/news software`, and `/news cybersecurity`.
- Updated `README.md` with news usage.
- Added `docs/SPRINT_3_VERIFIED_NEWS.md`.

### What I learned
- RSS/Atom feeds are machine-readable official news feeds.
- A source-backed news tool is safer than asking an LLM to invent current updates.
- Good assistant design separates facts from guesses.
- Tools should handle internet/feed errors gracefully.

### Next steps
- Test `/news sources`.
- Test `/news tech`, `/news ai`, and `/news south africa`.
- Commit the Sprint 3 changes.
- Next sprint: build Research Mode using source-backed academic/web results.

## 2026-06-23 — Sprint 2 Optional AI Brain Added

### What changed
- Added `ay_astra/config.py` to load private settings from a local `.env` file.
- Added `ay_astra/brain.py`, an optional OpenAI-compatible LLM client.
- Updated `ay_astra/assistant.py` so normal chat and `/tutor` can use the optional AI brain.
- Added `/brain status` to check whether the LLM brain is configured.
- Added `/memory clear` to clear short-term session memory.
- Added live/current-info detection so AyAstra does not answer news/current requests from memory.
- Updated `.env.example`, `README.md`, and added `docs/SPRINT_2_AI_BRAIN.md`.

### What I learned
- An LLM brain is optional: AyAstra can still run without it.
- API keys must be kept private in `.env`, never committed to GitHub.
- The app can combine local tools, short-term memory, and optional AI responses.
- Current facts still need verified source tools, not memory or guesses.

### Next steps
- Test `python main.py`.
- Try `/brain status`.
- If ready, create a private `.env` file and connect an LLM provider.
- Commit the Sprint 2 changes.
- Next sprint: add verified web/news search with citations.

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.

# AyAstra — QuantaCore

AyAstra, codename **QuantaCore**, is Ayanda Dlamini's personal AI assistant project: a Shuri-inspired, JARVIS/Siri-style assistant for learning, planning, research, news updates, and eventually smart home control.

## Current sprint: Sprint 4 — Source-Backed Research Mode

This version:

- Runs in the terminal.
- Uses an AyAstra personality style.
- Supports basic task commands.
- Supports basic reminder commands.
- Has short-term session memory.
- Can optionally connect to an OpenAI-compatible LLM API for smarter chat/tutor replies.
- Fetches source-backed news through RSS/Atom feeds.
- Searches academic paper metadata through Semantic Scholar.

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


# Progress Log — AyAstra / QuantaCore

## 2026-07-02 — Sprint 5 Learning Log Added

### What changed
- Added `ay_astra/tools/learning.py` for long-term study tracking.
- Added `/learn help`, `/learn add`, `/learn list`, `/learn review`, and `/learn reviewed` commands.
- Connected the learning log to `data/learning_log.json`.
- Updated `README.md` with learning log commands.
- Added `docs/SPRINT_5_LEARNING_LOG.md`.

### What I learned
- Short-term memory and long-term storage are different.
- JSON files can store structured learning entries.
- A useful study assistant should help track topics and reviews, not just answer questions.
- Repetition helps learning stick. Painfully simple. Annoyingly effective.

### Next steps
- Test `/learn help`.
- Add two learning topics.
- Test `/learn list`, `/learn review`, and `/learn reviewed 1`.
- Commit the Sprint 5 changes.
- Next sprint: add quizzes or a dashboard.

## 2026-07-02 — Sprint 4 Source-Backed Research Mode Added

### What changed
- Added `ay_astra/tools/research.py` for source-backed academic paper search.
- Connected `/research TOPIC` to Semantic Scholar paper metadata.
- Added `/research sources` to show the configured research source.
- Updated `README.md` with research examples.
- Added `docs/SPRINT_4_RESEARCH_MODE.md`.
- Updated the AI brain project date to 2026-07-02.

### What I learned
- Research mode should use sources and links, not guesses.
- Metadata and abstracts are useful starting points, but they are not the same as reading the full paper.
- A reliable assistant must explain what it knows and what it has not verified.
- Semantic Scholar can provide paper titles, authors, abstracts, citation counts, and links through an API.

### Next steps
- Test `/research sources`.
- Test `/research AI agents in education`.
- Commit the Sprint 4 changes.
- Next sprint: add learning logs or explain fetched abstracts using the optional AI brain.

## 2026-06-23 — Sprint 3 Verified News Mode Added

### What changed
- Added `ay_astra/tools/news.py` for source-backed RSS/Atom news fetching.
- Replaced the old `/news` placeholder with a working verified news command.
- Added `/news sources` to list configured feeds.
- Added topic examples like `/news tech`, `/news ai`, `/news south africa`, `/news software`, and `/news cybersecurity`.
- Updated `README.md` with news usage.
- Added `docs/SPRINT_3_VERIFIED_NEWS.md`.

### What I learned
- RSS/Atom feeds are machine-readable official news feeds.
- A source-backed news tool is safer than asking an LLM to invent current updates.
- Good assistant design separates facts from guesses.
- Tools should handle internet/feed errors gracefully.

### Next steps
- Test `/news sources`.
- Test `/news tech`, `/news ai`, and `/news south africa`.
- Commit the Sprint 3 changes.
- Next sprint: build Research Mode using source-backed academic/web results.

## 2026-06-23 — Sprint 2 Optional AI Brain Added

### What changed
- Added `ay_astra/config.py` to load private settings from a local `.env` file.
- Added `ay_astra/brain.py`, an optional OpenAI-compatible LLM client.
- Updated `ay_astra/assistant.py` so normal chat and `/tutor` can use the optional AI brain.
- Added `/brain status` to check whether the LLM brain is configured.
- Added `/memory clear` to clear short-term session memory.
- Added live/current-info detection so AyAstra does not answer news/current requests from memory.
- Updated `.env.example`, `README.md`, and added `docs/SPRINT_2_AI_BRAIN.md`.

### What I learned
- An LLM brain is optional: AyAstra can still run without it.
- API keys must be kept private in `.env`, never committed to GitHub.
- The app can combine local tools, short-term memory, and optional AI responses.
- Current facts still need verified source tools, not memory or guesses.

### Next steps
- Test `python main.py`.
- Try `/brain status`.
- If ready, create a private `.env` file and connect an LLM provider.
- Commit the Sprint 2 changes.
- Next sprint: add verified web/news search with citations.

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.

# Progress Log — AyAstra / QuantaCore

## 2026-07-02 — Sprint 6 Quiz Mode Added

### What changed
- Added `ay_astra/tools/quiz.py` for active-recall quiz sessions.
- Added `/quiz help`, `/quiz start`, `/quiz topic`, `/quiz current`, `/quiz answer`, and `/quiz stop` commands.
- Connected Quiz Mode to the Learning Log so AyAstra can quiz saved topics.
- Updated `README.md` with Quiz Mode commands.
- Added `docs/SPRINT_6_QUIZ_MODE.md`.

### What I learned
- Active recall helps learning more than passive rereading.
- A tool can keep temporary quiz state while the app is running.
- Assistant features can connect together: `/learn` stores topics and `/quiz` practises them.
- Automatic grading should be added carefully later, preferably with the optional AI brain.

### Next steps
- Test `/quiz help`.
- Add a learning topic.
- Test `/quiz start` and answer the questions.
- Commit the Sprint 6 changes.
- Next sprint: choose AI feedback, voice output, dashboard UI, or smart-home prep.

## 2026-07-02 — Sprint 5 Learning Log Added

### What changed
- Added `ay_astra/tools/learning.py` for long-term study tracking.
- Added `/learn help`, `/learn add`, `/learn list`, `/learn review`, and `/learn reviewed` commands.
- Connected the learning log to `data/learning_log.json`.
- Updated `README.md` with learning log commands.
- Added `docs/SPRINT_5_LEARNING_LOG.md`.

### What I learned
- Short-term memory and long-term storage are different.
- JSON files can store structured learning entries.
- A useful study assistant should help track topics and reviews, not just answer questions.
- Repetition helps learning stick. Painfully simple. Annoyingly effective.

### Next steps
- Test `/learn help`.
- Add two learning topics.
- Test `/learn list`, `/learn review`, and `/learn reviewed 1`.
- Commit the Sprint 5 changes.
- Next sprint: add quizzes or a dashboard.

## 2026-07-02 — Sprint 4 Source-Backed Research Mode Added

### What changed
- Added `ay_astra/tools/research.py` for source-backed academic paper search.
- Connected `/research TOPIC` to Semantic Scholar paper metadata.
- Added `/research sources` to show the configured research source.
- Updated `README.md` with research examples.
- Added `docs/SPRINT_4_RESEARCH_MODE.md`.
- Updated the AI brain project date to 2026-07-02.

### What I learned
- Research mode should use sources and links, not guesses.
- Metadata and abstracts are useful starting points, but they are not the same as reading the full paper.
- A reliable assistant must explain what it knows and what it has not verified.
- Semantic Scholar can provide paper titles, authors, abstracts, citation counts, and links through an API.

### Next steps
- Test `/research sources`.
- Test `/research AI agents in education`.
- Commit the Sprint 4 changes.
- Next sprint: add learning logs or explain fetched abstracts using the optional AI brain.

## 2026-06-23 — Sprint 3 Verified News Mode Added

### What changed
- Added `ay_astra/tools/news.py` for source-backed RSS/Atom news fetching.
- Replaced the old `/news` placeholder with a working verified news command.
- Added `/news sources` to list configured feeds.
- Added topic examples like `/news tech`, `/news ai`, `/news south africa`, `/news software`, and `/news cybersecurity`.
- Updated `README.md` with news usage.
- Added `docs/SPRINT_3_VERIFIED_NEWS.md`.

### What I learned
- RSS/Atom feeds are machine-readable official news feeds.
- A source-backed news tool is safer than asking an LLM to invent current updates.
- Good assistant design separates facts from guesses.
- Tools should handle internet/feed errors gracefully.

### Next steps
- Test `/news sources`.
- Test `/news tech`, `/news ai`, and `/news south africa`.
- Commit the Sprint 3 changes.
- Next sprint: build Research Mode using source-backed academic/web results.

## 2026-06-23 — Sprint 2 Optional AI Brain Added

### What changed
- Added `ay_astra/config.py` to load private settings from a local `.env` file.
- Added `ay_astra/brain.py`, an optional OpenAI-compatible LLM client.
- Updated `ay_astra/assistant.py` so normal chat and `/tutor` can use the optional AI brain.
- Added `/brain status` to check whether the LLM brain is configured.
- Added `/memory clear` to clear short-term session memory.
- Added live/current-info detection so AyAstra does not answer news/current requests from memory.
- Updated `.env.example`, `README.md`, and added `docs/SPRINT_2_AI_BRAIN.md`.

### What I learned
- An LLM brain is optional: AyAstra can still run without it.
- API keys must be kept private in `.env`, never committed to GitHub.
- The app can combine local tools, short-term memory, and optional AI responses.
- Current facts still need verified source tools, not memory or guesses.

### Next steps
- Test `python main.py`.
- Try `/brain status`.
- If ready, create a private `.env` file and connect an LLM provider.
- Commit the Sprint 2 changes.
- Next sprint: add verified web/news search with citations.

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.


# Progress Log — AyAstra / QuantaCore

## 2026-07-04 — Sprint 11 Geometric Depth Dashboard Upgrade

### What changed
- Redesigned the dashboard to feel less generic and more like an out-of-this-world AI interface.
- Added a cosmic mesh background, holographic framing, angular depth, and stronger glassmorphism.
- Improved the animated QuantaCore orb and reactive speaking/thinking state.
- Preserved the working dashboard features: chat, tasks, reminders, learning log, news, and research.
- Added `docs/SPRINT_11_GEOMETRIC_DEPTH_DASHBOARD.md`.

### What I learned
- Visual identity is part of assistant design, not decoration.
- Geometric depth can be created with CSS grids, pseudo-elements, transforms, and layered gradients.
- A premium AI interface needs motion, depth, and a recognizable core visual.

### Next steps
- Test the dashboard visually in the browser.
- Commit the dashboard UI upgrade.
- Next sprint: mobile view polish, real AI brain connection, speech input, or smart-home prep.

## 2026-07-04 — Sprint 10 Visual Core Dashboard Upgrade

### What changed
- Upgraded the dashboard theme to a dark cosmic glassmorphism UI.
- Added a Siri/JARVIS-inspired animated QuantaCore orb.
- Added a dashboard chat panel connected to AyAstra's existing command router.
- Added optional browser speech toggle for dashboard replies.
- Made the orb animate while AyAstra is thinking/responding/speaking.
- Added `docs/SPRINT_10_VISUAL_CORE_DASHBOARD.md`.

### What I learned
- UI personality matters for an assistant: it should feel like the product vision.
- CSS animations can create a living assistant core without needing external assets.
- Browser SpeechSynthesis can provide simple dashboard voice output.
- The dashboard can reuse the same backend tools as terminal AyAstra.

### Next steps
- Test `python dashboard.py`.
- Open `http://127.0.0.1:8765`.
- Toggle browser voice and send a chat message.
- Commit the visual dashboard upgrade.
- Next sprint: improve mobile UI, connect real AI brain, or start smart-home prep.

## 2026-07-04 — Sprint 9 Dashboard UI Added

### What changed
- Added `ay_astra/dashboard.py`, a local web dashboard server using Python standard library.
- Added root `dashboard.py` runner.
- Added `/dashboard` command in terminal AyAstra to show launch instructions.
- Dashboard shows tasks, reminders, learning log stats, news search, and research search.
- Dashboard can add tasks, complete tasks, add reminders, and add learning topics.
- Updated `README.md` and added `docs/SPRINT_9_DASHBOARD_UI.md`.

### What I learned
- A local web dashboard is just a small web server plus HTML/CSS/JavaScript.
- Browser pages can talk to Python through JSON API endpoints.
- A dashboard should start local-only before any public hosting.
- Visual interfaces make assistant tools easier to use.

### Next steps
- Test `python dashboard.py`.
- Open `http://127.0.0.1:8765`.
- Add a task, learning topic, and reminder from the dashboard.
- Commit the Sprint 9 changes.
- Next sprint: improve dashboard design, connect the real AI brain, or start smart-home prep.

## 2026-07-02 — Sprint 8 Quiz Feedback Added

### What changed
- Added `/quiz feedback` for feedback on the most recently completed quiz.
- Quiz Mode now stores the last completed quiz session in memory.
- If the optional AI brain is connected, AyAstra can use it for detailed feedback.
- If the AI brain is not connected, AyAstra gives rule-based feedback.
- Updated `README.md` and added `docs/SPRINT_8_QUIZ_FEEDBACK.md`.

### What I learned
- Feedback turns practice into better learning.
- Optional AI features should have safe non-AI fallbacks.
- Rule-based feedback is useful, but it is not the same as deep semantic grading.
- Features can improve gradually without breaking the whole assistant.

### Next steps
- Test a full quiz flow and run `/quiz feedback`.
- Commit the Sprint 8 changes.
- Next sprint: connect the real AI brain, build a dashboard, speech input, or smart-home prep.

## 2026-07-02 — Sprint 7 Optional Voice Output Added

### What changed
- Added `ay_astra/tools/voice.py` for optional text-to-speech output.
- Added `/voice help`, `/voice status`, `/voice on`, `/voice off`, and `/voice test` commands.
- Updated `main.py` so AyAstra can speak printed responses when voice is enabled.
- Added `pyttsx3` to `requirements.txt`.
- Updated `README.md` with voice commands.
- Added `docs/SPRINT_7_VOICE_OUTPUT.md`.

### What I learned
- Text-to-speech turns written responses into spoken audio.
- Optional features should not crash the app if a package is missing.
- Voice output belongs near the terminal loop because that is where final responses are printed.
- Voice starts off by default to avoid surprise laptop speeches.

### Next steps
- Run `pip install -r requirements.txt`.
- Test `/voice status` and `/voice test`.
- Turn on voice with `/voice on` and test a normal greeting.
- Commit the Sprint 7 changes.
- Next sprint: voice settings, speech input, dashboard UI, or smart-home prep.

## 2026-07-02 — Sprint 6 Quiz Mode Added

### What changed
- Added `ay_astra/tools/quiz.py` for active-recall quiz sessions.
- Added `/quiz help`, `/quiz start`, `/quiz topic`, `/quiz current`, `/quiz answer`, and `/quiz stop` commands.
- Connected Quiz Mode to the Learning Log so AyAstra can quiz saved topics.
- Updated `README.md` with Quiz Mode commands.
- Added `docs/SPRINT_6_QUIZ_MODE.md`.

### What I learned
- Active recall helps learning more than passive rereading.
- A tool can keep temporary quiz state while the app is running.
- Assistant features can connect together: `/learn` stores topics and `/quiz` practises them.
- Automatic grading should be added carefully later, preferably with the optional AI brain.

### Next steps
- Test `/quiz help`.
- Add a learning topic.
- Test `/quiz start` and answer the questions.
- Commit the Sprint 6 changes.
- Next sprint: choose AI feedback, voice output, dashboard UI, or smart-home prep.

## 2026-07-02 — Sprint 5 Learning Log Added

### What changed
- Added `ay_astra/tools/learning.py` for long-term study tracking.
- Added `/learn help`, `/learn add`, `/learn list`, `/learn review`, and `/learn reviewed` commands.
- Connected the learning log to `data/learning_log.json`.
- Updated `README.md` with learning log commands.
- Added `docs/SPRINT_5_LEARNING_LOG.md`.

### What I learned
- Short-term memory and long-term storage are different.
- JSON files can store structured learning entries.
- A useful study assistant should help track topics and reviews, not just answer questions.
- Repetition helps learning stick. Painfully simple. Annoyingly effective.

### Next steps
- Test `/learn help`.
- Add two learning topics.
- Test `/learn list`, `/learn review`, and `/learn reviewed 1`.
- Commit the Sprint 5 changes.
- Next sprint: add quizzes or a dashboard.

## 2026-07-02 — Sprint 4 Source-Backed Research Mode Added

### What changed
- Added `ay_astra/tools/research.py` for source-backed academic paper search.
- Connected `/research TOPIC` to Semantic Scholar paper metadata.
- Added `/research sources` to show the configured research source.
- Updated `README.md` with research examples.
- Added `docs/SPRINT_4_RESEARCH_MODE.md`.
- Updated the AI brain project date to 2026-07-02.

### What I learned
- Research mode should use sources and links, not guesses.
- Metadata and abstracts are useful starting points, but they are not the same as reading the full paper.
- A reliable assistant must explain what it knows and what it has not verified.
- Semantic Scholar can provide paper titles, authors, abstracts, citation counts, and links through an API.

### Next steps
- Test `/research sources`.
- Test `/research AI agents in education`.
- Commit the Sprint 4 changes.
- Next sprint: add learning logs or explain fetched abstracts using the optional AI brain.

## 2026-06-23 — Sprint 3 Verified News Mode Added

### What changed
- Added `ay_astra/tools/news.py` for source-backed RSS/Atom news fetching.
- Replaced the old `/news` placeholder with a working verified news command.
- Added `/news sources` to list configured feeds.
- Added topic examples like `/news tech`, `/news ai`, `/news south africa`, `/news software`, and `/news cybersecurity`.
- Updated `README.md` with news usage.
- Added `docs/SPRINT_3_VERIFIED_NEWS.md`.

### What I learned
- RSS/Atom feeds are machine-readable official news feeds.
- A source-backed news tool is safer than asking an LLM to invent current updates.
- Good assistant design separates facts from guesses.
- Tools should handle internet/feed errors gracefully.

### Next steps
- Test `/news sources`.
- Test `/news tech`, `/news ai`, and `/news south africa`.
- Commit the Sprint 3 changes.
- Next sprint: build Research Mode using source-backed academic/web results.

## 2026-06-23 — Sprint 2 Optional AI Brain Added

### What changed
- Added `ay_astra/config.py` to load private settings from a local `.env` file.
- Added `ay_astra/brain.py`, an optional OpenAI-compatible LLM client.
- Updated `ay_astra/assistant.py` so normal chat and `/tutor` can use the optional AI brain.
- Added `/brain status` to check whether the LLM brain is configured.
- Added `/memory clear` to clear short-term session memory.
- Added live/current-info detection so AyAstra does not answer news/current requests from memory.
- Updated `.env.example`, `README.md`, and added `docs/SPRINT_2_AI_BRAIN.md`.

### What I learned
- An LLM brain is optional: AyAstra can still run without it.
- API keys must be kept private in `.env`, never committed to GitHub.
- The app can combine local tools, short-term memory, and optional AI responses.
- Current facts still need verified source tools, not memory or guesses.

### Next steps
- Test `python main.py`.
- Try `/brain status`.
- If ready, create a private `.env` file and connect an LLM provider.
- Commit the Sprint 2 changes.
- Next sprint: add verified web/news search with citations.

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.

# Progress Log — AyAstra / QuantaCore

## 2026-07-07 — Sprint 12 LLM-style Assistant Chat UI

### What changed
- Removed the dashboard-style UI direction.
- Removed dashboard files and old dashboard documentation.
- Kept the focused assistant UI in `assistant_ui.py` and `ay_astra/assistant_ui.py`.
- Changed the UI to look more like a focused LLM/chat screen: AyAstra at the top, greeting/motivational prompt in the centre, large ask box, and quick action chips.
- Kept browser speech output and browser microphone input where supported.
- Updated `README.md` and replaced the UI docs with `docs/SPRINT_12_ASSISTANT_CHAT_UI.md`.

### What I learned
- Do not create a new sprint for every visual tweak inside the same feature.
- Keep a feature in one sprint until the direction is approved.
- AyAstra's UI should feel like a personal assistant/chat interface, not a control dashboard.
- True lock-screen/background response will require a future native/PWA/background-service approach.

### Next steps
- Test `python assistant_ui.py`.
- Refine Sprint 12 UI until Ayanda is satisfied.
- Do not create a new sprint for more UI tweaks unless we move to a genuinely new feature.


## 2026-07-02 — Sprint 8 Quiz Feedback Added

### What changed
- Added `/quiz feedback` for feedback on the most recently completed quiz.
- Quiz Mode now stores the last completed quiz session in memory.
- If the optional AI brain is connected, AyAstra can use it for detailed feedback.
- If the AI brain is not connected, AyAstra gives rule-based feedback.
- Updated `README.md` and added `docs/SPRINT_8_QUIZ_FEEDBACK.md`.

### What I learned
- Feedback turns practice into better learning.
- Optional AI features should have safe non-AI fallbacks.
- Rule-based feedback is useful, but it is not the same as deep semantic grading.
- Features can improve gradually without breaking the whole assistant.

### Next steps
- Test a full quiz flow and run `/quiz feedback`.
- Commit the Sprint 8 changes.
- Next sprint: connect the real AI brain, improve the assistant UI, speech input, or smart-home prep.

## 2026-07-02 — Sprint 7 Optional Voice Output Added

### What changed
- Added `ay_astra/tools/voice.py` for optional text-to-speech output.
- Added `/voice help`, `/voice status`, `/voice on`, `/voice off`, and `/voice test` commands.
- Updated `main.py` so AyAstra can speak printed responses when voice is enabled.
- Added `pyttsx3` to `requirements.txt`.
- Updated `README.md` with voice commands.
- Added `docs/SPRINT_7_VOICE_OUTPUT.md`.

### What I learned
- Text-to-speech turns written responses into spoken audio.
- Optional features should not crash the app if a package is missing.
- Voice output belongs near the terminal loop because that is where final responses are printed.
- Voice starts off by default to avoid surprise laptop speeches.

### Next steps
- Run `pip install -r requirements.txt`.
- Test `/voice status` and `/voice test`.
- Turn on voice with `/voice on` and test a normal greeting.
- Commit the Sprint 7 changes.
- Next sprint: voice settings, speech input, assistant UI, or smart-home prep.

## 2026-07-02 — Sprint 6 Quiz Mode Added

### What changed
- Added `ay_astra/tools/quiz.py` for active-recall quiz sessions.
- Added `/quiz help`, `/quiz start`, `/quiz topic`, `/quiz current`, `/quiz answer`, and `/quiz stop` commands.
- Connected Quiz Mode to the Learning Log so AyAstra can quiz saved topics.
- Updated `README.md` with Quiz Mode commands.
- Added `docs/SPRINT_6_QUIZ_MODE.md`.

### What I learned
- Active recall helps learning more than passive rereading.
- A tool can keep temporary quiz state while the app is running.
- Assistant features can connect together: `/learn` stores topics and `/quiz` practises them.
- Automatic grading should be added carefully later, preferably with the optional AI brain.

### Next steps
- Test `/quiz help`.
- Add a learning topic.
- Test `/quiz start` and answer the questions.
- Commit the Sprint 6 changes.
- Next sprint: choose AI feedback, voice output, assistant UI, or smart-home prep.

## 2026-07-02 — Sprint 5 Learning Log Added

### What changed
- Added `ay_astra/tools/learning.py` for long-term study tracking.
- Added `/learn help`, `/learn add`, `/learn list`, `/learn review`, and `/learn reviewed` commands.
- Connected the learning log to `data/learning_log.json`.
- Updated `README.md` with learning log commands.
- Added `docs/SPRINT_5_LEARNING_LOG.md`.

### What I learned
- Short-term memory and long-term storage are different.
- JSON files can store structured learning entries.
- A useful study assistant should help track topics and reviews, not just answer questions.
- Repetition helps learning stick. Painfully simple. Annoyingly effective.

### Next steps
- Test `/learn help`.
- Add two learning topics.
- Test `/learn list`, `/learn review`, and `/learn reviewed 1`.
- Commit the Sprint 5 changes.
- Next sprint: add quizzes or improve the assistant UI.

## 2026-07-02 — Sprint 4 Source-Backed Research Mode Added

### What changed
- Added `ay_astra/tools/research.py` for source-backed academic paper search.
- Connected `/research TOPIC` to Semantic Scholar paper metadata.
- Added `/research sources` to show the configured research source.
- Updated `README.md` with research examples.
- Added `docs/SPRINT_4_RESEARCH_MODE.md`.
- Updated the AI brain project date to 2026-07-02.

### What I learned
- Research mode should use sources and links, not guesses.
- Metadata and abstracts are useful starting points, but they are not the same as reading the full paper.
- A reliable assistant must explain what it knows and what it has not verified.
- Semantic Scholar can provide paper titles, authors, abstracts, citation counts, and links through an API.

### Next steps
- Test `/research sources`.
- Test `/research AI agents in education`.
- Commit the Sprint 4 changes.
- Next sprint: add learning logs or explain fetched abstracts using the optional AI brain.

## 2026-06-23 — Sprint 3 Verified News Mode Added

### What changed
- Added `ay_astra/tools/news.py` for source-backed RSS/Atom news fetching.
- Replaced the old `/news` placeholder with a working verified news command.
- Added `/news sources` to list configured feeds.
- Added topic examples like `/news tech`, `/news ai`, `/news south africa`, `/news software`, and `/news cybersecurity`.
- Updated `README.md` with news usage.
- Added `docs/SPRINT_3_VERIFIED_NEWS.md`.

### What I learned
- RSS/Atom feeds are machine-readable official news feeds.
- A source-backed news tool is safer than asking an LLM to invent current updates.
- Good assistant design separates facts from guesses.
- Tools should handle internet/feed errors gracefully.

### Next steps
- Test `/news sources`.
- Test `/news tech`, `/news ai`, and `/news south africa`.
- Commit the Sprint 3 changes.
- Next sprint: build Research Mode using source-backed academic/web results.

## 2026-06-23 — Sprint 2 Optional AI Brain Added

### What changed
- Added `ay_astra/config.py` to load private settings from a local `.env` file.
- Added `ay_astra/brain.py`, an optional OpenAI-compatible LLM client.
- Updated `ay_astra/assistant.py` so normal chat and `/tutor` can use the optional AI brain.
- Added `/brain status` to check whether the LLM brain is configured.
- Added `/memory clear` to clear short-term session memory.
- Added live/current-info detection so AyAstra does not answer news/current requests from memory.
- Updated `.env.example`, `README.md`, and added `docs/SPRINT_2_AI_BRAIN.md`.

### What I learned
- An LLM brain is optional: AyAstra can still run without it.
- API keys must be kept private in `.env`, never committed to GitHub.
- The app can combine local tools, short-term memory, and optional AI responses.
- Current facts still need verified source tools, not memory or guesses.

### Next steps
- Test `python main.py`.
- Try `/brain status`.
- If ready, create a private `.env` file and connect an LLM provider.
- Commit the Sprint 2 changes.
- Next sprint: add verified web/news search with citations.

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.

## 2026-07-07 — Sprint 12 LLM-style Assistant Chat UI

### What changed
- Removed the dashboard-style UI direction.
- Removed dashboard files and old dashboard documentation.
- Kept the focused assistant UI in `assistant_ui.py` and `ay_astra/assistant_ui.py`.
- Changed the UI to look more like a focused LLM/chat screen: AyAstra at the top, greeting/motivational prompt in the centre, large ask box, and quick action chips.
- Kept browser speech output and browser microphone input where supported.

### What I learned
- Do not create a new sprint for every visual tweak inside the same feature.
- Keep a feature in one sprint until the direction is approved.
- AyAstra's UI should feel like a personal assistant/chat interface, not a control dashboard.

### Next steps
- Test `python assistant_ui.py`.
- Refine Sprint 12 UI until Ayanda is satisfied.

# Progress Log — AyAstra / QuantaCore

## 2026-07-07 — Sprint 12 LLM-style Assistant Chat UI

### What changed
- Removed the dashboard-style UI direction.
- Removed dashboard files and old dashboard documentation.
- Kept the focused assistant UI in `assistant_ui.py` and `ay_astra/assistant_ui.py`.
- Changed the UI to a focused dark AI chat app using AyAstra's Dark Amethyst and Dark Royal Blue theme.
- Added HOME, Chats, Files, and Settings screens.
- Added a centered phone-like chat card on HOME.
- Added file upload, image upload, internet image preview UI, attachment chips, image thumbnails, and file library UI.
- Kept browser speech output and browser microphone input where supported.
- Updated `README.md` and replaced the UI docs with `docs/SPRINT_12_ASSISTANT_CHAT_UI.md`.

### What I learned
- Do not create a new sprint for every visual tweak inside the same feature.
- Keep a feature in one sprint until the direction is approved.
- AyAstra's UI should feel like a personal assistant/chat interface, not a control dashboard.
- True lock-screen/background response will require a future native/PWA/background-service approach.

### Next steps
- Test `python assistant_ui.py`.
- Refine Sprint 12 UI until Ayanda is satisfied.
- Do not create a new sprint for more UI tweaks unless we move to a genuinely new feature.


## 2026-07-02 — Sprint 8 Quiz Feedback Added

### What changed
- Added `/quiz feedback` for feedback on the most recently completed quiz.
- Quiz Mode now stores the last completed quiz session in memory.
- If the optional AI brain is connected, AyAstra can use it for detailed feedback.
- If the AI brain is not connected, AyAstra gives rule-based feedback.
- Updated `README.md` and added `docs/SPRINT_8_QUIZ_FEEDBACK.md`.

### What I learned
- Feedback turns practice into better learning.
- Optional AI features should have safe non-AI fallbacks.
- Rule-based feedback is useful, but it is not the same as deep semantic grading.
- Features can improve gradually without breaking the whole assistant.

### Next steps
- Test a full quiz flow and run `/quiz feedback`.
- Commit the Sprint 8 changes.
- Next sprint: connect the real AI brain, improve the assistant UI, speech input, or smart-home prep.

## 2026-07-02 — Sprint 7 Optional Voice Output Added

### What changed
- Added `ay_astra/tools/voice.py` for optional text-to-speech output.
- Added `/voice help`, `/voice status`, `/voice on`, `/voice off`, and `/voice test` commands.
- Updated `main.py` so AyAstra can speak printed responses when voice is enabled.
- Added `pyttsx3` to `requirements.txt`.
- Updated `README.md` with voice commands.
- Added `docs/SPRINT_7_VOICE_OUTPUT.md`.

### What I learned
- Text-to-speech turns written responses into spoken audio.
- Optional features should not crash the app if a package is missing.
- Voice output belongs near the terminal loop because that is where final responses are printed.
- Voice starts off by default to avoid surprise laptop speeches.

### Next steps
- Run `pip install -r requirements.txt`.
- Test `/voice status` and `/voice test`.
- Turn on voice with `/voice on` and test a normal greeting.
- Commit the Sprint 7 changes.
- Next sprint: voice settings, speech input, assistant UI, or smart-home prep.

## 2026-07-02 — Sprint 6 Quiz Mode Added

### What changed
- Added `ay_astra/tools/quiz.py` for active-recall quiz sessions.
- Added `/quiz help`, `/quiz start`, `/quiz topic`, `/quiz current`, `/quiz answer`, and `/quiz stop` commands.
- Connected Quiz Mode to the Learning Log so AyAstra can quiz saved topics.
- Updated `README.md` with Quiz Mode commands.
- Added `docs/SPRINT_6_QUIZ_MODE.md`.

### What I learned
- Active recall helps learning more than passive rereading.
- A tool can keep temporary quiz state while the app is running.
- Assistant features can connect together: `/learn` stores topics and `/quiz` practises them.
- Automatic grading should be added carefully later, preferably with the optional AI brain.

### Next steps
- Test `/quiz help`.
- Add a learning topic.
- Test `/quiz start` and answer the questions.
- Commit the Sprint 6 changes.
- Next sprint: choose AI feedback, voice output, assistant UI, or smart-home prep.

## 2026-07-02 — Sprint 5 Learning Log Added

### What changed
- Added `ay_astra/tools/learning.py` for long-term study tracking.
- Added `/learn help`, `/learn add`, `/learn list`, `/learn review`, and `/learn reviewed` commands.
- Connected the learning log to `data/learning_log.json`.
- Updated `README.md` with learning log commands.
- Added `docs/SPRINT_5_LEARNING_LOG.md`.

### What I learned
- Short-term memory and long-term storage are different.
- JSON files can store structured learning entries.
- A useful study assistant should help track topics and reviews, not just answer questions.
- Repetition helps learning stick. Painfully simple. Annoyingly effective.

### Next steps
- Test `/learn help`.
- Add two learning topics.
- Test `/learn list`, `/learn review`, and `/learn reviewed 1`.
- Commit the Sprint 5 changes.
- Next sprint: add quizzes or improve the assistant UI.

## 2026-07-02 — Sprint 4 Source-Backed Research Mode Added

### What changed
- Added `ay_astra/tools/research.py` for source-backed academic paper search.
- Connected `/research TOPIC` to Semantic Scholar paper metadata.
- Added `/research sources` to show the configured research source.
- Updated `README.md` with research examples.
- Added `docs/SPRINT_4_RESEARCH_MODE.md`.
- Updated the AI brain project date to 2026-07-02.

### What I learned
- Research mode should use sources and links, not guesses.
- Metadata and abstracts are useful starting points, but they are not the same as reading the full paper.
- A reliable assistant must explain what it knows and what it has not verified.
- Semantic Scholar can provide paper titles, authors, abstracts, citation counts, and links through an API.

### Next steps
- Test `/research sources`.
- Test `/research AI agents in education`.
- Commit the Sprint 4 changes.
- Next sprint: add learning logs or explain fetched abstracts using the optional AI brain.

## 2026-06-23 — Sprint 3 Verified News Mode Added

### What changed
- Added `ay_astra/tools/news.py` for source-backed RSS/Atom news fetching.
- Replaced the old `/news` placeholder with a working verified news command.
- Added `/news sources` to list configured feeds.
- Added topic examples like `/news tech`, `/news ai`, `/news south africa`, `/news software`, and `/news cybersecurity`.
- Updated `README.md` with news usage.
- Added `docs/SPRINT_3_VERIFIED_NEWS.md`.

### What I learned
- RSS/Atom feeds are machine-readable official news feeds.
- A source-backed news tool is safer than asking an LLM to invent current updates.
- Good assistant design separates facts from guesses.
- Tools should handle internet/feed errors gracefully.

### Next steps
- Test `/news sources`.
- Test `/news tech`, `/news ai`, and `/news south africa`.
- Commit the Sprint 3 changes.
- Next sprint: build Research Mode using source-backed academic/web results.

## 2026-06-23 — Sprint 2 Optional AI Brain Added

### What changed
- Added `ay_astra/config.py` to load private settings from a local `.env` file.
- Added `ay_astra/brain.py`, an optional OpenAI-compatible LLM client.
- Updated `ay_astra/assistant.py` so normal chat and `/tutor` can use the optional AI brain.
- Added `/brain status` to check whether the LLM brain is configured.
- Added `/memory clear` to clear short-term session memory.
- Added live/current-info detection so AyAstra does not answer news/current requests from memory.
- Updated `.env.example`, `README.md`, and added `docs/SPRINT_2_AI_BRAIN.md`.

### What I learned
- An LLM brain is optional: AyAstra can still run without it.
- API keys must be kept private in `.env`, never committed to GitHub.
- The app can combine local tools, short-term memory, and optional AI responses.
- Current facts still need verified source tools, not memory or guesses.

### Next steps
- Test `python main.py`.
- Try `/brain status`.
- If ready, create a private `.env` file and connect an LLM provider.
- Commit the Sprint 2 changes.
- Next sprint: add verified web/news search with citations.

## 2026-06-14 — Sprint 0/1 Starter Created

### What changed
- Created the initial Python project structure.
- Added a terminal chat loop in `main.py`.
- Added AyAstra's personality and truth/source rules.
- Added basic task storage using JSON.
- Added basic reminder storage using JSON.
- Added placeholders for future verified news and research modes.

### What I learned
- An assistant is more than a chatbot: it needs tools that can actually do things.
- A safe AI assistant should not pretend to know live/current facts without source tools.
- JSON files are a simple beginner-friendly way to store tasks and reminders.

### Next steps
- Open the project in VS Code.
- Run `python main.py`.
- Test `/help`, `/task add`, `/task list`, `/remind add`, and `/tutor`.
- Make the first Git commit.
- Next sprint: connect an LLM API for better conversation while keeping source rules.
