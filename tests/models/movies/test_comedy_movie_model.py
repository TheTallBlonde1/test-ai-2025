"""Tests for ComedyMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    BoxOfficeInfo,
    CastMemberInfo,
    HumorBeatInfo,
    ProductionCompanyInfo,
)
from aiss.models.movies.comedy_model import ComedyMovieInfo


@pytest.fixture
def comedy_movie_full():
    """Create a fully populated comedy movie instance for testing."""
    return ComedyMovieInfo(
        title="The Office Party",
        tagline="Work hard. Party harder.",
        synopsis="An accountant's office party spirals into chaos when secrets are revealed.",
        release_year=2024,
        runtime_minutes=105,
        genres=["Comedy"],
        mpaa_rating="R",
        directors=["Comedy Director"],
        writers=["Funny Writer"],
        producers=["Laugh Producer"],
        original_language="English",
        countries=["USA"],
        rating=7.5,
        keywords=["workplace", "party", "chaos"],
        cast=[
            CastMemberInfo(character="Bob Jenkins", actor="Comedian One", role="Lead"),
            CastMemberInfo(character="Susan Taylor", actor="Comedian Two", role="Supporting"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Laugh Factory Studios",
                founded_year=2000,
                start_year=2023,
                end_year=2024,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=25000000, gross_worldwide=150000000, gross_domestic=60000000),
        awards=["Best Comedy Ensemble"],
        soundtrack_highlights=["Party Anthem by DJ Fun"],
        humor_styles=["Situational comedy", "Slapstick", "Witty banter"],
        comedic_beats=[
            HumorBeatInfo(
                situation="Bob's presentation goes hilariously wrong",
                punchline="Slides show his embarrassing vacation photos",
                characters_involved=["Bob Jenkins", "Boss"],
                comedic_style="Situational comedy",
            ),
            HumorBeatInfo(
                situation="Office rivals compete in embarrassing karaoke battle",
                punchline="Both forget the words and freestyle badly",
                characters_involved=["Susan Taylor", "Rival"],
                comedic_style="Physical comedy",
            ),
        ],
        running_gags=["Coffee machine always breaking", "Bob's tie getting stuck in things"],
        improv_notes="Extended improv session in the party dance scene",
        tone="Raucous with heartfelt moments",
        cameo_appearances=["Famous Comedian Guest", "Reality TV Star"],
    )


def test_comedy_basic_creation():
    """Test basic comedy movie creation."""
    movie = ComedyMovieInfo(title="Test Comedy")
    assert movie.title == "Test Comedy"
    assert movie.model_name == "ComedyMovieInfo"


def test_comedy_additional_fact_pairs(comedy_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(comedy_movie_full._additional_fact_pairs())
    assert facts["Tone"] == "Raucous with heartfelt moments"
    assert facts["Improv"] == "Extended improv session in the party dance scene"


def test_comedy_extra_tables(comedy_movie_full):
    """Test extra tables generation."""
    tables = comedy_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Comedic Beats" in titles


def test_comedy_extra_panels(comedy_movie_full):
    """Test extra panels generation."""
    panels = comedy_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "Humor Styles" in panel_titles
    assert "Running Gags" in panel_titles
    assert "Cameos" in panel_titles


def test_comedy_render_includes_content(comedy_movie_full, console):
    """Test render includes all expected content."""
    comedy_movie_full.render(console)
    text = console.export_text()
    assert "The Office Party" in text
    assert "Work hard. Party harder." in text


def test_comedy_instruction_helpers():
    """Test instruction helper methods."""
    combined = ComedyMovieInfo.get_instructions(["Focus on timing"])
    assert "Additional context" in combined
    assert "Focus on timing" in combined

    prompt = ComedyMovieInfo.get_user_prompt("Test Comedy")
    assert "Test Comedy" in prompt

    formatted = ComedyMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_comedy_humor_styles(comedy_movie_full):
    """Test humor styles list."""
    assert len(comedy_movie_full.humor_styles) == 3
    assert "Slapstick" in comedy_movie_full.humor_styles


def test_comedy_comedic_beats(comedy_movie_full):
    """Test comedic beats data."""
    assert len(comedy_movie_full.comedic_beats) == 2
    assert "presentation" in comedy_movie_full.comedic_beats[0].situation.lower()
    assert comedy_movie_full.comedic_beats[0].comedic_style == "Situational comedy"


def test_comedy_running_gags(comedy_movie_full):
    """Test running gags list."""
    assert len(comedy_movie_full.running_gags) == 2
    assert "Coffee machine" in comedy_movie_full.running_gags[0]


def test_comedy_cameo_appearances(comedy_movie_full):
    """Test cameo appearances list."""
    assert len(comedy_movie_full.cameo_appearances) == 2
    assert "Famous Comedian Guest" in comedy_movie_full.cameo_appearances


def test_comedy_empty_optional_fields(console):
    """Test movie with minimal data."""
    movie = ComedyMovieInfo(
        title="Minimal Comedy",
        synopsis="Basic comedy",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    assert isinstance(facts, dict)


def test_comedy_roundtrip():
    """Test serialization roundtrip."""
    original = ComedyMovieInfo(
        title="Roundtrip Comedy",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=95,
        tone="Test tone",
        humor_styles=["Test style"],
    )
    data = original.to_dict()
    restored = ComedyMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.tone == original.tone
    assert restored.humor_styles == original.humor_styles


def test_humor_beat_info_table_schema():
    """Test HumorBeatInfo has table schema."""
    schema = HumorBeatInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Situation" in headers
