"""Run the AyAstra / QuantaCore local dashboard.

Usage:
    python dashboard.py

Then open:
    http://127.0.0.1:8765
"""

from ay_astra.dashboard import run_dashboard


if __name__ == "__main__":
    run_dashboard()
