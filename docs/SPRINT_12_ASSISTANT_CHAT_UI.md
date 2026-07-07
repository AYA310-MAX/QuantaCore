# Sprint 12 — LLM-style Assistant Chat UI

Sprint 12 is the current UI sprint. All visual edits for this feature stay inside this sprint until Ayanda is satisfied.

## Current direction

The dashboard concept has been removed. AyAstra should open like a focused LLM/chat assistant, similar in structure to Claude or ChatGPT:

- AyAstra name at the top.
- Greeting or motivational line in the centre.
- Large prompt box near the bottom.
- Quick action chips for common tasks.
- Conversation appears after the first message.
- Works responsively on phone, tablet, and desktop browser sizes.

## Run

```powershell
python assistant_ui.py
```

Open:

```text
http://127.0.0.1:8765
```

## Test

Try:

```text
hello
/news ai
/research AI agents in education
/tutor APIs
/task add Finish assignment
```

## Important rule for this project

Do not create a new sprint for every visual tweak. Keep UI refinement inside Sprint 12 until the UI direction is approved.

## Future native behaviour

A browser page cannot reliably respond while the phone/laptop is locked. True Siri-like background/lock-screen behaviour will need a future native/PWA/background-service sprint.
