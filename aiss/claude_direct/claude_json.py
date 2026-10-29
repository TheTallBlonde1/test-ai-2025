"""Helpers for asking Claude to emit JSON and rendering it.

This module asks the model to return JSON (using a system prompt with a json
schema) and then parses and renders that JSON via `aiss.utils.render_from_json`.
"""

import json
import re
from typing import Type, TypeVar, cast

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from aiss.models.protocols import ModelFormatProtocol
from aiss.models.shared import ModelTypeInput
from aiss.openai_direct.wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)
from aiss.utils import render_from_json

from ._common import MAX_TOKENS, check_refusal, extract_text_from_response, get_model_name

load_dotenv()

# MARK: JSON Response Helper
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_json_response(
    model_type_result: ModelTypeInput,
    client: Anthropic,
    console: Console,
):
    """Render JSON output for a detected model type."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Building Wikipedia context", total=5)

        text_format = cast(Type[T], model_type_result.model_type.get_model_from_name())
        try:
            wikipedia_summary, context_hint = build_wikipedia_topic_context(text_format, model_type_result)
        except Exception as e:
            console.print(f"[warn]Failed to build Wikipedia context: {e}[/warn]")
            wikipedia_summary, context_hint = "", ""
        progress.update(task, description="Composing instructions", advance=1)

        instructions = augment_instructions_with_tool_hint(
            text_format.get_instructions(model_type_result.additional_info),
            wikipedia_summary,
            context_hint,
        )

        progress.update(task, description="Requesting JSON response", advance=1)
        response = client.messages.create(
            model=get_model_name(),
            max_tokens=MAX_TOKENS,
            system=instructions,
            messages=[{"role": "user", "content": text_format.get_user_prompt(model_type_result.formatted_name)}],
        )

        if check_refusal(response, console, model_type_result.formatted_name):
            return

        progress.update(task, description="Parsing JSON output", advance=1)
        raw = extract_text_from_response(response)

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

        progress.update(task, description="Rendering JSON", advance=1)
        console.rule(f"[bold cyan]{model_type_result.formatted_name}")
        try:
            render_from_json(data, console)
        except Exception as exc:
            console.print(f"[red]Rendering JSON failed: {exc}[/red]")

        console.print("\n")
