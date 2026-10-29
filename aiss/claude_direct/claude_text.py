"""Helpers that request plain text responses from the Anthropic SDK.

This module demonstrates the "text" query flow where the model's raw
text output is printed inside a Rich Panel. It's intended for quick
inspection rather than structured parsing.
"""

from typing import Type, TypeVar, cast

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from aiss.models.protocols import ModelFormatProtocol
from aiss.models.shared import ModelTypeInput
from aiss.openai_direct.wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)

from ._common import MAX_TOKENS, check_refusal, extract_text_from_response, get_model_name

load_dotenv()

# MARK: Text Response Helper
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_text_response(
    model_type_result: ModelTypeInput,
    client: Anthropic,
    console: Console,
    text_format: Type[T] | None = None,
) -> None:
    """Render plain-text output for a detected model type."""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Building Wikipedia context", total=4)

        text_format = cast(Type[T], text_format or model_type_result.model_type.get_model_from_name())
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
        progress.update(task, description="Requesting text response", advance=1)
        response = client.messages.create(
            model=get_model_name(),
            max_tokens=MAX_TOKENS,
            system=instructions,
            messages=[{"role": "user", "content": text_format.get_user_prompt(model_type_result.formatted_name)}],
        )

        if check_refusal(response, console, model_type_result.formatted_name):
            return

        progress.update(task, description="Rendering text", advance=1)
        console.rule(f"[bold cyan]{model_type_result.formatted_name}")

        plain_text = extract_text_from_response(response)
        console.print(Panel(plain_text, title="Information (Text)", expand=False, style="green"))
