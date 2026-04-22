from unittest.mock import Mock, patch

from rich.console import Console

from aiss.models.shared import ModelType


def test_agents_flow_success():
    from aiss.models.shows.drama_model import DramaShowInfo
    from aiss.pydantic_ai.pydantic_ai_agents import find_model_from_input_pydantic, run_agents_parsed

    console = Console()

    # Detection output
    detection_output = Mock()
    detection_output.output = Mock(
        model_type=ModelType.DRAMA,
        formatted_name="Test Show",
        description="A test drama show",
        additional_info=["2024"],
    )

    # Wikipedia output
    wiki_output = Mock()
    wiki_output.output = Mock(summary="Wikipedia says: ...")

    # Specialist outputs (five calls returning strings)
    specialist_outputs = [Mock(output=f"note {i}") for i in range(5)]

    # Final formatting output
    parsed_instance = Mock(spec=DramaShowInfo)
    parsed_instance.render = Mock()
    final_output = Mock(output=parsed_instance)

    # Patch Agent so sequential instantiations return our mocks in order
    agent_instances = [
        Mock(run_sync=Mock(return_value=detection_output)),  # detection
        Mock(run_sync=Mock(return_value=wiki_output)),  # wikipedia
        *(Mock(run_sync=Mock(return_value=o)) for o in specialist_outputs),  # specialists
        Mock(run_sync=Mock(return_value=final_output)),  # formatter
    ]

    with patch("aiss.pydantic_ai.pydantic_ai_agents.Agent", side_effect=agent_instances):
        result = run_agents_parsed("Detect this: Test Show", console)

    assert result is not None
    parsed_instance.render.assert_called_once()
    assert hasattr(result, "wikipedia_summary")

    with patch("aiss.pydantic_ai.pydantic_ai_agents.Agent", return_value=Mock(run_sync=Mock(return_value=detection_output))):
        detection_result = find_model_from_input_pydantic("Detect this: Test Show", console)
    assert detection_result is not None
    assert detection_result.model_type == ModelType.DRAMA
    assert detection_result.formatted_name == "Test Show"


def test_agents_flow_unknown_type():
    from aiss.pydantic_ai.pydantic_ai_agents import run_agents_parsed

    console = Console()

    # Detection outputs an unknown type
    detection_output = Mock()
    detection_output.output = Mock(
        model_type=Mock(value="unknown_type"),
        formatted_name="X",
        description="Y",
        additional_info=None,
    )

    with patch("aiss.pydantic_ai.pydantic_ai_agents.Agent", return_value=Mock(run_sync=Mock(return_value=detection_output))):
        result = run_agents_parsed("Some input", console)
    assert result is None
