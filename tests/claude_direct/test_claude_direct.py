"""Tests for the claude_direct parsed/json/text flows and the Claude classifier."""

from unittest.mock import Mock, patch

import pytest
from rich.console import Console

from aiss.check_model import find_model_from_input_claude
from aiss.claude_direct import claude_json, claude_parsed, claude_text
from aiss.claude_direct._common import DEFAULT_CLAUDE_MODEL, extract_text_from_response, get_model_name
from aiss.models import FindModelRequest, ModelType
from aiss.models.shared import ModelTypeInput


def _text_response(text: str, stop_reason: str = "end_turn") -> Mock:
    block = Mock(type="text", text=text)
    return Mock(content=[block], stop_reason=stop_reason)


@pytest.fixture
def model_input() -> ModelTypeInput:
    return ModelTypeInput(model_type=ModelType.MOVIE, description="desc", formatted_name="Test Movie")


@pytest.fixture
def console() -> Console:
    return Console(record=True)


def _patch_wiki(module):
    return (
        patch(f"{module}.build_wikipedia_topic_context", return_value=("summary", "hint")),
        patch(f"{module}.augment_instructions_with_tool_hint", return_value="instructions"),
    )


class TestCommon:
    def test_model_name_default(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_MODEL_NAME", raising=False)
        assert get_model_name() == DEFAULT_CLAUDE_MODEL

    def test_model_name_env(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_MODEL_NAME", "claude-haiku-5-5")
        assert get_model_name() == "claude-haiku-5-5"

    def test_extract_text_skips_non_text_blocks(self):
        response = Mock(content=[Mock(type="thinking", text="hidden"), Mock(type="text", text="shown")])
        assert extract_text_from_response(response) == "shown"


class TestParsed:
    def test_success(self, model_input, console):
        client = Mock()
        item = Mock()
        client.messages.parse.return_value = Mock(parsed_output=item, stop_reason="end_turn")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_parsed")
        with p1, p2:
            result = claude_parsed.get_parsed_response(model_input, client, console)

        assert result is item
        assert item.wikipedia_summary == "summary"
        item.render.assert_called_once_with(console)
        assert client.messages.parse.call_args.kwargs["system"] == "instructions"

    def test_none_parsed_output(self, model_input, console):
        client = Mock()
        client.messages.parse.return_value = Mock(parsed_output=None, stop_reason="end_turn")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_parsed")
        with p1, p2:
            assert claude_parsed.get_parsed_response(model_input, client, console) is None
        assert "Failed to parse" in console.export_text()

    def test_refusal(self, model_input, console):
        client = Mock()
        client.messages.parse.return_value = Mock(parsed_output=None, stop_reason="refusal")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_parsed")
        with p1, p2:
            assert claude_parsed.get_parsed_response(model_input, client, console) is None
        assert "declined" in console.export_text()

    def test_wikipedia_failure_is_tolerated(self, model_input, console):
        client = Mock()
        item = Mock()
        client.messages.parse.return_value = Mock(parsed_output=item, stop_reason="end_turn")
        with (
            patch("aiss.claude_direct.claude_parsed.build_wikipedia_topic_context", side_effect=RuntimeError("boom")),
            patch("aiss.claude_direct.claude_parsed.augment_instructions_with_tool_hint", return_value="i"),
        ):
            assert claude_parsed.get_parsed_response(model_input, client, console) is item


class TestJson:
    def test_success(self, model_input, console):
        client = Mock()
        client.messages.create.return_value = _text_response('{"title": "x"}')
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_json")
        with p1, p2, patch("aiss.claude_direct.claude_json.render_from_json") as render:
            claude_json.get_json_response(model_input, client, console)
        render.assert_called_once_with({"title": "x"}, console)

    def test_json_embedded_in_prose(self, model_input, console):
        client = Mock()
        client.messages.create.return_value = _text_response('Here you go:\n{"a": 1}\nThanks')
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_json")
        with p1, p2, patch("aiss.claude_direct.claude_json.render_from_json") as render:
            claude_json.get_json_response(model_input, client, console)
        render.assert_called_once_with({"a": 1}, console)

    def test_invalid_json(self, model_input, console):
        client = Mock()
        client.messages.create.return_value = _text_response("not json at all")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_json")
        with p1, p2, patch("aiss.claude_direct.claude_json.render_from_json") as render:
            claude_json.get_json_response(model_input, client, console)
        render.assert_not_called()
        assert "Failed to parse JSON" in console.export_text()

    def test_refusal(self, model_input, console):
        client = Mock()
        client.messages.create.return_value = _text_response("", stop_reason="refusal")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_json")
        with p1, p2, patch("aiss.claude_direct.claude_json.render_from_json") as render:
            claude_json.get_json_response(model_input, client, console)
        render.assert_not_called()


class TestText:
    def test_success(self, model_input, console):
        client = Mock()
        client.messages.create.return_value = _text_response("Plain output")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_text")
        with p1, p2:
            claude_text.get_text_response(model_input, client, console)
        assert "Plain output" in console.export_text()
        assert client.messages.create.call_args.kwargs["system"] == "instructions"

    def test_refusal(self, model_input, console):
        client = Mock()
        client.messages.create.return_value = _text_response("", stop_reason="refusal")
        p1, p2 = _patch_wiki("aiss.claude_direct.claude_text")
        with p1, p2:
            claude_text.get_text_response(model_input, client, console)
        assert "Information (Text)" not in console.export_text()


class TestClassifier:
    def test_success(self, console):
        client = Mock()
        parsed = FindModelRequest(
            find_model=ModelType.MOVIE.value,
            description="A film",
            formatted_name="The Film",
            additional_info=[],
        )
        client.messages.parse.return_value = Mock(parsed_output=parsed, stop_reason="end_turn")

        result = find_model_from_input_claude("The Film", client, console)

        assert result is not None
        assert result.model_type == ModelType.MOVIE
        assert result.formatted_name == "The Film"
        assert client.messages.parse.call_args.kwargs["output_format"] is FindModelRequest

    def test_none_parsed(self, console):
        client = Mock()
        client.messages.parse.return_value = Mock(parsed_output=None, stop_reason="end_turn")
        assert find_model_from_input_claude("x", client, console) is None

    def test_refusal(self, console):
        client = Mock()
        client.messages.parse.return_value = Mock(parsed_output=None, stop_reason="refusal")
        assert find_model_from_input_claude("x", client, console) is None
