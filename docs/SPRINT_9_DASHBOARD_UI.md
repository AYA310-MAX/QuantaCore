# Sprint 9 — Dashboard UI

Sprint 9 adds a local web dashboard for AyAstra / QuantaCore.

## Child-level explanation

Before this sprint, AyAstra lived mostly in the terminal.

Now she also has a small local web page you can open in your browser.

Think of it like a simple command center:

- tasks,
- reminders,
- learning log,
- verified news,
- research search.

Not full JARVIS yet, but definitely a more futuristic lab panel.

## Files added

```text
dashboard.py
ay_astra/dashboard.py
```

## How to run it

Make sure your virtual environment is active:

```text
(.venv)
```

Then run:

```powershell
python dashboard.py
```

Open:

```text
http://127.0.0.1:8765
```

To stop the dashboard server, press:

```text
Ctrl + C
```

in the terminal where it is running.

## What the dashboard can do

- Show task counts.
- Add tasks.
- Mark tasks as done.
- Show reminders.
- Add reminders.
- Show learning log topics.
- Add learning topics.
- Fetch source-backed news.
- Search academic research metadata.

## Important safety note

The dashboard runs on:

```text
127.0.0.1
```

That means it is local to your computer only.

It is not meant to be exposed to the public internet.

## Test checklist

1. Run:

```powershell
python dashboard.py
```

2. Open:

```text
http://127.0.0.1:8765
```

3. Test:

```text
Add a task
Mark a task done
Add a learning topic
Add a reminder
Fetch /news ai
Search /research AI agents in education
```

4. Stop server with:

```text
Ctrl + C
```

## Commit

```powershell
git status
git add .
git commit -m "Add local dashboard UI"
```

## What you learned

- A local web server can serve a dashboard from Python.
- APIs can connect a web page to local JSON files.
- The same data can be used by both terminal commands and a browser UI.
- A good assistant can have multiple interfaces: CLI now, dashboard next, voice later.

## Next sprint options

- Make dashboard prettier and more interactive.
- Add smart-home prep with Home Assistant placeholders.
- Connect the real AI brain.
- Add speech input.
