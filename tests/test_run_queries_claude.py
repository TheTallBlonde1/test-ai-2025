"""Tests for the Claude branch of run_the_query."""

from unittest.mock import Mock, patch

import pytest

from aiss.models.shared import ModelType, ModelTypeInput, ResultType
from aiss.run_queries import run_the_query


@pytest.fixture
def model_input() -> ModelTypeInput:
    return ModelTypeInput(model_type=ModelType.MOVIE, description="d", formatted_name="N")


@pytest.mark.parametrize(
    ("mode", "target"),
    [
        (ResultType.PARSED, "get_claude_parsed_response"),
        (ResultType.JSON, "get_claude_json_response"),
        (ResultType.TEXT, "get_claude_text_response"),
    ],
)
@pytest.mark.parametrize("api", ["claude", "anthropic", " Claude "])
def test_claude_dispatch(mode, target, api, model_input):
    with (
        patch("aiss.run_queries.Anthropic") as anthropic_cls,
        patch("aiss.run_queries.OpenAI") as openai_cls,
        patch("aiss.run_queries.find_model_from_input_claude", return_value=model_input) as find,
        patch(f"aiss.run_queries.{target}") as handler,
    ):
        run_the_query("The Godfather", mode, api)

    openai_cls.assert_not_called()
    find.assert_called_once()
    handler.assert_called_once()
    assert handler.call_args.args[0] is model_input
    assert handler.call_args.args[1] is anthropic_cls.return_value


def test_claude_classification_failure_skips_handlers():
    with (
        patch("aiss.run_queries.Anthropic"),
        patch("aiss.run_queries.find_model_from_input_claude", return_value=None),
        patch("aiss.run_queries.get_claude_parsed_response") as handler,
    ):
        run_the_query("x", ResultType.PARSED, "claude")
    handler.assert_not_called()


def test_openai_still_default(model_input):
    with (
        patch("aiss.run_queries.OpenAI") as openai_cls,
        patch("aiss.run_queries.Anthropic") as anthropic_cls,
        patch("aiss.run_queries.find_model_from_input", return_value=model_input),
        patch("aiss.run_queries.get_parsed_response", Mock()) as handler,
    ):
        run_the_query("x", ResultType.PARSED)
    anthropic_cls.assert_not_called()
    handler.assert_called_once()
    assert handler.call_args.args[1] is openai_cls.return_value
