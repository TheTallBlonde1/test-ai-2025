"""Helpers to query OpenAI's responses.parse endpoint and render parsed models.

This module provides typed helpers that accept a "text format" class (for
example a genre-specific `*ShowInfo` or one of the movie formats) and call the OpenAI SDK
`responses.parse` endpoint, rendering the parsed Pydantic model to the console.
"""

import os
from typing import TYPE_CHECKING, Optional, Type, TypeVar, cast

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from aiss.models import ModelTypeInput
from aiss.models.protocols import ModelFormatProtocol

from .wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)

if TYPE_CHECKING:
    from openai.types.responses.parsed_response import ParsedResponse


load_dotenv()

# MARK: Parsed Response Helper
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_parsed_response(model_type_input: ModelTypeInput, client: OpenAI, console: Console) -> Optional[T]:
    """

    Query the model and return a parsed representation of the requested format.


    :param model_type_input: Detected model type input
    :type model_type_input: ModelTypeInput
    :param client: OpenAI client instance
    :type client: OpenAI
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

        # default to the shared show format when none is provided explicitly
        # Use the responses.parse endpoint to get structured format instances back
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
        model = os.getenv("OPENAI_MODEL_NAME", "gpt-5-mini")
        if not model:
            console.print("[red]OPENAI_MODEL_NAME environment variable is not set.[/red]")
            return None

        progress.update(task, description="Calling responses.parse", advance=1)
        # Use the responses.parse endpoint to get structured format instances back
        response: ParsedResponse[T] = client.responses.parse(
            model=model,
            instructions=instructions,
            input=input_model.get_user_prompt(model_type_input.formatted_name),
            text_format=input_model,
            timeout=Timeout(4000, connect=6.0),
        )

        item_info: Optional[T] = getattr(response, "output_parsed", None)
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
