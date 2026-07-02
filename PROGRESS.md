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


