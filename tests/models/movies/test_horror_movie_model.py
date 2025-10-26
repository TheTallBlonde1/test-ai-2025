"""Tests for HorrorMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    BoxOfficeInfo,
    CastMemberInfo,
    FearMomentInfo,
    ProductionCompanyInfo,
)
from aiss.models.movies.horror_model import HorrorMovieInfo


@pytest.fixture
def horror_movie_full():
    """Create a fully populated horror movie instance for testing."""
    return HorrorMovieInfo(
        title="The Haunting of Blackwood Manor",
        tagline="Some houses remember.",
        synopsis="A family moves into a historic manor, only to discover its terrifying secrets.",
        release_year=2024,
        runtime_minutes=118,
        genres=["Horror", "Thriller"],
        mpaa_rating="R",
        directors=["Horror Master"],
        writers=["Scary Writer"],
        producers=["Fright Producer"],
        original_language="English",
        countries=["USA"],
        rating=7.2,
        keywords=["haunted house", "psychological", "family terror"],
        cast=[
            CastMemberInfo(character="Sarah Mitchell", actor="Scream Queen", role="Lead"),
            CastMemberInfo(character="Tom Mitchell", actor="Horror Actor", role="Supporting"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Nightmare Productions",
                founded_year=1995,
                start_year=2023,
                end_year=2024,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=10000000, gross_worldwide=80000000, gross_domestic=35000000),
        awards=["Best Horror Film", "Best Sound Design"],
        soundtrack_highlights=["Atmospheric score by Composer Dark"],
        subgenre="psychological horror with supernatural elements",
        threat_entities=["The Spirit of Lady Blackwood", "Shadow Figures", "The House Itself"],
        fear_moments=[
            FearMomentInfo(
                moment_name="The Mirror Scene",
                type_of_fear="Jump scare",
                setup="Sarah walks past mirrors in dim hallway",
                payoff="Figure appears behind her in reflection",
                survivors_involved=["Sarah Mitchell"],
            ),
            FearMomentInfo(
                moment_name="The Basement Reveal",
                type_of_fear="Dread",
                setup="Sarah discovers hidden room in basement",
                payoff="Discovery of the manor's dark history",
                survivors_involved=["Sarah Mitchell", "Tom Mitchell"],
            ),
        ],
        gore_level="Minimal - focus on psychological terror",
        atmosphere="Claustrophobic and oppressive",
        final_survivors=["Sarah Mitchell (traumatized but alive)"],
        thematic_notes=["Guilt and past sins", "Family dysfunction", "Inescapable trauma"],
    )


def test_horror_basic_creation():
    """Test basic horror movie creation."""
    movie = HorrorMovieInfo(title="Test Horror")
    assert movie.title == "Test Horror"
    assert movie.model_name == "HorrorMovieInfo"


def test_horror_additional_fact_pairs(horror_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(horror_movie_full._additional_fact_pairs())
    assert "psychological" in facts["Subgenre"]
    assert facts["Gore"] == "Minimal - focus on psychological terror"
    assert facts["Atmosphere"] == "Claustrophobic and oppressive"


def test_horror_extra_tables(horror_movie_full):
    """Test extra tables generation."""
    tables = horror_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Fear Moments" in titles


def test_horror_extra_panels(horror_movie_full):
    """Test extra panels generation."""
    panels = horror_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "Threat Entities" in panel_titles
    assert "Final Survivors" in panel_titles
    assert "Themes" in panel_titles


def test_horror_render_includes_content(horror_movie_full, console):
    """Test render includes all expected content."""
    horror_movie_full.render(console)
    text = console.export_text()
    assert "The Haunting of Blackwood Manor" in text
    assert "Some houses remember." in text


def test_horror_instruction_helpers():
    """Test instruction helper methods."""
    combined = HorrorMovieInfo.get_instructions(["Emphasize atmosphere"])
    assert "Additional context" in combined
    assert "Emphasize atmosphere" in combined

    prompt = HorrorMovieInfo.get_user_prompt("Test Horror")
    assert "Test Horror" in prompt

    formatted = HorrorMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_horror_threat_entities(horror_movie_full):
    """Test threat entities list."""
    assert len(horror_movie_full.threat_entities) == 3
    assert "The Spirit of Lady Blackwood" in horror_movie_full.threat_entities


def test_horror_fear_moments(horror_movie_full):
    """Test fear moments data."""
    assert len(horror_movie_full.fear_moments) == 2
    assert horror_movie_full.fear_moments[0].moment_name == "The Mirror Scene"
    assert horror_movie_full.fear_moments[0].type_of_fear == "Jump scare"


def test_horror_final_survivors(horror_movie_full):
    """Test final survivors list."""
    assert len(horror_movie_full.final_survivors) == 1
    assert "Sarah Mitchell" in horror_movie_full.final_survivors[0]


def test_horror_thematic_notes(horror_movie_full):
    """Test thematic notes list."""
    assert len(horror_movie_full.thematic_notes) == 3
    assert "Guilt and past sins" in horror_movie_full.thematic_notes


def test_horror_empty_optional_fields(console):
    """Test movie with minimal data."""
    movie = HorrorMovieInfo(
        title="Minimal Horror",
        synopsis="Basic horror",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    assert isinstance(facts, dict)


def test_horror_roundtrip():
    """Test serialization roundtrip."""
    original = HorrorMovieInfo(
        title="Roundtrip Horror",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=110,
        subgenre="slasher",
        gore_level="High",
    )
    data = original.to_dict()
    restored = HorrorMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.subgenre == original.subgenre
    assert restored.gore_level == original.gore_level


def test_fear_moment_info_table_schema():
    """Test FearMomentInfo has table schema."""
    schema = FearMomentInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Moment" in headers
