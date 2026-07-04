# Sprint 10 — Visual Core Dashboard

Sprint 10 upgrades the dashboard style so AyAstra starts looking more like a Siri/JARVIS-style assistant.

## Design inspiration

The visual direction is based on:

- dark cosmic purple backgrounds,
- glassmorphism cards,
- neon violet/pink/cyan highlights,
- subtle green and gold accents,
- mobile assistant panels,
- an animated central orb/core.

## What changed

- The dashboard now has a hero section for AyAstra.
- The QuantaCore orb animates when AyAstra is thinking or responding.
- The dashboard has a chat panel connected to the existing AyAstra command router.
- Browser voice can be toggled on from the dashboard.
- When browser voice is enabled, the orb animates while speech synthesis is speaking.
- News, research, tasks, reminders, and learning actions also pulse the orb.

## How to run

```powershell
python dashboard.py
```

Then open:

```text
http://127.0.0.1:8765
```

## Test checklist

1. Open the dashboard.
2. Click **Chat with AyAstra**.
3. Send:

```text
hello
```

4. Send:

```text
/news ai
```

5. Toggle **browser voice + moving core**.
6. Send another message and watch the orb animate.
7. Add a task and confirm the orb pulses.
8. Search a research topic.

## Important note

This uses browser speech synthesis, not the earlier Python `pyttsx3` voice system. That means the dashboard can speak separately from the terminal voice feature.

## Commit

```powershell
git status
git add .
git commit -m "Upgrade dashboard with animated visual core"
```
