"""Run AyAstra's focused LLM-style assistant UI.

Usage:
    python assistant_ui.py

Then open:
    http://127.0.0.1:8765
"""

from ay_astra.assistant_ui import run_assistant_ui


if __name__ == "__main__":
    run_assistant_ui()