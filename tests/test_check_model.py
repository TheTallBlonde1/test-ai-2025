"""Tests for check_model module."""

from unittest.mock import Mock, patch

import pytest
from openai import OpenAI, Timeout

from aiss.check_model import find_model_from_input
from aiss.models import FindModelRequest, ModelType, ModelTypeResult


def test_module_import():
    """Test that check_model module can be imported (covers load_dotenv call)."""
    with patch("aiss.check_model.load_dotenv"):
        import importlib

        import aiss.check_model

        importlib.reload(aiss.check_model)
        assert hasattr(aiss.check_model, "find_model_from_input")


@pytest.fixture
def mock_client():
    """Create a mock OpenAI client."""
    return Mock(spec=OpenAI)


@pytest.fixture
def console():
    """Create a mock console."""
    from rich.console import Console

    return Console(record=True, force_terminal=False, width=80)


class TestFindModelFromInput:
    """Test find_model_from_input function."""

    def test_find_model_movie_action(self, mock_client, console):
        """Test finding action movie model type."""
        # Setup mock response
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="action_adventure_movie", formatted_name="Die Hard", additional_info=["Action packed", "Bruce Willis"])

        mock_client.responses.parse.return_value = mock_response

        result = find_model_from_input("Die Hard action movie", mock_client, console)

        assert isinstance(result, ModelTypeResult)
        assert result.model_type == ModelType.ACTION_ADVENTURE_MOVIE
        assert result.formatted_name == "Die Hard"
        assert "Action packed" in result.additional_info

        # Verify client was called correctly
        mock_client.responses.parse.assert_called_once()
        call_args = mock_client.responses.parse.call_args
        assert call_args.kwargs["model"] == "gpt-5-mini"
        assert "Die Hard action movie" in call_args.kwargs["input"]
        assert call_args.kwargs["text_format"] == FindModelRequest
        assert isinstance(call_args.kwargs["timeout"], Timeout)

    def test_find_model_show_comedy(self, mock_client, console):
        """Test finding comedy show model type."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="comedy", formatted_name="Friends", additional_info=["Sitcom", "90s classic"])

        mock_client.responses.parse.return_value = mock_response

        result = find_model_from_input("Friends TV show", mock_client, console)

        assert result.model_type == ModelType.COMEDY
        assert result.formatted_name == "Friends"
        assert len(result.additional_info) == 2

    def test_find_model_game_rpg(self, mock_client, console):
        """Test finding RPG game model type."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="role_playing_game", formatted_name="The Witcher 3", additional_info=["Open world", "Fantasy"])

        mock_client.responses.parse.return_value = mock_response

        result = find_model_from_input("The Witcher 3 video game", mock_client, console)

        assert result.model_type == ModelType.ROLE_PLAYING_GAME
        assert result.formatted_name == "The Witcher 3"

    def test_find_model_returns_none_on_failed_parse(self, mock_client, console):
        """Test handling of failed parse (output_parsed is None)."""
        mock_response = Mock()
        mock_response.output_parsed = None

        mock_client.responses.parse.return_value = mock_response

        result = find_model_from_input("Invalid input", mock_client, console)

        assert result is None
        output = console.export_text()
        assert "Failed to parse" in output

    def test_find_model_all_movie_types(self, mock_client, console):
        """Test all movie model types can be returned."""
        movie_types = [
            ("action_adventure_movie", ModelType.ACTION_ADVENTURE_MOVIE),
            ("comedy_movie", ModelType.COMEDY_MOVIE),
            ("documentary_biographical_movie", ModelType.DOCUMENTARY_BIOGRAPHICAL_MOVIE),
            ("drama_movie", ModelType.DRAMA_MOVIE),
            ("fantasy_science_fiction_movie", ModelType.FANTASY_SCIENCE_FICTION_MOVIE),
            ("horror_movie", ModelType.HORROR_MOVIE),
            ("romance_movie", ModelType.ROMANCE_MOVIE),
            ("thriller_mystery_crime_movie", ModelType.THRILLER_MYSTERY_CRIME_MOVIE),
        ]

        for model_str, model_type in movie_types:
            mock_response = Mock()
            mock_response.output_parsed = FindModelRequest(find_model=model_str, formatted_name="Test Movie", additional_info=[])
            mock_client.responses.parse.return_value = mock_response

            result = find_model_from_input("test", mock_client, console)
            assert result.model_type == model_type

    def test_find_model_all_show_types(self, mock_client, console):
        """Test all show model types can be returned."""
        show_types = [
            ("action_adventure_fantasy", ModelType.ACTION_ADVENTURE_FANTASY),
            ("comedy", ModelType.COMEDY),
            ("documentary_factual", ModelType.DOCUMENTARY_FACTUAL),
            ("drama", ModelType.DRAMA),
            ("family_animation_kids", ModelType.FAMILY_ANIMATION_KIDS),
            ("news_informational", ModelType.NEWS_INFORMATIONAL),
            ("reality_competition_lifestyle", ModelType.REALITY_COMPETITION_LIFESTYLE),
            ("science_fiction", ModelType.SCIENCE_FICTION),
            ("sports", ModelType.SPORTS),
            ("thriller", ModelType.THRILLER),
        ]

        for model_str, model_type in show_types:
            mock_response = Mock()
            mock_response.output_parsed = FindModelRequest(find_model=model_str, formatted_name="Test Show", additional_info=[])
            mock_client.responses.parse.return_value = mock_response

            result = find_model_from_input("test", mock_client, console)
            assert result.model_type == model_type

    def test_find_model_all_game_types(self, mock_client, console):
        """Test all game model types can be returned."""
        game_types = [
            ("action_adventure_game", ModelType.ACTION_ADVENTURE_GAME),
            ("horror_survival_game", ModelType.HORROR_SURVIVAL_GAME),
            ("mmo_online_game", ModelType.MMO_ONLINE_GAME),
            ("puzzle_strategy_game", ModelType.PUZZLE_STRATEGY_GAME),
            ("role_playing_game", ModelType.ROLE_PLAYING_GAME),
            ("shooter_game", ModelType.SHOOTER_GAME),
            ("simulation_sandbox_game", ModelType.SIMULATION_SANDBOX_GAME),
            ("sports_racing_game", ModelType.SPORTS_RACING_GAME),
        ]

        for model_str, model_type in game_types:
            mock_response = Mock()
            mock_response.output_parsed = FindModelRequest(find_model=model_str, formatted_name="Test Game", additional_info=[])
            mock_client.responses.parse.return_value = mock_response

            result = find_model_from_input("test", mock_client, console)
            assert result.model_type == model_type

    def test_find_model_with_empty_additional_info(self, mock_client, console):
        """Test with empty additional_info list."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="drama_movie", formatted_name="Test", additional_info=[])

        mock_client.responses.parse.return_value = mock_response

        result = find_model_from_input("test", mock_client, console)

        assert result.additional_info == []

    def test_find_model_with_many_additional_info(self, mock_client, console):
        """Test with multiple additional info items."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="action_adventure_movie", formatted_name="Test", additional_info=["Info 1", "Info 2", "Info 3", "Info 4", "Info 5"])

        mock_client.responses.parse.return_value = mock_response

        result = find_model_from_input("test", mock_client, console)

        assert len(result.additional_info) == 5
        assert "Info 1" in result.additional_info
        assert "Info 5" in result.additional_info

    def test_find_model_console_output_contains_model_type(self, mock_client, console):
        """Test that console output includes model type."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="drama", formatted_name="Breaking Bad", additional_info=[])

        mock_client.responses.parse.return_value = mock_response

        find_model_from_input("Breaking Bad", mock_client, console)

        output = console.export_text()
        assert "drama" in output.lower()

    def test_find_model_uses_correct_timeout(self, mock_client, console):
        """Test that correct timeout is passed to API call."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="drama_movie", formatted_name="Test", additional_info=[])

        mock_client.responses.parse.return_value = mock_response

        find_model_from_input("test", mock_client, console)

        call_args = mock_client.responses.parse.call_args
        timeout = call_args.kwargs["timeout"]
        assert isinstance(timeout, Timeout)

    def test_find_model_instructions_include_options(self, mock_client, console):
        """Test that instructions include formatted options."""
        mock_response = Mock()
        mock_response.output_parsed = FindModelRequest(find_model="drama_movie", formatted_name="Test", additional_info=[])

        mock_client.responses.parse.return_value = mock_response

        find_model_from_input("test", mock_client, console)

        call_args = mock_client.responses.parse.call_args
        instructions = call_args.kwargs["instructions"]
        # Should contain model type options
        assert "movie" in instructions.lower() or "show" in instructions.lower() or "game" in instructions.lower()
