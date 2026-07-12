"""AyAstra's optional AI brain.

Beginner explanation:
The first version of AyAstra used simple if-statements.
This file lets AyAstra optionally call a real LLM API for smarter replies.

Important safety idea:
The LLM is NOT allowed to invent live news, current tech updates, research
sources, prices, laws, medical facts, or anything that needs verification.
Those must go through source tools in later sprints.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Literal

from quantacore.config import AppConfig, load_config
from quantacore.personality import PERSONALITY_SUMMARY

BrainMode = Literal["chat", "tutor"]


@dataclass
class AIReply:
    """The response from AyAstra's brain."""

    text: str
    used_llm: bool
    error: str | None = None


class AIBrain:
    """Small OpenAI-compatible LLM client.

    "OpenAI-compatible" means many services use the same `/chat/completions`
    shape. Later, you can point this to different providers by changing `.env`.
    """

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or load_config()

    def is_configured(self) -> bool:
        """Return True when AyAstra has enough settings to call an LLM."""

        return bool(self.config.llm_api_key and self.config.llm_model and self.config.llm_base_url)

    def status_text(self) -> str:
        """Human-readable status for the `/brain status` command."""

        if self.is_configured():
            return (
                "AI brain status: connected settings found.\n"
                f"- Base URL: {self.config.llm_base_url}\n"
                f"- Model: {self.config.llm_model}\n"
                "- API key: loaded privately from environment/.env"
            )

        return (
            "AI brain status: not connected yet.\n"
            "AyAstra can still use local commands like /task, /remind, and /tutor.\n\n"
            "To connect an LLM, create a private `.env` file using `.env.example` as a guide.\n"
            "Do not commit `.env` to GitHub. Ever. The internet has sticky fingers."
        )

    def generate(
        self,
        user_message: str,
        *,
        mode: BrainMode = "chat",
        history: list[dict[str, str]] | None = None,
    ) -> AIReply:
        """Generate a reply using an LLM when configured, otherwise use fallback."""

        if not self.is_configured():
            return AIReply(text=self._fallback_reply(user_message, mode), used_llm=False)

        messages = self._build_messages(user_message, mode=mode, history=history or [])

        try:
            text = self._call_openai_compatible_api(messages)
            return AIReply(text=text, used_llm=True)
        except Exception as error:  # Keep the app alive while we learn.
            fallback = self._fallback_reply(user_message, mode)
            return AIReply(
                text=(
                    f"{fallback}\n\n"
                    "Tiny lab warning: I tried to call the AI brain, but the API call failed.\n"
                    f"Reason: {error}"
                ),
                used_llm=False,
                error=str(error),
            )

    def _build_messages(
        self,
        user_message: str,
        *,
        mode: BrainMode,
        history: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        system_prompt = _system_prompt_for_mode(mode)

        # Keep only recent session memory so prompts do not grow forever.
        recent_history = history[-12:]

        return [
            {"role": "system", "content": system_prompt},
            *recent_history,
            {"role": "user", "content": user_message},
        ]

    def _call_openai_compatible_api(self, messages: list[dict[str, str]]) -> str:
        url = f"{self.config.llm_base_url}/chat/completions"

        payload = {
            "model": self.config.llm_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 900,
        }

        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.llm_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.config.llm_timeout_seconds) as response:
                response_text = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {error.code}: {body}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"Network error: {error.reason}") from error

        data = json.loads(response_text)

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(f"Unexpected API response: {data}") from error

    def _fallback_reply(self, user_message: str, mode: BrainMode) -> str:
        if mode == "tutor":
            return (
                "Tutor Mode is awake, but the full AI brain is not connected yet.\n\n"
                f"Topic/request: {user_message}\n\n"
                "Here is the learning structure we will use:\n"
                "1. Plain-English definition\n"
                "2. Real-world analogy\n"
                "3. Small example\n"
                "4. Common mistakes\n"
                "5. Mini quiz\n\n"
                "Connect an LLM in Sprint 2 and I will generate the full lesson dynamically."
            )

        return (
            "I hear you. My local tools are online, but the larger AI brain is not connected yet.\n"
            "Use /help to see what I can do now, or connect an LLM with a private `.env` file.\n"
            "Step by step, Ayanda. Even royal labs start with a power switch."
        )


def _system_prompt_for_mode(mode: BrainMode) -> str:
    mode_instructions = {
        "chat": (
            "Mode: normal assistant conversation. Be helpful, concise, warm, and witty. "
            "If the user asks for current/recent/live facts, tell them this needs verified source tools."
        ),
        "tutor": (
            "Mode: tutor. Teach step by step. Use simple explanations, analogies, examples, "
            "and a short quiz. Be patient and encouraging."
        ),
    }

    return f"""
{PERSONALITY_SUMMARY}

Current project date: 2026-07-02.
User timezone/context: South Africa, Africa/Johannesburg.

{mode_instructions[mode]}

Critical output rules:
- Do not begin with "AyAstra:" because the terminal app adds that prefix.
- Do not pretend you can browse the web from this chat call.
- Do not invent sources, citations, current news, recent releases, prices, laws, medical guidance, or research-paper details.
- If an answer needs current verification, say it needs `/news` or `/research` once source tools are connected.
- For coding and study help, explain clearly and give practical examples.
""".strip()
