"""AyAstra / QuantaCore terminal app.

Run with:
    python main.py

This is the first beginner-friendly version: a terminal chat loop with tools.
"""

from quantacore.assistant import handle_message
from quantacore.personality import banner, style_reply
from quantacore.tools.reminders import get_due_reminders
from quantacore.tools.voice import speak_response


def show_due_reminders() -> None:
    due_reminders = get_due_reminders()
    for reminder in due_reminders:
        print(style_reply(f"⏰ {reminder}"))


def main() -> None:
    print(banner())
    print()
    """AyAstra / QuantaCore terminal app.

Run with:
    python main.py

This is the beginner-friendly terminal app: a chat loop with tools.
"""

from quantacore.assistant import handle_message
from quantacore.personality import banner, style_reply
from quantacore.tools.reminders import get_due_reminders
from quantacore.tools.voice import speak_response


def show_due_reminders() -> None:
    due_reminders = get_due_reminders()
    for reminder in due_reminders:
        response = style_reply(f"⏰ {reminder}")
        print(response)
        _speak_if_enabled(response)


def _speak_if_enabled(response: str) -> None:
    """Speak a response if voice output is enabled."""

    voice_error = speak_response(response)
    if voice_error:
        print(style_reply(f"Voice warning: {voice_error}"))


def main() -> None:
    print(banner())
    print()

    while True:
        show_due_reminders()
        user_message = input("You: ")
        response = handle_message(user_message)

        if response == "__EXIT__":
            exit_response = style_reply("Powering down. Go drink water, Ayanda. Even geniuses need hydration.")
            print(exit_response)
            _speak_if_enabled(exit_response)
            break

        print(response)
        _speak_if_enabled(response)
        print()


if __name__ == "__main__":
    main()


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
