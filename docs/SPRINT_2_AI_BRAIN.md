Sprint 2 — Connect AyAstra's Optional AI Brain
AyAstra already runs locally. Sprint 2 adds an optional LLM brain so normal chat and Tutor Mode can become smarter.

Child-level explanation
Right now AyAstra has:

text

body = terminal app
hands = tools like tasks/reminders
personality = AyAstra/Shuri-inspired style
The LLM brain is like adding a bigger thinking engine.

But the brain has rules:

It may help explain stable concepts.
It may help with coding and studying.
It must not invent live news or research sources.
Current facts must go through verified source tools later.
Step 1: Make sure your virtual environment is active
Your terminal should begin with:

text

(.venv)
If not, activate it:

PowerShell

.\.venv\Scripts\Activate.ps1
Step 2: Run AyAstra without an LLM first
PowerShell

python main.py
Inside AyAstra:

text

/brain status
You should see that the AI brain is not connected yet. That is okay.

Exit:

text

/exit
Step 3: Create your private .env file
In VS Code:

Right-click .env.example.
Copy it.
Paste it in the same folder.
Rename the copy to:
text

.env
Do not rename .env.example; make a copy.

Step 4: Add your LLM settings
Open .env and fill in:

text

LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name-here
LLM_API_KEY=your-private-api-key-here
LLM_TIMEOUT_SECONDS=30
The starter code expects an OpenAI-compatible chat completions API.

Ask before choosing a provider if you are unsure. Student budget matters; we do not spend money accidentally in this lab.

Step 5: Run AyAstra again
PowerShell

python main.py
Check the brain:

text

/brain status
If configured, it should show:

text

AI brain status: connected settings found.
Step 6: Test smarter chat
Try:

text

Explain APIs like I am new to software engineering
Then:

text

/tutor Python classes
Then test truth protocol:

text

What is the latest AI news today?
AyAstra should not hallucinate live news. It should direct that kind of request to future verified source tools.

Step 7: Commit your work
After testing:

PowerShell

git status
git add .
git commit -m "Add optional AI brain configuration"
Important: .env should not appear in the commit because .gitignore protects it.

Check with:

PowerShell

git status
If .env appears, stop and ask for help before committing.

What you learned
What an LLM brain is.
Why API keys must stay private.
How .env stores private settings.
How AyAstra uses local tools plus optional AI replies.
Why current facts need verified source tools instead of memory.
