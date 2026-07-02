# Sprint 4 — Source-Backed Research Mode

Sprint 4 gives AyAstra a real `/research` command using Semantic Scholar.

## Child-level explanation

Imagine a huge library catalogue for research papers.

Semantic Scholar is one of those catalogues. AyAstra asks it:

> "Show me papers about this topic."

Then AyAstra returns paper metadata:

- title
- authors
- year/date
- venue
- abstract when available
- citation count
- links
- open-access PDF link when available

## Important truth rule

AyAstra is not pretending to have read the full paper.

For now, she is reading the catalogue card and abstract.

So the correct wording is:

```text
Based on source metadata and abstract...
```

Not:

```text
This paper definitely proves...
```

Tiny academic detail. Massive difference.

## Step 1: Make sure your venv is active

Your terminal should show:

```text
(.venv)
```

## Step 2: Run AyAstra

```powershell
python main.py
```

## Step 3: Test Research Mode

Inside AyAstra, run:

```text
/research sources
```

Then:

```text
/research AI agents in education
```

Then:

```text
/research CRISPR gene editing
```

Then:

```text
/research machine learning cybersecurity
```

## Step 4: Read the output carefully

Each result should include:

```text
Title
Authors
Year/date
Venue
Citation count
Abstract/summary from source
Link
Open PDF if available
```

## Step 5: Commit this sprint

```powershell
git status
git add .
git commit -m "Add source-backed research mode"
```

## What you learned

- Research Mode should use sources, not guesses.
- A paper's metadata and abstract are useful, but they are not the same as reading the full paper.
- APIs let AyAstra connect to external knowledge systems.
- Good research assistants clearly separate source facts from interpretation.

## Next sprint options

- Let AyAstra explain fetched abstracts in beginner language using the optional LLM brain.
- Add PDF upload/summarisation.
- Save research results to a learning log.
- Add citation export in APA/IEEE style.
