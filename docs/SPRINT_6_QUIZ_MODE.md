# Sprint 6 — Quiz Mode

Sprint 6 gives AyAstra a simple active-recall quiz mode.

## Child-level explanation

Reading notes is like looking at food.

Quizzing yourself is like eating the food.

Your brain learns better when it has to pull information out, not just stare at notes and hope magic happens.

## What Quiz Mode does

AyAstra can:

- pick a topic from your learning log,
- ask study questions,
- save your answers during the session,
- remind you to mark the topic reviewed.

For now, AyAstra does **not** fully grade your answers automatically. That will come later when we connect the AI brain for feedback.

## Commands

```text
/quiz help
/quiz start
/quiz topic TOPIC
/quiz current
/quiz answer YOUR ANSWER
/quiz stop
```

## Examples

```text
/learn add APIs | APIs let apps talk to each other
/quiz start
/quiz answer An API is a set of rules that lets software communicate.
/quiz answer It matters because apps can request data or services from other apps.
/quiz answer Example: a weather app calling a weather API.
/quiz answer A common mistake is thinking an API is only a database.
/learn reviewed 1
```

Or quiz any topic:

```text
/quiz topic Python classes
/quiz answer A class is a blueprint for creating objects.
```

## Step 1: Make sure your venv is active

Your terminal should show:

```text
(.venv)
```

## Step 2: Run AyAstra

```powershell
python main.py
```

## Step 3: Test Quiz Mode

Inside AyAstra:

```text
/learn add APIs | APIs let apps talk to each other
/quiz start
/quiz answer An API is a set of rules that lets programs communicate.
/quiz answer It matters because apps can share data and services.
/quiz answer A weather app using a weather service.
/quiz answer Thinking an API is only a database.
/learn reviewed 1
```

## Step 4: Commit this sprint

```powershell
git status
git add .
git commit -m "Add quiz mode for learning log topics"
```

## What you learned

- Active recall is stronger than passive rereading.
- A tool can keep short quiz state in memory while the app is running.
- Learning tools can connect together: `/learn` stores topics, `/quiz` practises them.
- Automatic grading should be added carefully so AyAstra does not pretend to understand answers without enough logic or an LLM.

## Next sprint options

- Add AI-powered answer feedback once the LLM brain is connected.
- Add voice output.
- Build a dashboard UI.
- Start smart-home integration planning.
