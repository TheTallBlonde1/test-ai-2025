"""Tests for RomanceMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    BoxOfficeInfo,
    CastMemberInfo,
    ProductionCompanyInfo,
    RomanticBeatInfo,
)
from aiss.models.movies.romance_model import RomanceMovieInfo


@pytest.fixture
def romance_movie_full():
    """Create a fully populated romance movie instance for testing."""
    return RomanceMovieInfo(
        title="Love in the City",
        tagline="Two hearts. One destiny.",
        synopsis="An architect and a chef fall in love while competing for the same property.",
        release_year=2024,
        runtime_minutes=112,
        genres=["Romance", "Comedy"],
        mpaa_rating="PG-13",
        directors=["Romance Director"],
        writers=["Love Writer"],
        producers=["Heart Producer"],
        original_language="English",
        countries=["USA"],
        rating=7.8,
        keywords=["love", "competition", "destiny"],
        cast=[
            CastMemberInfo(character="Emma Stone", actor="Leading Lady", role="Lead"),
            CastMemberInfo(character="James Carter", actor="Leading Man", role="Lead"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Heartfelt Films",
                founded_year=2005,
                start_year=2023,
                end_year=2024,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=20000000, gross_worldwide=120000000, gross_domestic=50000000),
        awards=["Best Romantic Film", "Audience Choice Award"],
        soundtrack_highlights=["Love Theme by Romantic Composer"],
        relationship_dynamics=["Rivals to lovers", "Professional competition", "Emotional vulnerability"],
        meet_cute_description="Emma and James clash at a property auction over the same building",
        romantic_beats=[
            RomanticBeatInfo(
                beat_name="The First Meeting",
                description="Emma and James clash at a property auction",
                emotional_shift="Tension and attraction begin",
                setting="Property Auction House",
            ),
            RomanticBeatInfo(
                beat_name="The Cooking Lesson",
                description="James teaches Emma to cook, walls come down",
                emotional_shift="Tenderness and trust develop",
                setting="James's Restaurant Kitchen",
            ),
        ],
        conflict_obstacles=["Business rivalry", "Past relationship trauma", "Family expectations"],
        ending_type="Happy ending - together with business partnership",
        chemistry_notes="Natural banter with undeniable physical chemistry",
    )


def test_romance_basic_creation():
    """Test basic romance movie creation."""
    movie = RomanceMovieInfo(title="Test Romance")
    assert movie.title == "Test Romance"
    assert movie.model_name == "RomanceMovieInfo"


def test_romance_additional_fact_pairs(romance_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(romance_movie_full._additional_fact_pairs())
    assert "auction" in facts["Meet-Cute"].lower()
    assert "together" in facts["Ending"].lower()


def test_romance_extra_tables(romance_movie_full):
    """Test extra tables generation."""
    tables = romance_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Romantic Beats" in titles


def test_romance_extra_panels(romance_movie_full):
    """Test extra panels generation."""
    panels = romance_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "Relationship Dynamics" in panel_titles
    assert "Conflicts" in panel_titles
    assert "Chemistry" in panel_titles


def test_romance_render_includes_content(romance_movie_full, console):
    """Test render includes all expected content."""
    romance_movie_full.render(console)
    text = console.export_text()
    assert "Love in the City" in text
    assert "Two hearts. One destiny." in text


def test_romance_instruction_helpers():
    """Test instruction helper methods."""
    combined = RomanceMovieInfo.get_instructions(["Focus on chemistry"])
    assert "Additional context" in combined
    assert "Focus on chemistry" in combined

    prompt = RomanceMovieInfo.get_user_prompt("Test Romance")
    assert "Test Romance" in prompt

    formatted = RomanceMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_romance_romantic_beats(romance_movie_full):
    """Test romantic beats data."""
    assert len(romance_movie_full.romantic_beats) == 2
    assert romance_movie_full.romantic_beats[0].beat_name == "The First Meeting"
    assert "Tension" in romance_movie_full.romantic_beats[0].emotional_shift


def test_romance_obstacles(romance_movie_full):
    """Test obstacles list."""
    assert len(romance_movie_full.conflict_obstacles) == 3
    assert "Business rivalry" in romance_movie_full.conflict_obstacles


def test_romance_relationship_dynamics(romance_movie_full):
    """Test relationship dynamics field."""
    assert len(romance_movie_full.relationship_dynamics) == 3
    assert "Rivals to lovers" in romance_movie_full.relationship_dynamics


def test_romance_meet_cute(romance_movie_full):
    """Test meet cute description."""
    assert "auction" in romance_movie_full.meet_cute_description.lower()


def test_romance_empty_optional_fields(console):
    """Test movie with minimal data."""
    movie = RomanceMovieInfo(
        title="Minimal Romance",
        synopsis="Basic romance",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    assert isinstance(facts, dict)


def test_romance_roundtrip():
    """Test serialization roundtrip."""
    original = RomanceMovieInfo(
        title="Roundtrip Romance",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=105,
        meet_cute_description="Test meet cute",
        ending_type="Happy",
    )
    data = original.to_dict()
    restored = RomanceMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.meet_cute_description == original.meet_cute_description
    assert restored.ending_type == original.ending_type


def test_romantic_beat_info_table_schema():
    """Test RomanticBeatInfo has table schema."""
    schema = RomanticBeatInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Beat" in headers
