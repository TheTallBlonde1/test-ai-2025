"""Helpers that request plain text responses from the OpenAI SDK.

This module demonstrates the "text" query flow where the model's raw
text output is printed inside a Rich Panel. It's intended for quick
inspection rather than structured parsing.
"""

from typing import TYPE_CHECKING, Type, TypeVar, cast

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console
from rich.panel import Panel

# Progress UI is managed by the caller (run_queries)
from aiss.models.protocols import ModelFormatProtocol
from aiss.models.shared import ModelTypeResult

from .wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)

if TYPE_CHECKING:
    from openai.types.responses.response import Response


load_dotenv()

# MARK: Text Response Helper
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_text_response(
    model_type_result: ModelTypeResult,
    client: OpenAI,
    console: Console,
    text_format: Type[T] | None = None,
) -> None:
    """Render plain-text output for a detected model type."""

    text_format = cast(Type[T], text_format or model_type_result.model_type.get_model_from_name())
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

    console.rule(f"[bold cyan]{model_type_result.formatted_name}")

    plain_text = response.output_text
    console.print(Panel(plain_text, title="Information (Text)", expand=False, style="green"))
