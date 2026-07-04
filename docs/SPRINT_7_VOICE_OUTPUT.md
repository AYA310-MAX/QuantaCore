# Sprint 7 — Voice Output

Sprint 7 gives AyAstra optional text-to-speech voice output.

## Child-level explanation

Before this sprint, AyAstra could type replies.

Now, AyAstra can also read replies out loud.

That is called **text-to-speech** or **TTS**.

For this beginner version, we use:

```text
pyttsx3
```

`pyttsx3` uses voices already available on your computer, so it does not need an API key.

## Important

Voice is optional.

AyAstra still works even if voice is not installed or turned on.

Voice starts **off** every time you open AyAstra. This prevents surprise laptop speeches in public. You are welcome.

## Step 1: Make sure your virtual environment is active

Your terminal should show:

```text
(.venv)
```

## Step 2: Install requirements

Exit AyAstra first if it is running, then run:

```powershell
pip install -r requirements.txt
```

This installs `pyttsx3`.

If that gives issues, try:

```powershell
pip install pyttsx3
```

## Step 3: Run AyAstra

```powershell
python main.py
```

## Step 4: Test voice commands inside AyAstra

```text
/voice status
/voice test
/voice on
hello
/voice off
```

## Voice commands

```text
/voice help
/voice status
/voice on
/voice off
/voice test
```

## What to expect

- `/voice status` tells you if `pyttsx3` is installed.
- `/voice test` speaks a short test line.
- `/voice on` makes AyAstra speak replies.
- `/voice off` returns to silent mode.

## If no sound plays

Check:

1. Your laptop volume is on.
2. Windows output device is correct.
3. You installed `pyttsx3` inside the active `.venv`.
4. You restarted AyAstra after installing.

Run:

```powershell
pip show pyttsx3
```

If it shows package details, it is installed.

## Step 5: Commit this sprint

```powershell
git status
git add .
git commit -m "Add optional voice output"
```

## What you learned

- Text-to-speech turns text into spoken audio.
- Optional features should not break the whole app if a package is missing.
- Voice output belongs in `main.py` because that is where responses are printed.
- Voice commands belong in a tool file so the code stays organised.

## Future upgrades

- Pick a different system voice.
- Add voice speed/volume commands.
- Add speech-to-text input.
- Add a wake word like “AyAstra” or “QuantaCore”.
- Use a more natural cloud TTS voice later if budget allows.
