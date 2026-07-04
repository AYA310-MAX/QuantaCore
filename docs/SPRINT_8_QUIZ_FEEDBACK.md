# Sprint 8 — Quiz Feedback

Sprint 8 improves Quiz Mode so AyAstra can give feedback on your completed quiz answers.

## Child-level explanation

Before this sprint, AyAstra could ask quiz questions and save your answers.

Now, after a quiz, you can ask:

```text
/quiz feedback
```

AyAstra will review your answers.

If the optional AI brain is connected, AyAstra uses it for more detailed feedback.

If the AI brain is not connected, AyAstra uses a rule-based checklist.

## Why this is useful

Quizzing is good.

Feedback is better.

Feedback tells you what to improve instead of just letting you confidently be wrong. Painful, but productive.

## New command

```text
/quiz feedback
```

## Test flow

Inside AyAstra:

```text
/learn add APIs | APIs let apps talk to each other
/quiz start
/quiz answer An API lets programs communicate.
/quiz answer It matters because apps can share data and services.
/quiz answer A weather app calls a weather API.
/quiz answer Thinking an API is the same as a database.
/quiz feedback
/learn reviewed 1
```

## How feedback works

### If LLM brain is connected

AyAstra sends your quiz questions and answers to the optional AI brain and asks for:

- what was good,
- what needs improvement,
- stronger phrasing,
- revision tips,
- a mini-challenge.

### If LLM brain is not connected

AyAstra uses rule-based feedback:

- checks if answers are very short,
- encourages examples,
- suggests the structure: definition → why it matters → example → common mistake.

## Important honesty rule

Rule-based feedback is not deep grading.

It is a helpful checklist, not a professor with coffee and a marking rubric.

## Commit this sprint

```powershell
git status
git add .
git commit -m "Add quiz feedback command"
```

## Next sprint options

- Connect the real LLM brain.
- Build a dashboard UI.
- Add speech input.
- Start smart-home prep.
