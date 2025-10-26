"""Comprehensive tests for openai_text module."""

from unittest.mock import Mock, patch

from rich.console import Console

from aiss.models.shared import ModelType, ModelTypeResult
from aiss.openai_direct.openai_text import get_text_response


class TestGetTextResponse:
    """Test get_text_response function."""

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_success(self, mock_augment, mock_build_context):
        """Test successful text response retrieval and rendering."""
        mock_client = Mock()
        console = Console()

        # Setup mocks
        mock_build_context.return_value = ("Wikipedia summary", "Context hint")
        mock_augment.return_value = "Augmented instructions"

        mock_response = Mock()
        mock_response.output_text = "This is the plain text output from the model."
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test Movie",
        )

        get_text_response(model_result, mock_client, console)

        # Verify calls
        mock_build_context.assert_called_once()
        mock_augment.assert_called_once()
        mock_client.responses.create.assert_called_once()

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_with_custom_format(self, mock_augment, mock_build_context):
        """Test text response with custom text_format provided."""
        from aiss.models.games.role_playing_model import RolePlayingGameInfo

        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = "Custom format output"
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.ROLE_PLAYING_GAME,
            description="Test game description",
            formatted_name="Test Game",
        )

        get_text_response(model_result, mock_client, console, text_format=RolePlayingGameInfo)

        mock_build_context.assert_called_once()
        mock_client.responses.create.assert_called_once()

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_with_additional_info(self, mock_augment, mock_build_context):
        """Test text response with additional info."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = "Output with additional context"
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.DRAMA_MOVIE,
            description="Complex movie with additional information",
            formatted_name="Complex Movie",
            additional_info=["2020", "Drama"],
        )

        get_text_response(model_result, mock_client, console)

        mock_augment.assert_called_once()

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_empty_output(self, mock_augment, mock_build_context):
        """Test handling of empty text output."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = ""
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.SHOW,
            description="Test show description",
            formatted_name="Test",
        )

        get_text_response(model_result, mock_client, console)

        # Should handle empty output gracefully

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_multiline_output(self, mock_augment, mock_build_context):
        """Test handling of multiline text output."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = "Line 1\nLine 2\nLine 3\nLine 4"
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.COMEDY,
            description="Test comedy show",
            formatted_name="Test Show",
        )

        get_text_response(model_result, mock_client, console)

        # Should display all lines

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_with_none_format(self, mock_augment, mock_build_context):
        """Test text response when text_format is explicitly None."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = "Text with None format"
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test",
        )

        get_text_response(model_result, mock_client, console, text_format=None)

        # Should use model_type to get format
        mock_client.responses.create.assert_called_once()

    @patch("aiss.openai_direct.openai_text.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_text.augment_instructions_with_tool_hint")
    def test_get_text_response_long_output(self, mock_augment, mock_build_context):
        """Test handling of very long text output."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        long_text = "Lorem ipsum " * 100
        mock_response = Mock()
        mock_response.output_text = long_text
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.THRILLER,
            description="Test thriller description",
            formatted_name="Test",
        )

        get_text_response(model_result, mock_client, console)

        # Should display long text without crashing
