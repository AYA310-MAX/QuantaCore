# Setup AyAstra / QuantaCore in VS Code

This guide assumes you are a beginner to AI agents but comfortable enough with basic coding.

## 1. Install the tools

Install these first:

1. **Python 3.11 or newer**
   - Download: https://www.python.org/downloads/
   - During installation on Windows, tick **Add Python to PATH**.

2. **Visual Studio Code**
   - Download: https://code.visualstudio.com/

3. **Git**
   - Download: https://git-scm.com/downloads

4. **GitHub account**
   - Create one if you do not have one: https://github.com/

## 2. Open the project in VS Code

1. Open VS Code.
2. Click **File > Open Folder**.
3. Select the folder named:

```text
ay-astra-quantacore
```

4. Open the terminal in VS Code:

```text
Terminal > New Terminal
```

## 3. Check Python works

In the VS Code terminal, run:

```bash
python --version
```

If that does not work, try:

```bash
python3 --version
```

You should see something like:

```text
Python 3.11.x
```

## 4. Create a virtual environment

A virtual environment is a private Python setup for this project.

### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When it works, your terminal should show `(.venv)`.

## 5. Install requirements

For this starter sprint, there are no external packages yet, but still run:

```bash
pip install -r requirements.txt
```

## 6. Run AyAstra

Run:

```bash
python main.py
```

or:

```bash
python3 main.py
```

You should see:

```text
AyAstra online — QuantaCore core active
```

## 7. Test commands

Try:

```text
/help
/task add Finish AI assignment
/task list
/task done 1
/remind add 2026-06-14 18:00 Review AI agents notes
/remind list
/tutor APIs
/news AI
/research AI agents in education
/exit
```

## 8. Make your first Git commit

In the terminal:

```bash
git init
git add .
git commit -m "Initialize AyAstra QuantaCore project"
```

## 9. Push to GitHub

Create a new empty GitHub repo called:

```text
ay-astra-quantacore
```

Then run these commands, replacing `YOUR_USERNAME`:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ay-astra-quantacore.git
git branch -M main
git push -u origin main
```

## 10. What you learned

- How to open a Python project in VS Code.
- How to run a terminal assistant.
- How commands are routed to tools.
- How tasks and reminders can be stored in JSON.
- Why AyAstra must not answer live news/research without valid sources.

Next sprint: connect an LLM API for smarter conversation.
