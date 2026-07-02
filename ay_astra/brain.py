"""AyAstra's optional AI brain.

This is the beginner-safe version.
It keeps AyAstra running even before we connect a real LLM API.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AIReply:
    """The response from AyAstra's brain."""

    text: str
    used_llm: bool = False
    error: str | None = None


class AIBrain:
    """Temporary beginner-friendly AI brain.

    Later, this class will connect to a real LLM API.
    For now, it gives safe fallback replies so AyAstra can run.
    """

    def is_configured(self) -> bool:
        return False

    def status_text(self) -> str:
        return (
            "AI brain status: not connected yet.\n"
            "AyAstra can still use local commands like /task, /remind, /news, and /tutor.\n\n"
            "Later we will connect an LLM using a private `.env` file.\n"
            "Do not put API keys directly in the code. The internet has sticky fingers."
        )

    def generate(
        self,
        user_message: str,
        *,
        mode: str = "chat",
        history: list[dict[str, str]] | None = None,
    ) -> AIReply:
        if mode == "tutor":
            return AIReply(
                text=(
                    "Tutor Mode is awake, but the full AI brain is not connected yet.\n\n"
                    f"Topic/request: {user_message}\n\n"
                    "Here is the learning structure we will use:\n"
                    "1. Plain-English definition\n"
                    "2. Real-world analogy\n"
                    "3. Small example\n"
                    "4. Common mistakes\n"
                    "5. Mini quiz\n\n"
                    "Next upgrade: connect a real LLM so I can generate deeper lessons dynamically."
                )
            )

        return AIReply(
            text=(
                "I hear you. My local tools are online, but the larger AI brain is not connected yet.\n"
                "Use /help to see what I can do now.\n"
                "Step by step, Ayanda. Even royal labs start with a power switch."
            )
        )