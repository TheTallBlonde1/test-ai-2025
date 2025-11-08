from unittest.mock import Mock, patch

from rich.console import Console

from aiss.models.shared import ModelType, ModelTypeInput


@patch("aiss.pydantic_ai.pydantic_ai_std_parse.build_wikipedia_topic_context")
@patch("aiss.pydantic_ai.pydantic_ai_std_parse.augment_instructions_with_tool_hint")
def test_std_parse_success(mock_augment, mock_build_context):
    # Arrange
    from aiss.models.shows.drama_model import DramaShowInfo
    from aiss.pydantic_ai.pydantic_ai_std_parse import get_parsed_response

    console = Console()
    mock_build_context.return_value = ("Wikipedia summary", "Context hint")
    mock_augment.return_value = "Augmented instructions"

    # Fake Agent and run_sync result
    mock_agent_instance = Mock()
    mock_parsed_result = Mock(spec=DramaShowInfo)
    mock_parsed_result.render = Mock()
    mock_agent_instance.run_sync.return_value = Mock(output=mock_parsed_result)

    with patch("aiss.pydantic_ai.pydantic_ai_std_parse.Agent", return_value=mock_agent_instance):
        mti = ModelTypeInput(
            model_type=ModelType.DRAMA,
            description="Test drama",
            formatted_name="Test Show",
        )

        # Act
        result = get_parsed_response(mti, console)

        # Assert
        assert result is not None
        assert hasattr(result, "wikipedia_summary")
        mock_parsed_result.render.assert_called_once()


@patch("aiss.pydantic_ai.pydantic_ai_std_parse.build_wikipedia_topic_context")
@patch("aiss.pydantic_ai.pydantic_ai_std_parse.augment_instructions_with_tool_hint")
def test_std_parse_handles_no_output(mock_augment, mock_build_context):
    from aiss.pydantic_ai.pydantic_ai_std_parse import get_parsed_response

    console = Console()
    mock_build_context.return_value = ("Summary", "Context")
    mock_augment.return_value = "Instructions"

    mock_agent_instance = Mock()
    mock_agent_instance.run_sync.return_value = Mock(output=None)

    with patch("aiss.pydantic_ai.pydantic_ai_std_parse.Agent", return_value=mock_agent_instance):
        mti = ModelTypeInput(
            model_type=ModelType.DRAMA,
            description="Desc",
            formatted_name="Name",
        )
        result = get_parsed_response(mti, console)
        assert result is None
