"""Helpers for asking the model to emit JSON and rendering it.

This module asks the model to return JSON (using system/user messages with a
json schema prompt) and then parses and renders that JSON via
`aiss.utils.render_from_json`.
"""

import json
import re
from typing import TYPE_CHECKING, Type, TypeVar, cast

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console

from aiss.models.protocols import ModelFormatProtocol
from aiss.models.shared import ModelType, ModelTypeResult
from aiss.utils import render_from_json

from .wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)

if TYPE_CHECKING:
    from openai.types.responses.response import Response

load_dotenv()

# MARK: JSON Response Helper
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def _extract_text_from_response(response) -> str:
    # Safely extract plain text from common SDK response shapes.
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    try:
        parts = []
        for item in getattr(response, "output", []) or []:
            content = item.get("content") if isinstance(item, dict) else None
            if content:
                for c in content:
                    if isinstance(c, dict):
                        t = c.get("text") or c.get("content")
                        if t:
                            parts.append(t)
                    elif isinstance(c, str):
                        parts.append(c)
        return "\n".join(parts)
    except Exception:
        return ""


def _model_type_for_format(format_cls: Type[ModelFormatProtocol]) -> ModelType:
    for candidate in ModelType:
        try:
            if candidate.get_model_from_name() is format_cls:
                return candidate
        except ValueError:
            continue
    return ModelType.SHOW


def get_json_response(
    model_type_result: ModelTypeResult,
    client: OpenAI,
    console: Console,
):
    """Render JSON output for a detected model type."""

    text_format = cast(Type[T], model_type_result.model_type.get_model_from_name())
    wikipedia_summary, context_hint = build_wikipedia_topic_context(text_format, model_type_result)
    instructions = augment_instructions_with_tool_hint(
        text_format.get_instructions(model_type_result.additional_info),
        wikipedia_summary,
        context_hint,
    )

    response: Response = client.responses.create(
        model="gpt-5-mini",
        instructions=instructions,
        input=text_format.get_user_prompt(model_type_result.formatted_name),
        timeout=Timeout(4000, connect=6.0),
    )

    raw = _extract_text_from_response(response)

    data = None
    if raw:
        try:
            data = json.loads(raw)
        except Exception:
            m = re.search(r"(\{(?:.|\n)*\}|\[(?:.|\n)*\])", raw)
            if m:
                try:
                    data = json.loads(m.group(1))
                except Exception:
                    data = None

    if data is None:
        console.print(f"[red]Failed to parse JSON output for '{model_type_result.formatted_name}'[/red]")
        return

    console.rule(f"[bold cyan]{model_type_result.formatted_name}")
    try:
        render_from_json(data, console)
    except Exception as exc:
        console.print(f"[red]Rendering JSON failed: {exc}[/red]")

    console.print("\n")
