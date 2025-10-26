"""Comprehensive tests for openai_json module."""

from unittest.mock import Mock, patch

from rich.console import Console

from aiss.models.shared import ModelType, ModelTypeResult
from aiss.openai_direct.openai_json import (
    _extract_text_from_response,
    _model_type_for_format,
    get_json_response,
)


class TestExtractTextFromResponse:
    """Test _extract_text_from_response function."""

    def test_extract_with_output_text_attribute(self):
        """Test extracting text when response has output_text attribute."""
        response = Mock()
        response.output_text = "Sample output text"

        result = _extract_text_from_response(response)

        assert result == "Sample output text"

    def test_extract_without_output_text(self):
        """Test extracting text when output_text is None."""
        response = Mock()
        response.output_text = None
        response.output = []

        result = _extract_text_from_response(response)

        assert result == ""

    def test_extract_from_output_list_with_dict_content(self):
        """Test extracting text from output list with dict content."""
        response = Mock()
        response.output_text = None
        response.output = [{"content": [{"text": "First part"}, {"text": "Second part"}]}]

        result = _extract_text_from_response(response)

        assert "First part" in result
        assert "Second part" in result

    def test_extract_from_output_with_content_key(self):
        """Test extracting text using 'content' key."""
        response = Mock()
        response.output_text = None
        response.output = [{"content": [{"content": "Content text"}]}]

        result = _extract_text_from_response(response)

        assert "Content text" in result

    def test_extract_from_output_with_string_content(self):
        """Test extracting when content items are strings."""
        response = Mock()
        response.output_text = None
        response.output = [{"content": ["String content 1", "String content 2"]}]

        result = _extract_text_from_response(response)

        assert "String content 1" in result
        assert "String content 2" in result

    def test_extract_with_empty_output(self):
        """Test extracting when output list is empty."""
        response = Mock()
        response.output_text = None
        response.output = []

        result = _extract_text_from_response(response)

        assert result == ""

    def test_extract_with_none_output(self):
        """Test extracting when output is None."""
        response = Mock()
        response.output_text = None
        response.output = None

        result = _extract_text_from_response(response)

        assert result == ""

    def test_extract_handles_exception(self):
        """Test that exceptions during extraction return empty string."""
        response = Mock()
        response.output_text = None
        # Set output to something that will cause an error
        response.output = Mock()
        response.output.__iter__ = Mock(side_effect=Exception("Test error"))

        result = _extract_text_from_response(response)

        assert result == ""

    def test_extract_with_no_output_attribute(self):
        """Test extracting when response has no output attribute."""
        response = Mock(spec=[])  # Empty spec means no attributes
        del response.output_text

        result = _extract_text_from_response(response)

        assert result == ""

    def test_extract_multiline_output(self):
        """Test extracting multiple lines of text."""
        response = Mock()
        response.output_text = None
        response.output = [
            {"content": [{"text": "Line 1"}]},
            {"content": [{"text": "Line 2"}]},
            {"content": [{"text": "Line 3"}]},
        ]

        result = _extract_text_from_response(response)

        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result


class TestModelTypeForFormat:
    """Test _model_type_for_format function."""

    def test_model_type_for_movie_format(self):
        """Test getting model type for a movie format class."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        result = _model_type_for_format(DramaMovieInfo)

        # Returns a ModelType enum value
        assert isinstance(result, ModelType)

    def test_model_type_for_game_format(self):
        """Test getting model type for a game format class."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        result = _model_type_for_format(ActionAdventureGameInfo)

        # Returns a ModelType enum value
        assert isinstance(result, ModelType)

    def test_model_type_for_show_format(self):
        """Test getting model type for a show format class."""
        from aiss.models.shows.drama_model import DramaShowInfo

        result = _model_type_for_format(DramaShowInfo)

        # Returns a ModelType enum value
        assert isinstance(result, ModelType)

    def test_model_type_for_unknown_format(self):
        """Test getting model type for unknown format returns SHOW as default."""

        class UnknownFormat:
            pass

        result = _model_type_for_format(UnknownFormat)

        assert result == ModelType.SHOW


