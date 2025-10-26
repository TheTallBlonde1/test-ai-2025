"""Tests for ActionAdventureMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    ActionSetPieceInfo,
    BoxOfficeInfo,
    CastMemberInfo,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.movies.action_adventure_model import ActionAdventureMovieInfo


@pytest.fixture
def action_adventure_movie_full():
    """Create a fully populated action adventure movie instance for testing."""
    return ActionAdventureMovieInfo(
        title="Global Strike Force",
        tagline="One team. One mission. No limits.",
        synopsis="An elite team must prevent a global catastrophe across multiple continents.",
        release_year=2024,
        runtime_minutes=142,
        genres=["Action", "Adventure", "Thriller"],
        mpaa_rating="PG-13",
        directors=["Michael Bay"],
        writers=["John Writer", "Jane Screenwriter"],
        producers=["Big Producer"],
        original_language="English",
        countries=["USA"],
        rating=7.8,
        keywords=["explosions", "heroism", "global threat"],
        cast=[
            CastMemberInfo(character="Jack Stone", actor="Action Star", role="Lead"),
            CastMemberInfo(character="Maria Garcia", actor="Supporting Star", role="Supporting"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Big Action Studios",
                founded_year=1990,
                start_year=2022,
                end_year=2023,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=150000000, gross_worldwide=750000000, gross_domestic=250000000),
        distribution_info=[
            DistributionInfo(
                distributor="Global Pictures",
                territory="Worldwide",
                release_type="Theatrical",
                start_year=2024,
                end_year=0,
                revenue=750000000,
            )
        ],
        awards=["Best Action Sequence"],
        soundtrack_highlights=["Epic Battle Theme by Hans Zimmer"],
        hero_motivation="Save the world from nuclear threat",
        primary_locales=["New York", "Tokyo", "London", "Dubai"],
        antagonists=["Viktor Blackwood", "The Syndicate"],
        gear_and_tech=["Stealth Drones", "Smart Missiles", "Advanced Exosuits"],
        stunt_team=["Stunt Coordinator Pro", "Second Unit Director"],
        set_pieces=[
            ActionSetPieceInfo(
                name="Dubai Tower Chase",
                act="Act 2",
                location="Burj Khalifa, Dubai",
                stakes="Stop terrorist before detonation",
                practical_effects="Vertical chase with BASE jumping and practical stunts",
            ),
            ActionSetPieceInfo(
                name="Tokyo Harbor Battle",
                act="Act 3",
                location="Tokyo Bay",
                stakes="Prevent submarine launch",
                practical_effects="Underwater combat and boat chase with practical effects",
            ),
        ],
    )


def test_action_adventure_basic_creation():
    """Test basic action adventure movie creation."""
    movie = ActionAdventureMovieInfo(title="Test Action")
    assert movie.title == "Test Action"
    assert movie.model_name == "ActionAdventureMovieInfo"


def test_action_adventure_additional_fact_pairs(action_adventure_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(action_adventure_movie_full._additional_fact_pairs())
    assert facts["Hero Motivation"] == "Save the world from nuclear threat"
    assert "New York" in facts["Locales"]
    assert "Tokyo" in facts["Locales"]


def test_action_adventure_extra_tables(action_adventure_movie_full):
    """Test extra tables generation."""
    tables = action_adventure_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Set Pieces" in titles


def test_action_adventure_extra_panels(action_adventure_movie_full):
    """Test extra panels generation."""
    panels = action_adventure_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "Antagonists" in panel_titles
    assert "Gear & Tech" in panel_titles
    assert "Stunt Team" in panel_titles


def test_action_adventure_render_includes_content(action_adventure_movie_full, console):
    """Test render includes all expected content."""
    action_adventure_movie_full.render(console)
    text = console.export_text()
    assert "Global Strike Force" in text
    assert "One team. One mission. No limits." in text
    assert "Action Star" in text


def test_action_adventure_instruction_helpers():
    """Test instruction helper methods."""
    combined = ActionAdventureMovieInfo.get_instructions(["Focus on stunts"])
    assert "Additional context" in combined
    assert "Focus on stunts" in combined

    prompt = ActionAdventureMovieInfo.get_user_prompt("Test Action")
    assert "Test Action" in prompt

    formatted = ActionAdventureMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_action_adventure_set_pieces(action_adventure_movie_full):
    """Test set pieces data."""
    assert len(action_adventure_movie_full.set_pieces) == 2
    assert action_adventure_movie_full.set_pieces[0].name == "Dubai Tower Chase"
    assert action_adventure_movie_full.set_pieces[1].location == "Tokyo Bay"


def test_action_adventure_primary_locales(action_adventure_movie_full):
    """Test primary locales list."""
    assert len(action_adventure_movie_full.primary_locales) == 4
    assert "Dubai" in action_adventure_movie_full.primary_locales


def test_action_adventure_antagonists(action_adventure_movie_full):
    """Test antagonists list."""
    assert len(action_adventure_movie_full.antagonists) == 2
    assert "Viktor Blackwood" in action_adventure_movie_full.antagonists


def test_action_adventure_gear_and_tech(action_adventure_movie_full):
    """Test gear and technology list."""
    assert len(action_adventure_movie_full.gear_and_tech) == 3
    assert "Stealth Drones" in action_adventure_movie_full.gear_and_tech


def test_action_adventure_empty_optional_fields(console):
    """Test movie with minimal data."""
    movie = ActionAdventureMovieInfo(
        title="Minimal Action",
        synopsis="Basic action movie",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    # Should handle empty lists gracefully
    assert isinstance(facts, dict)


def test_action_adventure_roundtrip():
    """Test serialization roundtrip."""
    original = ActionAdventureMovieInfo(
        title="Roundtrip Action",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=120,
        hero_motivation="Test motivation",
        primary_locales=["Test Location"],
    )
    data = original.to_dict()
    restored = ActionAdventureMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.hero_motivation == original.hero_motivation
    assert restored.primary_locales == original.primary_locales


def test_action_set_piece_info_table_schema():
    """Test ActionSetPieceInfo has table schema."""
    schema = ActionSetPieceInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Set Piece" in headers or "Name" in headers
