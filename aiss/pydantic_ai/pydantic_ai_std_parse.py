"""Pydantic AI standard parse helper.

Replicates the behavior of `aiss.openai_direct.openai_parsed.get_parsed_response`
but implemented using the Pydantic AI Agent API.

This module selects the appropriate Pydantic model class from a `ModelTypeInput`,
builds task instructions augmented with optional Wikipedia context, and runs a
single Pydantic AI agent to produce a structured model instance. The result is
rendered via the model's `render(console)` method and returned to the caller.
"""

from __future__ import annotations

import os
from typing import Optional, Type, TypeVar, cast

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from aiss.models import ModelTypeInput
from aiss.models.protocols import ModelFormatProtocol
from aiss.openai_direct.wikipedia_tool import (
    augment_instructions_with_tool_hint,
    build_wikipedia_topic_context,
)

# Import lazily/flexibly so tests can mock Agent without the dependency present
try:  # pragma: no cover - exercised via mocks in tests
    from pydantic_ai import Agent
except Exception:  # pragma: no cover - allows tests to patch Agent symbol
    Agent = None  # type: ignore


# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def _provider_model_name() -> str:
    """Return the provider-prefixed model name for Pydantic AI.

    Defaults to the OPENAI model and mirrors the OPENAI_MODEL_NAME env var used
    by the OpenAI SDK helpers, e.g. "gpt-5-mini" becomes "openai:gpt-5-mini".
    """

    base = os.getenv("PYDANTIC_AI_MODEL_NAME") or os.getenv("OPENAI_MODEL_NAME", "gpt-5-mini")
    base = base.strip()
    if base == "test":
        return base
    # If the user already supplied a provider prefix (e.g., "openai:gpt-4o-mini"),
    # pass it through unchanged. Otherwise, assume OpenAI.
    return base if ":" in base else f"openai:{base}"


def get_parsed_response(model_type_input: ModelTypeInput, console: Console) -> Optional[T]:
    """Run a single Pydantic AI Agent to produce a structured model output.

    This mirrors `aiss.openai_direct.openai_parsed.get_parsed_response` using
    the Pydantic AI Agent API instead of the OpenAI Responses API.

    Args:
            model_type_input: The detected model type and input metadata
            console: Rich console for rendering

    Returns:
            The parsed model instance or None if parsing fails
    """

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Building Wikipedia context", total=4)

        # Resolve the Pydantic model class for the requested type
        input_model: Type[T] = cast(Type[T], model_type_input.model_type.get_model_from_name())

        # Try to build optional Wikipedia context for better accuracy
        try:
            wikipedia_summary, context_hint = build_wikipedia_topic_context(
                input_model,
                model_type_input,
            )
        except Exception as e:  # pragma: no cover - defensive
            console.print(f"[warn]Failed to build Wikipedia context: {e}[/warn]")
            wikipedia_summary, context_hint = "", ""
        progress.update(task, description="Composing instructions", advance=1)

        # Build instructions and user prompt
        base_instructions = input_model.get_instructions(model_type_input.additional_info)
        instructions = augment_instructions_with_tool_hint(base_instructions, wikipedia_summary, context_hint)
        user_prompt = input_model.get_user_prompt(model_type_input.formatted_name)

        # Prepare the agent (provider model mirrors OPENAI_MODEL_NAME env var)
        provider_model = _provider_model_name()

        if Agent is None:  # pragma: no cover - caught in tests via mocking
            console.print("[red]Pydantic AI is not installed. Install `pydantic-ai` to run this helper.[/red]")
            return None

        progress.update(task, description="Running Pydantic AI agent", advance=1)
        agent = Agent(provider_model, output_type=input_model, system_prompt=instructions)

        # Run synchronously to mirror existing OpenAI helper API
        try:
            result = agent.run_sync(user_prompt)
        except Exception as e:  # pragma: no cover - defensive
            console.print(f"[red]Agent run failed: {e}[/red]")
            return None

        item_info: Optional[T] = cast(Optional[T], getattr(result, "output", None))
        if item_info is None:
            console.print(f"[red]Failed to parse info for '{model_type_input.formatted_name}'[/red]")
            return None

        # Attach the Wikipedia summary for downstream display parity
        setattr(item_info, "wikipedia_summary", wikipedia_summary)

        progress.update(task, description="Rendering output", advance=1)
        # Render through the model's own renderer for consistent UI
        console.rule(f"[bold cyan]{model_type_input.formatted_name}")
        item_info.render(console)
        console.print("\n")

        return item_info
