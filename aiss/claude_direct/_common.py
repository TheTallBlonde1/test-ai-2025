"""Shared helpers for the Claude (Anthropic) direct flows."""

import os
from typing import Any

from rich.console import Console

DEFAULT_CLAUDE_MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 16000


def get_model_name() -> str:
    """Return the Claude model name from the environment (or the default)."""
    return os.getenv("ANTHROPIC_MODEL_NAME") or DEFAULT_CLAUDE_MODEL


def extract_text_from_response(response: Any) -> str:
    """Join the text blocks of a Messages API response (skipping thinking/tool blocks)."""
    parts = [
        block.text
        for block in getattr(response, "content", None) or []
        if getattr(block, "type", None) == "text" and getattr(block, "text", None)
    ]
    return "\n".join(parts)


def check_refusal(response: Any, console: Console, name: str) -> bool:
    """Print an error and return True when the response was a safety refusal."""
    if getattr(response, "stop_reason", None) == "refusal":
        console.print(f"[red]Claude declined the request for '{name}'[/red]")
        return True
    return False
