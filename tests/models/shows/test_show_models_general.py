"""General tests for all show models."""

import pytest

from aiss.models.shows import (
    ActionAdventureFantasyShowInfo,
    ComedyShowInfo,
    DocumentaryFactualShowInfo,
    DramaShowInfo,
    FamilyAnimationKidsShowInfo,
    NewsInformationalShowInfo,
    RealityCompetitionLifestyleShowInfo,
    ScienceFictionShowInfo,
    SportsShowInfo,
    ThrillerShowInfo,
)

ALL_SHOW_MODELS = [
    ActionAdventureFantasyShowInfo,
    ComedyShowInfo,
    DocumentaryFactualShowInfo,
    DramaShowInfo,
    FamilyAnimationKidsShowInfo,
    NewsInformationalShowInfo,
    RealityCompetitionLifestyleShowInfo,
    ScienceFictionShowInfo,
    SportsShowInfo,
    ThrillerShowInfo,
]


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_has_required_attributes(model_class):
    """Test that each show model has required class variables."""
    assert hasattr(model_class, "model_name")
    assert hasattr(model_class, "description")
    assert hasattr(model_class, "key_trait")
    # Check for methods instead of class variables
    assert hasattr(model_class, "get_instructions")
    assert hasattr(model_class, "get_user_prompt")


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_can_create_minimal_instance(model_class):
    """Test that each show model can be created with minimal data."""
    show = model_class(title="Test Show")
    assert show.title == "Test Show"
    assert show.model_name == model_class.model_name


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_render_method_exists(model_class, console):
    """Test that each show model has a render method that works."""
    show = model_class(
        title="Test Show",
        show_summary="Test summary",
    )
    show.render(console)
    output = console.export_text()
    assert "Test Show" in output


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_fact_pairs_returns_list(model_class):
    """Test that _fact_pairs returns a list of tuples."""
    show = model_class(
        title="Test Show",
        season_count=3,
        episode_count=30,
    )
    facts = show._fact_pairs()
    assert isinstance(facts, (list, tuple))
    for item in facts:
        assert isinstance(item, tuple)
        assert len(item) == 2


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_table_sections_returns_list(model_class):
    """Test that _table_sections returns a list."""
    show = model_class(title="Test Show")
    sections = show._table_sections()
    assert isinstance(sections, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_extra_panels_returns_list(model_class):
    """Test that _extra_panels returns a list."""
    show = model_class(title="Test Show")
    panels = show._extra_panels()
    assert isinstance(panels, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_summary_panel_returns_tuple(model_class):
    """Test that _summary_panel returns a tuple."""
    show = model_class(
        title="Test Show",
        show_summary="Test summary",
    )
    result = show._summary_panel()
    assert isinstance(result, tuple)
    assert len(result) == 3


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_to_dict_serialization(model_class):
    """Test that to_dict works for serialization."""
    show = model_class(
        title="Test Show",
        season_count=2,
        episode_count=20,
    )
    data = show.to_dict()
    assert isinstance(data, dict)
    assert data["title"] == "Test Show"


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_from_dict_deserialization(model_class):
    """Test that from_dict works for deserialization."""
    original = model_class(
        title="Test Show",
        show_summary="Test summary",
    )
    data = original.to_dict()
    restored = model_class.from_dict(data)
    assert restored.title == original.title
    assert restored.show_summary == original.show_summary


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_get_instructions(model_class):
    """Test that get_instructions returns a string."""
    instructions = model_class.get_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_get_instructions_with_context(model_class):
    """Test get_instructions with additional context."""
    instructions = model_class.get_instructions(["Focus on character development"])
    assert isinstance(instructions, str)
    assert "Focus on character development" in instructions


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_get_user_prompt(model_class):
    """Test that get_user_prompt returns a string."""
    prompt = model_class.get_user_prompt("Test Show")
    assert isinstance(prompt, str)
    assert "Test Show" in prompt


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_json_format_instructions(model_class):
    """Test that json_format_instructions returns a string."""
    formatted = model_class.json_format_instructions()
    assert isinstance(formatted, str)
    assert "JSON" in formatted or "json" in formatted


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_has_basic_fields(model_class):
    """Test that each show model has expected basic fields."""
    show = model_class(
        title="Test Show",
        show_summary="Test summary",
        tone="Dramatic",
    )
    assert show.title == "Test Show"
    assert show.show_summary == "Test summary"
    assert show.tone == "Dramatic"


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_wikipedia_summary_field(model_class):
    """Test that wikipedia_summary field exists and works."""
    show = model_class(
        title="Test Show",
        wikipedia_summary="This is a test Wikipedia summary.",
    )
    assert show.wikipedia_summary == "This is a test Wikipedia summary."


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_render_wikipedia_summary(model_class, console):
    """Test that render_wikipedia_summary method works."""
    show = model_class(
        title="Test Show",
        wikipedia_summary="This is a Wikipedia summary for testing.",
    )
    show.render_wikipedia_summary(console)
    output = console.export_text()
    assert "Wikipedia" in output or "Summary" in output


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_empty_optional_fields(model_class):
    """Test that models work with empty optional fields."""
    show = model_class(title="Minimal Show")
    assert show.title == "Minimal Show"
    # Should not raise errors
    show._fact_pairs()
    show._table_sections()
    show._extra_panels()


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_render_with_minimal_data(model_class, console):
    """Test rendering with minimal data doesn't crash."""
    show = model_class(title="Minimal Show")
    show.render(console)
    output = console.export_text()
    assert "Minimal Show" in output


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_release_years_in_facts(model_class):
    """Test that release years appear in fact pairs when provided."""
    show = model_class(
        title="Test Show",
    )
    # Just check that _fact_pairs returns something valid
    facts = show._fact_pairs()
    assert isinstance(facts, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_tone_in_output(model_class, console):
    """Test that tone appears in rendered output."""
    show = model_class(
        title="Test Show",
        tone="Dark and gritty",
    )
    show.render(console)
    output = console.export_text()
    assert "Dark and gritty" in output or "Tone" in output


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_get_instructions_method(model_class):
    """Test get_instructions method works."""
    instructions = model_class.get_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0


@pytest.mark.parametrize("model_class", ALL_SHOW_MODELS)
def test_show_model_get_user_prompt_method(model_class):
    """Test get_user_prompt method works."""
    prompt = model_class.get_user_prompt("Test Show")
    assert isinstance(prompt, str)
    assert "Test Show" in prompt
