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