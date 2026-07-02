# Sprint 3 — Verified News Mode

Sprint 3 gives AyAstra a real source-backed `/news` command using RSS/Atom feeds.

## Child-level explanation

Imagine every trusted news website has a public notice board.

RSS is that notice board in a format code can read.

AyAstra now checks those notice boards and shows:

- headline
- source name
- publication date from the feed
- short feed summary
- article link

This helps AyAstra avoid making up news.

## What works now

Try these commands inside AyAstra:

```text
/news tech
/news ai
/news south africa
/news software
/news cybersecurity
/news sources
```

## Important truth rule

AyAstra is not "thinking up" headlines.
It fetches them from configured source feeds.

If a feed is down or the internet is unavailable, AyAstra should say that instead of pretending.

## Current configured feeds

- BBC News — Technology
- The Verge
- Ars Technica
- Hacker News Front Page
- TechCentral South Africa

These are starter feeds. Later we can add more South African sources, biotech/science feeds, research feeds, and official company blogs.

## Step 1: Make sure your venv is active

Your terminal should show:

```text
(.venv)
```

## Step 2: Run AyAstra

```powershell
python main.py
```

## Step 3: Test the news tool

Inside AyAstra, run:

```text
/news sources
```

Then:

```text
/news tech
```

Then:

```text
/news ai
```

Then:

```text
/news south africa
```

## Step 4: Read the output carefully

Each item should include:

```text
Title
Source
Published date
Summary from feed
Link
```

That is the no-hallucination habit we want.

## Step 5: Commit this sprint

```powershell
git status
git add .
git commit -m "Add verified RSS news mode"
```

## What you learned

- RSS/Atom feeds are machine-readable news feeds.
- Verified source-backed output is safer than asking an LLM to guess.
- AyAstra should cite links for current information.
- Not all websites allow direct feed access; tools must handle errors gracefully.

## Next sprint options

- Improve Research Mode with academic/source search.
- Connect the optional LLM brain to summarize only the fetched news text.
- Add more South African and biotech/science feeds.
- Build a small dashboard interface.
