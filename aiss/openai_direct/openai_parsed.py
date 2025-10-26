"""Helpers to query OpenAI's responses.parse endpoint and render parsed models.

This module provides typed helpers that accept a "text format" class (for
example a genre-specific `*ShowInfo` or one of the movie formats) and call the OpenAI SDK
`responses.parse` endpoint, rendering the parsed Pydantic model to the console.
"""

from typing import TYPE_CHECKING, Optional, Type, TypeVar, cast

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console

from aiss.models import ModelTypeResult
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


def get_parsed_response(model_type_result: ModelTypeResult, client: OpenAI, console: Console) -> None:
    """

    Query the model and return a parsed representation of the requested format.

    :param input_text: Name to query
    :type input_text: str
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console
    :param local_model: Local model name for progress display
    :type local_model: str

    """

    # default to the shared show format when none is provided explicitly
    text_format = cast(Type[T], model_type_result.model_type.get_model_from_name())
    wikipedia_summary, context_hint = build_wikipedia_topic_context(
        text_format,
        model_type_result,
    )
    instructions = augment_instructions_with_tool_hint(
        text_format.get_instructions(model_type_result.additional_info),
        wikipedia_summary,
        context_hint,
    )

    # Use the responses.parse endpoint to get structured format instances back
    response: ParsedResponse[T] = client.responses.parse(
        model="gpt-5-mini",
        instructions=instructions,
        input=text_format.get_user_prompt(model_type_result.formatted_name),
        text_format=text_format,
        timeout=Timeout(4000, connect=6.0),
    )
    item_info: Optional[T] = getattr(response, "output_parsed", None)
    if item_info is None:
        console.print(f"[red]Failed to parse info for '{model_type_result.formatted_name}'[/red]")
        return

    setattr(item_info, "wikipedia_summary", wikipedia_summary)

    # render output (delegate to model's render method)
    console.rule(f"[bold cyan]{model_type_result.formatted_name}")
    item_info.render(console)
    console.print("\n")
