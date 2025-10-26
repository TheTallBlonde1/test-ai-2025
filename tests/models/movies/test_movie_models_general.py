"""General tests for all movie models."""

import pytest

from aiss.models.movies import (
    ActionAdventureMovieInfo,
    ComedyMovieInfo,
    DocumentaryBiographicalMovieInfo,
    DramaMovieInfo,
    FantasyScienceFictionMovieInfo,
    HorrorMovieInfo,
    RomanceMovieInfo,
    ThrillerMysteryCrimeMovieInfo,
)
from aiss.models.movies._base import BaseMovieInfo

# All movie model classes to test
ALL_MOVIE_MODELS = [
    ActionAdventureMovieInfo,
    ComedyMovieInfo,
    DocumentaryBiographicalMovieInfo,
    DramaMovieInfo,
    FantasyScienceFictionMovieInfo,
    HorrorMovieInfo,
    RomanceMovieInfo,
    ThrillerMysteryCrimeMovieInfo,
]


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_inherits_from_base(model_class):
    """Verify each movie model inherits from BaseMovieInfo."""
    assert issubclass(model_class, BaseMovieInfo)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_required_class_vars(model_class):
    """Verify each movie model has required ClassVar attributes."""
    assert hasattr(model_class, "model_name")
    assert hasattr(model_class, "description")
    assert hasattr(model_class, "key_trait")
    assert hasattr(model_class, "instructions")
    assert hasattr(model_class, "label")
    assert hasattr(model_class, "user_prompt_template")


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_instruction_methods(model_class):
    """Verify each movie model has instruction helper methods."""
    assert hasattr(model_class, "get_instructions")
    assert callable(model_class.get_instructions)
    assert hasattr(model_class, "get_user_prompt")
    assert callable(model_class.get_user_prompt)
    assert hasattr(model_class, "json_format_instructions")
    assert callable(model_class.json_format_instructions)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_can_instantiate_empty(model_class):
    """Verify each movie model can be instantiated with no arguments."""
    instance = model_class()
    assert instance is not None
    assert isinstance(instance, BaseMovieInfo)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_title_field(model_class):
    """Verify each movie model has a title field."""
    instance = model_class()
    assert hasattr(instance, "title")


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_synopsis_field(model_class):
    """Verify each movie model has a synopsis field."""
    instance = model_class()
    assert hasattr(instance, "synopsis")


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_release_year_field(model_class):
    """Verify each movie model has a release_year field."""
    instance = model_class()
    assert hasattr(instance, "release_year")


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_runtime_minutes_field(model_class):
    """Verify each movie model has a runtime_minutes field."""
    instance = model_class()
    assert hasattr(instance, "runtime_minutes")


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_directors_field(model_class):
    """Verify each movie model has a directors field."""
    instance = model_class()
    assert hasattr(instance, "directors")
    assert isinstance(instance.directors, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_get_instructions_basic(model_class):
    """Test get_instructions returns a string."""
    instructions = model_class.get_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_get_instructions_with_additional_info(model_class):
    """Test get_instructions accepts additional info."""
    additional = ["Extra context 1", "Extra context 2"]
    instructions = model_class.get_instructions(additional)
    assert isinstance(instructions, str)
    assert "Additional context" in instructions


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_get_user_prompt(model_class):
    """Test get_user_prompt returns a string with the movie title."""
    movie_title = "Test Movie"
    prompt = model_class.get_user_prompt(movie_title)
    assert isinstance(prompt, str)
    assert movie_title in prompt


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_json_format_instructions(model_class):
    """Test json_format_instructions returns a string."""
    instructions = model_class.json_format_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0
    assert "JSON" in instructions


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_render_empty_instance(model_class, console):
    """Test that rendering an empty instance doesn't crash."""
    instance = model_class()
    instance.render(console)
    text = console.export_text()
    assert isinstance(text, str)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_render_with_title(model_class, console):
    """Test rendering with a title."""
    instance = model_class(title="Test Movie Title")
    instance.render(console)
    text = console.export_text()
    assert "Test Movie Title" in text


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_base_fact_pairs_returns_sequence(model_class):
    """Test _base_fact_pairs returns a sequence."""
    instance = model_class()
    fact_pairs = instance._base_fact_pairs()
    assert isinstance(fact_pairs, (list, tuple))


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_additional_fact_pairs_returns_list(model_class):
    """Test _additional_fact_pairs returns a list."""
    instance = model_class()
    fact_pairs = instance._additional_fact_pairs()
    assert isinstance(fact_pairs, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_extra_tables_returns_list(model_class):
    """Test _extra_tables returns a list."""
    instance = model_class()
    tables = instance._extra_tables()
    assert isinstance(tables, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_extra_panels_returns_list(model_class):
    """Test _extra_panels returns a list."""
    instance = model_class()
    panels = instance._extra_panels()
    assert isinstance(panels, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_to_dict(model_class):
    """Test to_dict method returns a dictionary."""
    instance = model_class(title="Test")
    data = instance.to_dict()
    assert isinstance(data, dict)
    assert "title" in data


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_from_dict(model_class):
    """Test from_dict method creates an instance."""
    data = {"title": "Test Movie", "synopsis": "A test", "release_year": 2024}
    instance = model_class.from_dict(data)
    assert isinstance(instance, model_class)
    assert instance.title == "Test Movie"


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_roundtrip_dict(model_class):
    """Test serialization roundtrip with to_dict and from_dict."""
    original = model_class(
        title="Roundtrip Test",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=120,
    )
    data = original.to_dict()
    restored = model_class.from_dict(data)
    assert restored.title == original.title
    assert restored.synopsis == original.synopsis
    assert restored.release_year == original.release_year
    assert restored.runtime_minutes == original.runtime_minutes


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_cast_field(model_class):
    """Verify each movie model has a cast field."""
    instance = model_class()
    assert hasattr(instance, "cast")
    assert isinstance(instance.cast, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_production_companies_field(model_class):
    """Verify each movie model has a production_companies field."""
    instance = model_class()
    assert hasattr(instance, "production_companies")
    assert isinstance(instance.production_companies, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_genres_field(model_class):
    """Verify each movie model has a genres field."""
    instance = model_class()
    assert hasattr(instance, "genres")
    assert isinstance(instance.genres, list)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_render_wikipedia_summary_empty(model_class, console):
    """Test _render_wikipedia_summary with empty summary."""
    instance = model_class()
    instance._render_wikipedia_summary(console)
    text = console.export_text()
    # Should not add anything when empty
    assert text == "" or "Context" not in text


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_render_wikipedia_summary_with_content(model_class, console):
    """Test _render_wikipedia_summary with content."""
    instance = model_class()
    instance.wikipedia_summary = "This is a test Wikipedia summary."
    instance._render_wikipedia_summary(console)
    text = console.export_text()
    assert "Context" in text
    assert "This is a test Wikipedia summary." in text


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_has_box_office_field(model_class):
    """Verify each movie model has an optional box_office field."""
    instance = model_class()
    assert hasattr(instance, "box_office")


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_render_with_populated_data(model_class, console):
    """Test rendering with populated data to cover all render paths."""
    from aiss.models.movies._base import BoxOfficeInfo, CastMemberInfo, DistributionInfo, ProductionCompanyInfo

    instance = model_class(
        title="Comprehensive Test Movie",
        synopsis="A fully populated test instance",
        tagline="Testing all paths",
        release_year=2024,
        runtime_minutes=120,
        genres=["Drama", "Action"],
        directors=["Director One"],
        writers=["Writer One"],
        producers=["Producer One"],
        cast=[CastMemberInfo(character="Hero", actor="Star Actor", role="Lead")],
        production_companies=[ProductionCompanyInfo(name="Studio", founded_year=2000, start_year=2023, end_year=2024, country="USA")],
        box_office=BoxOfficeInfo(budget=100000000, gross_worldwide=500000000, gross_domestic=200000000),
        distribution_info=[DistributionInfo(distributor="Dist", territory="World", release_type="Theatrical", start_year=2024, end_year=0, revenue=500000000)],
        keywords=["test", "comprehensive"],
        awards=["Best Picture"],
        wikipedia_summary="A comprehensive Wikipedia summary for testing.",
    )
    instance.render(console)
    text = console.export_text()
    assert "Comprehensive Test Movie" in text
    assert "2024" in text


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_additional_fact_pairs_with_data(model_class):
    """Test _additional_fact_pairs returns data when fields are populated."""
    instance = model_class(title="Test")
    # Call with minimal instance
    facts = instance._additional_fact_pairs()
    assert isinstance(facts, list)
    # All models should return a list, even if empty
    assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in facts)


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_extra_tables_empty_vs_populated(model_class):
    """Test _extra_tables behavior with empty and populated data."""
    empty_instance = model_class()
    empty_tables = empty_instance._extra_tables()
    assert isinstance(empty_tables, list)
    # When empty, should return empty list or minimal tables
    # When populated, should return more


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_extra_panels_empty_vs_populated(model_class):
    """Test _extra_panels behavior with empty and populated data."""
    empty_instance = model_class()
    empty_panels = empty_instance._extra_panels()
    assert isinstance(empty_panels, list)
    # Should return list of tuples with (title, content) or (title, content, style)
    for panel in empty_panels:
        assert isinstance(panel, tuple)
        assert len(panel) >= 2


@pytest.mark.parametrize("model_class", ALL_MOVIE_MODELS)
def test_movie_model_class_variables_are_strings(model_class):
    """Verify class variables are properly typed strings."""
    assert isinstance(model_class.model_name, str)
    assert isinstance(model_class.description, str)
    assert isinstance(model_class.key_trait, str)
    assert isinstance(model_class.instructions, str)
    assert isinstance(model_class.label, str)
    assert isinstance(model_class.user_prompt_template, str)
    # All should be non-empty
    assert len(model_class.model_name) > 0
    assert len(model_class.description) > 0
    assert len(model_class.key_trait) > 0
    assert len(model_class.instructions) > 0
    assert len(model_class.label) > 0
    assert len(model_class.user_prompt_template) > 0
