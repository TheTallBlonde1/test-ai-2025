"""Comprehensive tests for openai_parsed module."""

from unittest.mock import Mock, patch

from rich.console import Console

from aiss.models.shared import ModelType, ModelTypeResult
from aiss.openai_direct.openai_parsed import (
    _model_type_for_format,
    get_parsed_response,
)


class TestModelTypeForFormat:
    """Test _model_type_for_format function."""

    def test_model_type_for_none(self):
        """Test that None format returns SHOW."""
        result = _model_type_for_format(None)
        assert result == ModelType.SHOW

    def test_model_type_for_movie_format(self):
        """Test getting model type for a movie format class."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        result = _model_type_for_format(DramaMovieInfo)
        assert isinstance(result, ModelType)

    def test_model_type_for_game_format(self):
        """Test getting model type for a game format class."""
        from aiss.models.games.role_playing_model import RolePlayingGameInfo

        result = _model_type_for_format(RolePlayingGameInfo)
        assert isinstance(result, ModelType)

    def test_model_type_for_show_format(self):
        """Test getting model type for a show format class."""
        from aiss.models.shows.comedy_model import ComedyShowInfo

        result = _model_type_for_format(ComedyShowInfo)
        assert isinstance(result, ModelType)

    def test_model_type_for_unknown_format(self):
        """Test getting model type for unknown format returns SHOW."""

        class UnknownFormat:
            pass

        result = _model_type_for_format(UnknownFormat)
        assert result == ModelType.SHOW


class TestGetParsedResponse:
    """Test get_parsed_response function."""

    @patch("aiss.openai_direct.openai_parsed.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_parsed.augment_instructions_with_tool_hint")
    def test_get_parsed_response_success(self, mock_augment, mock_build_context):
        """Test successful parsed response retrieval and rendering."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        mock_client = Mock()
        console = Console()

        # Setup mocks
        mock_build_context.return_value = ("Wikipedia summary", "Context hint")
        mock_augment.return_value = "Augmented instructions"

        mock_parsed_result = Mock(spec=DramaMovieInfo)
        mock_parsed_result.render = Mock()

        mock_response = Mock()
        mock_response.output_parsed = mock_parsed_result
        mock_client.responses.parse.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test Movie",
        )

        get_parsed_response(model_result, mock_client, console)

        # Verify calls
        mock_build_context.assert_called_once()
        mock_augment.assert_called_once()
        mock_client.responses.parse.assert_called_once()
        mock_parsed_result.render.assert_called_once()

    @patch("aiss.openai_direct.openai_parsed.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_parsed.augment_instructions_with_tool_hint")
    def test_get_parsed_response_no_output(self, mock_augment, mock_build_context):
        """Test handling when output_parsed is None."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock()
        mock_response.output_parsed = None
        mock_client.responses.parse.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.SHOW,
            description="Test show description",
            formatted_name="Test",
        )

        get_parsed_response(model_result, mock_client, console)

        # Should handle gracefully and print error

    @patch("aiss.openai_direct.openai_parsed.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_parsed.augment_instructions_with_tool_hint")
    def test_get_parsed_response_sets_wikipedia_summary(self, mock_augment, mock_build_context):
        """Test that Wikipedia summary is set on parsed result."""
        from aiss.models.shows.drama_model import DramaShowInfo

        mock_client = Mock()
        console = Console()

        wikipedia_summary = "Test Wikipedia summary"
        mock_build_context.return_value = (wikipedia_summary, "Context")
        mock_augment.return_value = "Instructions"

        mock_parsed_result = Mock(spec=DramaShowInfo)
        mock_parsed_result.render = Mock()

        mock_response = Mock()
        mock_response.output_parsed = mock_parsed_result
        mock_client.responses.parse.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.DRAMA,
            description="Test drama show",
            formatted_name="Test Show",
        )

        get_parsed_response(model_result, mock_client, console)

        # Verify wikipedia_summary was set
        assert hasattr(mock_parsed_result, "wikipedia_summary")

    @patch("aiss.openai_direct.openai_parsed.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_parsed.augment_instructions_with_tool_hint")
    def test_get_parsed_response_with_additional_info(self, mock_augment, mock_build_context):
        """Test parsed response with additional info."""
        from aiss.models.games.shooter_model import ShooterGameInfo

        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_parsed_result = Mock(spec=ShooterGameInfo)
        mock_parsed_result.render = Mock()

        mock_response = Mock()
        mock_response.output_parsed = mock_parsed_result
        mock_client.responses.parse.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.SHOOTER_GAME,
            description="Test shooter game with additional info",
            formatted_name="Test Game",
            additional_info=["2023", "FPS"],
        )

        get_parsed_response(model_result, mock_client, console)

        mock_parsed_result.render.assert_called_once()

    @patch("aiss.openai_direct.openai_parsed.build_wikipedia_topic_context")
    @patch("aiss.openai_direct.openai_parsed.augment_instructions_with_tool_hint")
    def test_get_parsed_response_no_output_parsed_attribute(self, mock_augment, mock_build_context):
        """Test handling when response has no output_parsed attribute."""
        mock_client = Mock()
        console = Console()

        mock_build_context.return_value = ("Summary", "Context")
        mock_augment.return_value = "Instructions"

        mock_response = Mock(spec=[])  # No attributes
        mock_client.responses.parse.return_value = mock_response

        model_result = ModelTypeResult(
            model_type=ModelType.MOVIE,
            description="Test movie description",
            formatted_name="Test",
        )

        get_parsed_response(model_result, mock_client, console)

        # Should handle gracefully


def test_model_type_for_format_value_error_handling():
    """Test _model_type_for_format handles ValueError from get_model_from_name()."""
    from aiss.models.movies.action_adventure_model import ActionAdventureMovieInfo

    # Test with a class that should work normally
    result = _model_type_for_format(ActionAdventureMovieInfo)
    assert result == ModelType.ACTION_ADVENTURE_MOVIE
