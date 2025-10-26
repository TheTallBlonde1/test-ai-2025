"""Utility helpers for integrating a Wikipedia summary tool with OpenAI responses.

This module defines the tool schema that can be offered to OpenAI models as well
as the local implementation for resolving tool calls. It also provides helper
utilities for crafting context-rich prompts derived from the active
``ModelFormatProtocol`` implementation so the model can construct accurate tool
arguments.
"""

from __future__ import annotations

from typing import List, Type

from wikipedia import summary

from aiss.models.protocols import ModelFormatProtocol
from aiss.models.shared import ModelTypeResult


def build_wikipedia_topic_context(
    text_format: Type[ModelFormatProtocol],
    model_type_result: ModelTypeResult,
) -> tuple[str, str]:
    """Create a context string describing the work for informative tool usage."""

    parts: List[str] = []
    parts.append(f"Title: {model_type_result.formatted_name}")

    model_name = getattr(text_format, "model_name", text_format.__name__)
    parts.append(f"Format: {model_name}")

    key_trait = getattr(text_format, "key_trait", "")
    if key_trait:
        parts.append(f"Key Trait: {key_trait}")

    description = getattr(text_format, "description", "")
    if description:
        parts.append(f"Description: {description}")

    additional = model_type_result.additional_info or []
    additional_str = ""
    if additional:
        additional_str = "; ".join(str(item) for item in additional)
        parts.append(f"Additional Info: {additional_str}")

    topic_base = (model_type_result.formatted_name or "").strip()
    if not topic_base:
        return ""

    wikipedia_topic = topic_base
    if additional_str:
        wikipedia_topic = f"{topic_base} ({description} / {key_trait} / {additional_str})".strip()

    try:
        wikipedia_summary = summary(f"{model_type_result.formatted_name}: {model_type_result.description}", sentences=10)
        return wikipedia_summary, ",".join(parts)

    except Exception as e:
        print(f"Error fetching Wikipedia summary for topic '{wikipedia_topic}': {e}")


def augment_prompt_with_wikipedia_context(base_prompt: str, wikipedia_summary: str, context: str) -> str:
    """Append context guidance to a user prompt for Wikipedia tool usage."""

    if not context:
        return base_prompt
    return f"{base_prompt}\n\nTopic & Context Hint: {context}\n\nWikipedia Summary: {wikipedia_summary}"


def augment_instructions_with_tool_hint(instructions: str, wikipedia_summary: str, context: str) -> str:
    """Encourage tool usage directly within the system instructions."""

    if not context:
        return instructions
    return f"{instructions}\n\nPrefer the following context: {context}.\n\nWikipedia Summary: {wikipedia_summary}"