class TestGetJsonResponse:
    """Test get_json_response function."""

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    @patch("aiss.openai_direct.openai_json.render_from_json")
    def test_get_json_response_success(self, mock_render, mock_augment, mock_build_context):
        """Test successful JSON response retrieval and rendering."""
        mock_client = Mock()
        console = Console()

        # Setup mocks
        mock_build_context.return_value = ("Wikipedia summary", "Context hint")
        mock_augment.return_value = "Augmented instructions"

        mock_response = Mock()
        mock_response.output_text = '{"title": "Test Movie", "year": 2020}'
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test Movie",
        )

        get_json_response(model_result, mock_client, console)

        # Verify calls
        mock_build_context.assert_called_once()
        mock_augment.assert_called_once()
        mock_client.responses.create.assert_called_once()
        mock_render.assert_called_once()

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    def test_get_json_response_invalid_json(self, mock_augment, mock_build_context):
        """Test handling of invalid JSON response."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = "Not valid JSON at all"
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.ACTION_ADVENTURE_GAME,
            description="Test game description",
            formatted_name="Test",
        )

        get_json_response(model_result, mock_client, console)

        # Should handle gracefully without crashing

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    @patch("aiss.openai_direct.openai_json.render_from_json")
    def test_get_json_response_with_regex_extraction(self, mock_render, mock_augment, mock_build_context):
        """Test JSON extraction using regex when parsing fails initially."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = 'Some text before {"title": "Extracted"} some text after'
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.SHOW,
            description="Test show description",
            formatted_name="Test",
        )

        get_json_response(model_result, mock_client, console)

        # Should extract and render the JSON
        mock_render.assert_called_once()

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    def test_get_json_response_empty_output(self, mock_augment, mock_build_context):
        """Test handling of empty response output."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = ""
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test",
        )

        get_json_response(model_result, mock_client, console)

        # Should handle empty output gracefully

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    @patch("aiss.openai_direct.openai_json.render_from_json")
    def test_get_json_response_render_exception(self, mock_render, mock_augment, mock_build_context):
        """Test handling of exception during rendering."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = '{"key": "value"}'
        mock_client.responses.create.return_value = mock_response

        mock_render.side_effect = Exception("Rendering error")

        model_result = ModelTypeResult(
            model_type=ModelType.SHOOTER_GAME,
            description="Test shooter game",
            formatted_name="Test",
        )

        get_json_response(model_result, mock_client, console)

        # Should catch and handle rendering exception

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    @patch("aiss.openai_direct.openai_json.render_from_json")
    def test_get_json_response_with_additional_info(self, mock_render, mock_augment, mock_build_context):
        """Test JSON response with additional info in model result."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = '{"title": "Movie"}'
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Complex movie with additional information",
            formatted_name="Complex Movie",
            additional_info=["2020", "Drama"],
        )

        get_json_response(model_result, mock_client, console)

        mock_render.assert_called_once()

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    @patch("aiss.openai_direct.openai_json.render_from_json")
    def test_get_json_response_array_json(self, mock_render, mock_augment, mock_build_context):
        """Test handling JSON array response."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = '[{"item": 1}, {"item": 2}]'
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.SHOW,
            description="Test show description",
            formatted_name="Test",
        )

        get_json_response(model_result, mock_client, console)

        mock_render.assert_called_once()

    @patch("aiss.openai_direct.openai_json.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_json.augment_instructions_with_tool_hint")
    def test_get_json_response_regex_fails_to_parse(self, mock_augment, mock_build_context):
        """Test when regex extracts text but it's still not valid JSON."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_text = "Text with {invalid json} in it"
        mock_client.responses.create.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test",
        )

        get_json_response(model_result, mock_client, console)

        # Should handle gracefully and print error message


def test_model_type_for_format_value_error_handling():
    """Test _model_type_for_format handles ValueError from get_model_from_name()."""
    from aiss.models.movies.action_adventure_model import ActionAdventureMovieInfo

    # Test with a class that should work normally
    result = _model_type_for_format(ActionAdventureMovieInfo)
    assert result == ModelType.ACTION_ADVENTURE_MOVIE
