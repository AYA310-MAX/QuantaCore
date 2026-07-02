# Sprint 5 — Learning Log

Sprint 5 gives AyAstra a basic long-term study tracker.

## Child-level explanation

Short-term chat memory is like remembering what you said in one conversation.

The learning log is like a notebook AyAstra keeps in a file.

When you study something, you can save it:

```text
/learn add APIs | Learned that APIs let apps talk to each other
```

AyAstra stores it in:

```text
data/learning_log.json
```

## Commands

```text
/learn help
/learn add TOPIC
/learn add TOPIC | NOTE
/learn list
/learn review
/learn reviewed ID
```

## Examples

```text
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
```

## Why this matters

AyAstra should become your learning partner, not just a chatbot.

This feature helps AyAstra track:

- what you studied,
- notes about the topic,
- how many times you reviewed it,
- when you last reviewed it.

## Step 1: Make sure your venv is active

Your terminal should show:

```text
(.venv)
```

## Step 2: Run AyAstra

```powershell
python main.py
```

## Step 3: Test Learning Log

Inside AyAstra:

```text
/learn help
/learn add APIs | Learned that APIs let apps talk to each other
/learn add Python classes | Classes group data and behaviour together
/learn list
/learn review
/learn reviewed 1
/learn list
```

## Step 4: Commit this sprint

```powershell
git status
git add .
git commit -m "Add learning log tool"
```

## What you learned

- Long-term storage means saving data to a file.
- JSON can store structured learning entries.
- Assistant tools can help with study habits, not just answering questions.
- Reviewing topics repeatedly is better than cramming like a panicked raccoon.

## Next sprint options

- Add simple quizzes based on learning-log topics.
- Connect Tutor Mode to automatically suggest saving topics.
- Add a dashboard for tasks, news, research, and learning.
- Add voice output.
