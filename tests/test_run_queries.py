"""Comprehensive tests for run_queries module."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from aiss.models.shared import ModelTypeResult, ResultType
from aiss.run_queries import run_the_query


class TestRunTheQuery:
    """Test run_the_query function."""

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_parsed_response")
    def test_run_query_parsed_mode(self, mock_get_parsed, mock_find_model, mock_openai_class):
        """Test running query in PARSED mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="A test movie",
            formatted_name="Test Movie",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test Movie", ResultType.PARSED)

        mock_find_model.assert_called_once()
        mock_get_parsed.assert_called_once()
        # Verify correct arguments
        call_args = mock_get_parsed.call_args[0]
        assert call_args[0] == model_result
        assert call_args[1] == mock_client

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_json_response")
    def test_run_query_json_mode(self, mock_get_json, mock_find_model, mock_openai_class):
        """Test running query in JSON mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="game",
            description="A test game",
            formatted_name="Test Game",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test Game", ResultType.JSON)

        mock_find_model.assert_called_once()
        mock_get_json.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_text_response")
    def test_run_query_text_mode(self, mock_get_text, mock_find_model, mock_openai_class):
        """Test running query in TEXT mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="show",
            description="A test show",
            formatted_name="Test Show",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test Show", ResultType.TEXT)

        mock_find_model.assert_called_once()
        mock_get_text.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_parsed_response")
    def test_run_query_string_parsed(self, mock_get_parsed, mock_find_model, mock_openai_class):
        """Test running query with string 'parsed' mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test", "parsed")

        mock_get_parsed.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_json_response")
    def test_run_query_string_json(self, mock_get_json, mock_find_model, mock_openai_class):
        """Test running query with string 'json' mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="game",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test", "json")

        mock_get_json.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_text_response")
    def test_run_query_string_text(self, mock_get_text, mock_find_model, mock_openai_class):
        """Test running query with string 'text' mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="show",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test", "text")

        mock_get_text.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_parsed_response")
    def test_run_query_none_result_type_defaults_to_parsed(self, mock_get_parsed, mock_find_model, mock_openai_class):
        """Test that None result_type defaults to PARSED."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test", None)

        mock_get_parsed.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    def test_run_query_empty_input(self, mock_openai_class):
        """Test running query with empty input text."""
        # Use real console since we're not actually rendering
        with patch("aiss.run_queries.Console") as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            run_the_query("", ResultType.PARSED)

            # Should print error and return early
            mock_console.print.assert_called_once()
            assert "Error" in str(mock_console.print.call_args)

    @patch("aiss.run_queries.OpenAI")
    def test_run_query_whitespace_only_input(self, mock_openai_class):
        """Test running query with whitespace-only input."""
        with patch("aiss.run_queries.Console") as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console

            run_the_query("   ", ResultType.JSON)

            # Should print error and return early
            mock_console.print.assert_called_once()
            assert "Error" in str(mock_console.print.call_args)

    @patch("aiss.run_queries.OpenAI")
    def test_run_query_invalid_result_type(self, mock_openai_class):
        """Test running query with invalid result type raises ValueError."""
        # This should raise ValueError when trying to convert to ResultType
        with pytest.raises(ValueError, match="is not a valid ResultType"):
            run_the_query("Test Input", "invalid_mode")

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    def test_run_query_model_detection_fails(self, mock_find_model, mock_openai_class):
        """Test running query when model detection fails."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_find_model.return_value = None

        # Use capsys to capture console output instead of mocking
        run_the_query("Unknown Input", ResultType.PARSED)

        # Should have called find_model and returned early
        mock_find_model.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_parsed_response")
    def test_run_query_strips_input_whitespace(self, mock_get_parsed, mock_find_model, mock_openai_class):
        """Test that input text whitespace is stripped."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("  Test Input  ", ResultType.PARSED)

        # Check that stripped text was used
        call_args = mock_find_model.call_args[0]
        assert call_args[0] == "Test Input"

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_json_response")
    def test_run_query_uppercase_string_mode(self, mock_get_json, mock_find_model, mock_openai_class):
        """Test running query with uppercase string mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test", "JSON")

        mock_get_json.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_text_response")
    def test_run_query_mixed_case_string_mode(self, mock_get_text, mock_find_model, mock_openai_class):
        """Test running query with mixed case string mode."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="show",
            description="Test content",
            formatted_name="Test",
        )
        mock_find_model.return_value = model_result

        run_the_query("Test", "TeXt")

        mock_get_text.assert_called_once()

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_parsed_response")
    @patch("aiss.run_queries.Progress")
    def test_run_query_progress_ui_created(self, mock_progress_class, mock_get_parsed, mock_find_model, mock_openai_class):
        """Test that Progress UI is created and used."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="Test movie content",
            formatted_name="Test Movie",
        )
        mock_find_model.return_value = model_result

        mock_progress = MagicMock()
        mock_progress_class.return_value.__enter__.return_value = mock_progress

        run_the_query("Test Movie", ResultType.PARSED)

        # Verify progress was used
        assert mock_progress.add_task.called
        assert mock_progress.update.called
        assert mock_progress.stop.called

    @patch("aiss.run_queries.OpenAI")
    @patch("aiss.run_queries.find_model_from_input")
    @patch("aiss.run_queries.get_parsed_response")
    def test_run_query_with_additional_info(self, mock_get_parsed, mock_find_model, mock_openai_class):
        """Test running query with model result containing additional info."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        model_result = ModelTypeResult(
            model_type="movie",
            description="Complex movie with additional information",
            formatted_name="Complex Movie",
            additional_info=["2020", "Drama", "Award Winner"],
        )
        mock_find_model.return_value = model_result

        run_the_query("Complex Movie", ResultType.PARSED)

        mock_get_parsed.assert_called_once()

    @patch("aiss.run_queries.load_dotenv")
    def test_load_dotenv_called_on_import(self, mock_load_dotenv):
        """Test that load_dotenv is called when module is imported."""
        # This test verifies the module-level call
        # Since we're importing the module, load_dotenv should have been called
        # We can't directly test this without re-importing, but we can verify
        # the import doesn't fail
        import aiss.run_queries

        assert hasattr(aiss.run_queries, "run_the_query")
