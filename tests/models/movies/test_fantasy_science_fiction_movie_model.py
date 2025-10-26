"""Tests for FantasyScienceFictionMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    ActionSetPieceInfo,
    BoxOfficeInfo,
    CastMemberInfo,
    ProductionCompanyInfo,
)
from aiss.models.movies.fantasy_science_fiction_model import FantasyScienceFictionMovieInfo


@pytest.fixture
def fantasy_scifi_movie_full():
    """Create a fully populated fantasy/sci-fi movie instance for testing."""
    return FantasyScienceFictionMovieInfo(
        title="Quantum Nexus",
        tagline="Reality is just the beginning.",
        synopsis="A physicist discovers portals to parallel dimensions and must stop an interdimensional war.",
        release_year=2024,
        runtime_minutes=145,
        genres=["Science Fiction", "Action"],
        mpaa_rating="PG-13",
        directors=["Sci-Fi Director"],
        writers=["Sci-Fi Writer"],
        producers=["Sci-Fi Producer"],
        original_language="English",
        countries=["USA"],
        rating=8.3,
        keywords=["parallel dimensions", "quantum physics", "war"],
        cast=[
            CastMemberInfo(character="Dr. Alex Quantum", actor="Leading Sci-Fi Actor", role="Lead"),
            CastMemberInfo(character="Commander Zara", actor="Supporting Actor", role="Supporting"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Dimension Films",
                founded_year=2000,
                start_year=2022,
                end_year=2024,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=150000000, gross_worldwide=650000000, gross_domestic=250000000),
        awards=["Best Visual Effects", "Best Sound Design"],
        soundtrack_highlights=["Epic score by Sci-Fi Composer"],
        world_building_elements=[
            "Quantum Nexus - hub between dimensions",
            "Dimensional physics based on string theory",
            "Technology powered by quantum entanglement",
        ],
        technology_or_magic=[
            "Portal generators",
            "Quantum suits for dimensional travel",
            "Reality stabilizers",
        ],
        factions=[
            "The Nexus Council (interdimensional peacekeepers)",
            "The Void Collective (dimensional conquerors)",
            "Earth Defense Forces",
        ],
        mythology_notes="Ancient civilization predicted the Nexus; prophecy of the Quantum Traveler",
        timeline="2024 with flashbacks to dimensional war 100 years prior",
        visual_effects_partners=["ILM", "Weta Digital"],
        signature_set_pieces=[
            ActionSetPieceInfo(
                name="The Portal Battle",
                act="Act 2",
                location="The Quantum Nexus",
                stakes="Prevent dimensional collapse",
                practical_effects="Multi-dimensional combat with extensive VFX",
            ),
            ActionSetPieceInfo(
                name="The Nexus Collapse",
                act="Act 3",
                location="All Dimensions",
                stakes="Save reality itself",
                practical_effects="Reality unraveling sequence with practical and VFX",
            ),
        ],
    )


def test_fantasy_scifi_basic_creation():
    """Test basic fantasy/sci-fi movie creation."""
    movie = FantasyScienceFictionMovieInfo(title="Test Sci-Fi")
    assert movie.title == "Test Sci-Fi"
    assert movie.model_name == "FantasyScienceFictionMovieInfo"


def test_fantasy_scifi_additional_fact_pairs(fantasy_scifi_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(fantasy_scifi_movie_full._additional_fact_pairs())
    assert "2024" in facts["Timeline"]
    assert "Ancient civilization" in facts["Mythology"]


def test_fantasy_scifi_extra_tables(fantasy_scifi_movie_full):
    """Test extra tables generation."""
    tables = fantasy_scifi_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Signature Set Pieces" in titles


def test_fantasy_scifi_extra_panels(fantasy_scifi_movie_full):
    """Test extra panels generation."""
    panels = fantasy_scifi_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "World Building" in panel_titles
    assert "Technology / Magic" in panel_titles
    assert "Factions" in panel_titles
    assert "VFX Partners" in panel_titles


def test_fantasy_scifi_render_includes_content(fantasy_scifi_movie_full, console):
    """Test render includes all expected content."""
    fantasy_scifi_movie_full.render(console)
    text = console.export_text()
    assert "Quantum Nexus" in text
    assert "Reality is just the beginning." in text


def test_fantasy_scifi_instruction_helpers():
    """Test instruction helper methods."""
    combined = FantasyScienceFictionMovieInfo.get_instructions(["Emphasize world-building"])
    assert "Additional context" in combined
    assert "Emphasize world-building" in combined

    prompt = FantasyScienceFictionMovieInfo.get_user_prompt("Test Sci-Fi")
    assert "Test Sci-Fi" in prompt

    formatted = FantasyScienceFictionMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_fantasy_scifi_world_building_elements(fantasy_scifi_movie_full):
    """Test world building elements list."""
    assert len(fantasy_scifi_movie_full.world_building_elements) == 3
    assert "Quantum Nexus" in fantasy_scifi_movie_full.world_building_elements[0]


def test_fantasy_scifi_technology_or_magic(fantasy_scifi_movie_full):
    """Test technology/magic list."""
    assert len(fantasy_scifi_movie_full.technology_or_magic) == 3
    assert "Portal generators" in fantasy_scifi_movie_full.technology_or_magic


def test_fantasy_scifi_factions(fantasy_scifi_movie_full):
    """Test factions list."""
    assert len(fantasy_scifi_movie_full.factions) == 3
    assert "Nexus Council" in fantasy_scifi_movie_full.factions[0]


def test_fantasy_scifi_visual_effects_partners(fantasy_scifi_movie_full):
    """Test VFX partners list."""
    assert len(fantasy_scifi_movie_full.visual_effects_partners) == 2
    assert "ILM" in fantasy_scifi_movie_full.visual_effects_partners


def test_fantasy_scifi_signature_set_pieces(fantasy_scifi_movie_full):
    """Test signature set pieces data."""
    assert len(fantasy_scifi_movie_full.signature_set_pieces) == 2
    assert fantasy_scifi_movie_full.signature_set_pieces[0].name == "The Portal Battle"


def test_fantasy_scifi_empty_optional_fields(console):
    """Test movie with minimal data."""
    movie = FantasyScienceFictionMovieInfo(
        title="Minimal Sci-Fi",
        synopsis="Basic sci-fi",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    assert isinstance(facts, dict)


def test_fantasy_scifi_roundtrip():
    """Test serialization roundtrip."""
    original = FantasyScienceFictionMovieInfo(
        title="Roundtrip Sci-Fi",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=130,
        timeline="Future",
        mythology_notes="Test mythology",
    )
    data = original.to_dict()
    restored = FantasyScienceFictionMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.timeline == original.timeline
    assert restored.mythology_notes == original.mythology_notes


def test_action_set_piece_info_used_correctly():
    """Test ActionSetPieceInfo integration."""
    set_piece = ActionSetPieceInfo(
        name="Test Battle",
        act="Act 2",
        location="Test Location",
        stakes="High stakes",
        practical_effects="Practical and VFX",
    )
    assert set_piece.name == "Test Battle"
    schema = ActionSetPieceInfo.table_schema()
    assert len(schema) > 0
