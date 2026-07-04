"""Voice output tool for AyAstra.

Beginner explanation:
Text-to-speech, or TTS, means the computer reads text out loud.
This tool uses `pyttsx3` when it is installed. `pyttsx3` is beginner-friendly
because it can use voices already available on your computer.

Important:
Voice is optional. AyAstra must still run even if the TTS package is missing.
"""

from __future__ import annotations

import importlib.util
import re
from typing import Any

VOICE_MAX_CHARS = 700
VOICE_RATE = 185
VOICE_VOLUME = 0.95

_VOICE_ENABLED = False
_ENGINE: Any | None = None


def handle_voice_command(message: str) -> str:
    """Route `/voice` commands."""

    command = message.strip().lower()

    if command in {"/voice", "/voice help"}:
        return voice_help()

    if command == "/voice status":
        return voice_status()

    if command == "/voice on":
        return set_voice_enabled(True)

    if command == "/voice off":
        return set_voice_enabled(False)

    if command == "/voice test":
        return test_voice()

    return "Voice command not recognized. Try /voice help."


def voice_help() -> str:
    return """
Voice commands:
/voice help              Show this menu
/voice status            Check whether voice output is available/enabled
/voice on                Turn voice output on for this session
/voice off               Turn voice output off
/voice test              Speak a short test line

Note:
Voice resets to off when you restart AyAstra. That is intentional for now, because surprise talking laptops are how trust issues begin.
""".strip()


def voice_status() -> str:
    available = _is_pyttsx3_available()
    enabled = "on" if _VOICE_ENABLED else "off"
    package_status = "installed" if available else "not installed"

    lines = [
        "Voice output status:",
        f"- Voice for this session: {enabled}",
        f"- pyttsx3 package: {package_status}",
    ]

    if not available:
        lines.extend(
            [
                "",
                "To install voice support, exit AyAstra and run:",
                "pip install pyttsx3",
                "",
                "Then start AyAstra again with:",
                "python main.py",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "Try:",
                "/voice test",
                "/voice on",
            ]
        )

    return "\n".join(lines)


def set_voice_enabled(enabled: bool) -> str:
    """Turn voice output on/off for the current session."""

    global _VOICE_ENABLED

    if enabled:
        if not _is_pyttsx3_available():
            _VOICE_ENABLED = False
            return (
                "Voice output is not available yet because `pyttsx3` is not installed.\n\n"
                "Exit AyAstra, then run:\n"
                "pip install pyttsx3\n\n"
                "Then start again with:\n"
                "python main.py"
            )

        error = _warm_up_engine()
        if error:
            _VOICE_ENABLED = False
            return f"I found pyttsx3, but the voice engine failed to start. Reason: {error}"

        _VOICE_ENABLED = True
        return "Voice output enabled for this session. AyAstra can speak now. The lab finally has audio."

    _VOICE_ENABLED = False
    return "Voice output disabled. Silent mode active. Very stealthy."


def test_voice() -> str:
    """Speak a short test line without permanently changing the voice setting."""

    if not _is_pyttsx3_available():
        return (
            "Voice test unavailable because `pyttsx3` is not installed.\n"
            "Exit AyAstra and run: pip install pyttsx3"
        )

    error = _speak_now("AyAstra voice test successful. QuantaCore audio systems are awake.")

    if error:
        return f"Voice test failed. Reason: {error}"

    return "Voice test sent. If you heard me, QuantaCore audio systems are awake."


def speak_response(response_text: str) -> str | None:
    """Speak an assistant response when voice output is enabled.

    Returns an error message if speech fails, otherwise None.
    """

    if not _VOICE_ENABLED:
        return None

    text = _clean_for_speech(response_text)

    if not text:
        return None

    return _speak_now(text)


def _is_pyttsx3_available() -> bool:
    return importlib.util.find_spec("pyttsx3") is not None


def _warm_up_engine() -> str | None:
    try:
        _get_engine()
        return None
    except Exception as error:  # Keep AyAstra alive even when audio fails.
        return str(error)


def _get_engine() -> Any:
    global _ENGINE

    if _ENGINE is not None:
        return _ENGINE

    import pyttsx3  # Imported lazily so AyAstra works without the package.

    engine = pyttsx3.init()
    engine.setProperty("rate", VOICE_RATE)
    engine.setProperty("volume", VOICE_VOLUME)
    _ENGINE = engine
    return _ENGINE


def _speak_now(text: str) -> str | None:
    try:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
        return None
    except Exception as error:
        return str(error)


def _clean_for_speech(text: str) -> str:
    """Make terminal output easier to speak aloud."""

    cleaned = text.strip()
    cleaned = re.sub(r"^AyAstra:\s*", "", cleaned)
    cleaned = re.sub(r"https?://\S+", "link available in the terminal", cleaned)
    cleaned = cleaned.replace("/", " slash ")
    cleaned = re.sub(r"[`*_>#|=]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if len(cleaned) > VOICE_MAX_CHARS:
        cleaned = (
            cleaned[:VOICE_MAX_CHARS].rstrip()
            + "... I left the full details in the terminal. Obviously I am not reading the whole scroll like a royal decree."
        )

    return cleaned
