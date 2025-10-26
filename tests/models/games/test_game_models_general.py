"""General tests for all game models."""

import pytest

from aiss.models.games import (
    ActionAdventureGameInfo,
    HorrorSurvivalGameInfo,
    MmoOnlineGameInfo,
    PuzzleStrategyGameInfo,
    RolePlayingGameInfo,
    ShooterGameInfo,
    SimulationSandboxGameInfo,
    SportsRacingGameInfo,
)
from aiss.models.games._base import GameFormatBase

# All game model classes to test
ALL_GAME_MODELS = [
    ActionAdventureGameInfo,
    HorrorSurvivalGameInfo,
    MmoOnlineGameInfo,
    PuzzleStrategyGameInfo,
    RolePlayingGameInfo,
    ShooterGameInfo,
    SimulationSandboxGameInfo,
    SportsRacingGameInfo,
]


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_inherits_from_base(model_class):
    """Verify each game model inherits from GameFormatBase."""
    assert issubclass(model_class, GameFormatBase)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_required_class_vars(model_class):
    """Verify each game model has required ClassVar attributes."""
    assert hasattr(model_class, "model_name")
    assert hasattr(model_class, "description")
    assert hasattr(model_class, "key_trait")
    assert hasattr(model_class, "summary_title_fallback")
    assert hasattr(model_class, "summary_attributes")


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_instruction_methods(model_class):
    """Verify each game model has instruction helper methods."""
    assert hasattr(model_class, "get_instructions")
    assert callable(model_class.get_instructions)
    assert hasattr(model_class, "get_user_prompt")
    assert callable(model_class.get_user_prompt)
    assert hasattr(model_class, "json_format_instructions")
    assert callable(model_class.json_format_instructions)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_can_instantiate_empty(model_class):
    """Verify each game model can be instantiated with no arguments."""
    instance = model_class()
    assert instance is not None
    assert isinstance(instance, GameFormatBase)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_title_field(model_class):
    """Verify each game model has a title field."""
    instance = model_class()
    assert hasattr(instance, "title")


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_game_summary_field(model_class):
    """Verify each game model has a game_summary field."""
    instance = model_class()
    assert hasattr(instance, "game_summary")


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_core_loop_field(model_class):
    """Verify each game model has a core_loop field."""
    instance = model_class()
    assert hasattr(instance, "core_loop")


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_release_year_field(model_class):
    """Verify each game model has a release_year field."""
    instance = model_class()
    assert hasattr(instance, "release_year")


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_get_instructions_basic(model_class):
    """Test get_instructions returns a string."""
    instructions = model_class.get_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_get_instructions_with_additional_info(model_class):
    """Test get_instructions accepts additional info."""
    additional = ["Extra context 1", "Extra context 2"]
    instructions = model_class.get_instructions(additional)
    assert isinstance(instructions, str)
    assert "Additional context" in instructions or "Extra context" in instructions


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_get_user_prompt(model_class):
    """Test get_user_prompt returns a string with the game name."""
    game_name = "Test Game"
    prompt = model_class.get_user_prompt(game_name)
    assert isinstance(prompt, str)
    assert game_name in prompt


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_json_format_instructions(model_class):
    """Test json_format_instructions returns a string."""
    instructions = model_class.json_format_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_render_empty_instance(model_class, console):
    """Test that rendering an empty instance doesn't crash."""
    instance = model_class()
    instance.render(console)
    text = console.export_text()
    assert isinstance(text, str)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_render_with_title(model_class, console):
    """Test rendering with a title."""
    instance = model_class(title="Test Game Title")
    instance.render(console)
    text = console.export_text()
    assert "Test Game Title" in text


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_fact_pairs_returns_sequence(model_class):
    """Test _fact_pairs returns a sequence."""
    instance = model_class()
    fact_pairs = instance._fact_pairs()
    assert isinstance(fact_pairs, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_table_sections_returns_sequence(model_class):
    """Test _table_sections returns a sequence."""
    instance = model_class()
    sections = instance._table_sections()
    assert isinstance(sections, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_extra_panels_returns_sequence(model_class):
    """Test _extra_panels returns a sequence."""
    instance = model_class()
    panels = instance._extra_panels()
    assert isinstance(panels, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_summary_panel_returns_tuple(model_class):
    """Test _summary_panel returns a tuple with title, lines, style."""
    instance = model_class(title="Test Title", game_summary="Test summary")
    title, lines, style = instance._summary_panel()
    assert isinstance(title, str)
    assert isinstance(lines, (list, tuple))
    assert isinstance(style, str)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_to_dict(model_class):
    """Test to_dict method returns a dictionary."""
    instance = model_class(title="Test")
    data = instance.to_dict()
    assert isinstance(data, dict)
    assert "title" in data


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_from_dict(model_class):
    """Test from_dict method creates an instance."""
    data = {"title": "Test Game", "game_summary": "A test", "core_loop": "Test loop"}
    instance = model_class.from_dict(data)
    assert isinstance(instance, model_class)
    assert instance.title == "Test Game"


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_roundtrip_dict(model_class):
    """Test serialization roundtrip with to_dict and from_dict."""
    original = model_class(
        title="Roundtrip Test",
        game_summary="Testing serialization",
        core_loop="test -> verify -> iterate",
        release_year=2024,
    )
    data = original.to_dict()
    restored = model_class.from_dict(data)
    assert restored.title == original.title
    assert restored.game_summary == original.game_summary
    assert restored.core_loop == original.core_loop
    assert restored.release_year == original.release_year


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_developers_field(model_class):
    """Verify each game model has a developers field."""
    instance = model_class()
    assert hasattr(instance, "developers")
    assert isinstance(instance.developers, list)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_publishers_field(model_class):
    """Verify each game model has a publishers field."""
    instance = model_class()
    assert hasattr(instance, "publishers")
    assert isinstance(instance.publishers, list)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_platform_releases_field(model_class):
    """Verify each game model has a platform_releases field."""
    instance = model_class()
    assert hasattr(instance, "platform_releases")
    assert isinstance(instance.platform_releases, list)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_has_accessibility_features_field(model_class):
    """Verify each game model has accessibility_features field."""
    instance = model_class()
    assert hasattr(instance, "accessibility_features")
    assert isinstance(instance.accessibility_features, list)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_render_wikipedia_summary_empty(model_class, console):
    """Test render_wikipedia_summary with empty summary."""
    instance = model_class()
    instance.render_wikipedia_summary(console)
    text = console.export_text()
    # Should not add anything when empty
    assert text == "" or "Context" not in text


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_render_wikipedia_summary_with_content(model_class, console):
    """Test render_wikipedia_summary with content."""
    instance = model_class()
    instance.wikipedia_summary = "This is a test Wikipedia summary."
    instance.render_wikipedia_summary(console)
    text = console.export_text()
    assert "Context" in text
    assert "This is a test Wikipedia summary." in text


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_render_with_populated_data(model_class, console):
    """Test rendering with populated data to cover all render paths."""
    from aiss.models.games._base import AccessibilityFeatureInfo, PlatformReleaseInfo, StudioProfile

    instance = model_class(
        title="Comprehensive Test Game",
        game_summary="A fully populated test instance",
        tagline="Testing all paths",
        core_loop="test -> render -> verify",
        release_year=2024,
        genres=["Action", "Adventure"],
        developers=[StudioProfile(name="Dev Studio", founded_year=2010, country="USA")],
        publishers=[StudioProfile(name="Publisher", founded_year=2005, country="USA")],
        platform_releases=[PlatformReleaseInfo(platform="PC", release_date="2024-01-01", version="1.0")],
        accessibility_features=[AccessibilityFeatureInfo(feature="Subtitles", implementation="Full subtitles")],
        wikipedia_summary="A comprehensive Wikipedia summary for testing.",
    )
    instance.render(console)
    text = console.export_text()
    assert "Comprehensive Test Game" in text
    assert "2024" in text


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_class_variables_are_strings(model_class):
    """Verify class variables are properly typed strings."""
    assert isinstance(model_class.model_name, str)
    assert isinstance(model_class.description, str)
    assert isinstance(model_class.key_trait, str)
    assert isinstance(model_class.summary_title_fallback, str)
    # All should be non-empty
    assert len(model_class.model_name) > 0
    assert len(model_class.description) > 0
    assert len(model_class.key_trait) > 0
    assert len(model_class.summary_title_fallback) > 0


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_summary_attributes_is_sequence(model_class):
    """Verify summary_attributes is a sequence."""
    assert hasattr(model_class, "summary_attributes")
    from collections.abc import Sequence

    assert isinstance(model_class.summary_attributes, Sequence)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_fact_pairs_with_data(model_class):
    """Test _fact_pairs returns proper data when fields are populated."""
    instance = model_class(
        title="Test Game",
        release_year=2024,
        core_loop="test loop",
    )
    facts = instance._fact_pairs()
    assert isinstance(facts, (list, tuple))
    assert len(facts) > 0
    # All should be tuples of (str, str)
    for pair in facts:
        assert isinstance(pair, tuple)
        assert len(pair) == 2
        assert isinstance(pair[0], str)
        assert isinstance(pair[1], str)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_table_sections_structure(model_class):
    """Test _table_sections returns proper structure."""
    instance = model_class()
    sections = instance._table_sections()
    assert isinstance(sections, (list, tuple))
    # Each section should be (title, schema, data)
    for section in sections:
        assert isinstance(section, tuple)
        assert len(section) == 3
        title, schema, data = section
        assert isinstance(title, str)
        assert isinstance(schema, list)
        assert isinstance(data, list)


@pytest.mark.parametrize("model_class", ALL_GAME_MODELS)
def test_game_model_extra_panels_structure(model_class):
    """Test _extra_panels returns proper structure."""
    instance = model_class()
    panels = instance._extra_panels()
    assert isinstance(panels, (list, tuple))
    # Each panel should be (title, content) or (title, content, style)
    for panel in panels:
        assert isinstance(panel, tuple)
        assert len(panel) >= 2
        assert isinstance(panel[0], str)  # title
        assert isinstance(panel[1], str)  # content
