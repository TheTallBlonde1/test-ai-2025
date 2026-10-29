"""Helpers to query Claude's messages.parse endpoint and render parsed models.

This module provides typed helpers that accept a "text format" class (for
example a genre-specific `*ShowInfo` or one of the movie formats) and call the
Anthropic SDK `messages.parse` endpoint (structured outputs), rendering the
parsed Pydantic model to the console.
"""

from typing import Optional, Type, TypeVar, cast

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from aiss.models import ModelTypeInput
from aiss.models.protocols import ModelFormatProtocol
from aiss.openai_direct.wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)

from ._common import MAX_TOKENS, check_refusal, get_model_name

load_dotenv()

# MARK: Parsed Response Helper
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_parsed_response(model_type_input: ModelTypeInput, client: Anthropic, console: Console) -> Optional[T]:
    """

    Query Claude and return a parsed representation of the requested format.


    :param model_type_input: Detected model type input
    :type model_type_input: ModelTypeInput
    :param client: Anthropic client instance
    :type client: Anthropic
    :param console: Rich Console to render output to
    :type console: Console

    :return: Parsed model instance or None if parsing failed
    :rtype: Optional[T]

    """

    # Progress: context -> instructions -> parse -> render
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Building Wikipedia context", total=4)

        input_model: Type[T] = cast(Type[T], model_type_input.model_type.get_model_from_name())
        try:
            wikipedia_summary, context_hint = build_wikipedia_topic_context(
                input_model,
                model_type_input,
            )
        except Exception as e:
            console.print(f"[warn]Failed to build Wikipedia context: {e}[/warn]")
            wikipedia_summary, context_hint = "", ""
        progress.update(task, description="Composing instructions", advance=1)

        instructions = augment_instructions_with_tool_hint(
            input_model.get_instructions(model_type_input.additional_info),
            wikipedia_summary,
            context_hint,
        )

        progress.update(task, description="Calling messages.parse", advance=1)
        # Use the messages.parse endpoint to get structured format instances back
        response = client.messages.parse(
            model=get_model_name(),
            max_tokens=MAX_TOKENS,
            system=instructions,
            messages=[{"role": "user", "content": input_model.get_user_prompt(model_type_input.formatted_name)}],
            output_format=input_model,
        )

        if check_refusal(response, console, model_type_input.formatted_name):
            return None

        item_info: Optional[T] = getattr(response, "parsed_output", None)
        if item_info is None:
            console.print(f"[red]Failed to parse info for '{model_type_input.formatted_name}'[/red]")
            return None

        setattr(item_info, "wikipedia_summary", wikipedia_summary)

        progress.update(task, description="Rendering output", advance=1)
        # render output (delegate to model's render method)
        console.rule(f"[bold cyan]{model_type_input.formatted_name}")
        item_info.render(console)
        console.print("\n")

        return item_info
