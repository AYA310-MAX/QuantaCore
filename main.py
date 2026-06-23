"""AyAstra / QuantaCore terminal app.

Run with:
    python main.py

This is the first beginner-friendly version: a terminal chat loop with tools.
"""

from ay_astra.assistant import handle_message
from ay_astra.personality import banner, style_reply
from ay_astra.tools.reminders import get_due_reminders


def show_due_reminders() -> None:
    due_reminders = get_due_reminders()
    for reminder in due_reminders:
        print(style_reply(f"⏰ {reminder}"))


def main() -> None:
    print(banner())
    print()

    while True:
        show_due_reminders()
        user_message = input("You: ")
        response = handle_message(user_message)

        if response == "__EXIT__":
            print(style_reply("Powering down. Go drink water, Ayanda. Even geniuses need hydration."))
            break

        print(response)
        print()


if __name__ == "__main__":
    main()
