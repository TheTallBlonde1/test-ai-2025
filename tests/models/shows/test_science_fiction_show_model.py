"""Tests for ScienceFictionShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.science_fiction_model import (
    ScienceFictionShowInfo,
    ScientificTheme,
    SciFiCharacterProfile,
    TechnologyConcept,
)


@pytest.fixture
def scifi_show_full():
    """Create a fully populated sci-fi show instance for testing."""
    return ScienceFictionShowInfo(
        title="Quantum Voyager",
        premise="Space crew explores uncharted dimensions",
        show_summary="Science fiction series following a starship crew's journey through quantum space.",
        subgenre_mix=["Space Opera", "Hard Sci-Fi"],
        world_building_notes="Multiverse with alternate physics",
        world_setting="2250 AD, Galactic Federation",
        tone="Thoughtful and adventurous",
        core_themes=["Exploration", "Identity", "Free will"],
        season_count=7,
        episode_count=154,
        average_runtime_minutes=45,
        release_start_year=2015,
        release_end_year=2022,
        age_rating="TV-14",
        effects_methodology="CGI with practical models",
        visual_palette="Dark with vibrant energy effects",
        characters=[
            SciFiCharacterProfile(
                name="Captain Nova",
                actor="Lead Actor",
                role="Ship Captain",
                species_or_origin="Human - Earth",
                specialization="Command and diplomacy",
                ethical_alignment="Pragmatic idealist",
                arc_summary="Learns to balance duty and morality",
            )
        ],
        technologies=[
            TechnologyConcept(
                name="Quantum Drive",
                category="Propulsion",
                description="Enables travel between quantum states",
                introduced_in="S01E01",
                scientific_basis="Quantum mechanics theory",
                ethical_implications="Risk of timeline disruption",
            )
        ],
        philosophical_themes=[
            ScientificTheme(
                theme="Free Will vs Determinism",
                episode_explored="S03E12",
                narrative_treatment="Crew faces predestined timeline",
                resolution="Choice matters even in determined universe",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Sci-Fi Magazine",
                reviewer="Genre Critic",
                score=9.0,
                summary="Ambitious and thought-provoking",
                quote="The best sci-fi on television",
                publication_date="2016-03-20",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 18-49",
                average_viewers=4000000,
                share=3.5,
                engagement_notes="Strong cult following",
            )
        ],
        creators=["Creator Name"],
        showrunners=["Showrunner Name"],
        science_consultants=["Dr. Physics Expert"],
        production_companies=[
            ProductionCompanyInfo(
                name="Sci-Fi Productions",
                founded_year=2010,
                start_year=2014,
                end_year=2022,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="Sci-Fi Channel",
                country="USA",
                start_year=2015,
                end_year=2022,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Global Streaming",
                territory="Worldwide",
                release_type="Broadcast + Streaming",
                start_year=2015,
                end_year=0,
                revenue=250000000,
            )
        ],
    )


def test_scifi_basic_creation():
    """Test basic show creation."""
    show = ScienceFictionShowInfo(title="Test Sci-Fi")
    assert show.title == "Test Sci-Fi"
    assert show.model_name == "ScienceFictionShowInfo"


def test_scifi_fact_pairs(scifi_show_full):
    """Test fact pairs generation."""
    facts = dict(scifi_show_full._fact_pairs())
    assert "Setting" in facts
    assert facts["Setting"] == "2250 AD, Galactic Federation"
    assert "Scientific Focus" in facts


def test_scifi_render_includes_content(scifi_show_full, console):
    """Test render includes all expected content."""
    scifi_show_full.render(console)
    text = console.export_text()
    assert "Quantum Voyager" in text


def test_scifi_instruction_helpers():
    """Test instruction helper methods."""
    combined = ScienceFictionShowInfo.get_instructions(["Focus on science"])
    assert "Additional context" in combined


def test_scifi_characters(scifi_show_full):
    """Test characters data."""
    assert len(scifi_show_full.characters) == 1
    assert scifi_show_full.characters[0].name == "Captain Nova"


def test_scifi_roundtrip():
    """Test serialization roundtrip."""
    original = ScienceFictionShowInfo(
        title="Roundtrip Sci-Fi",
        premise="Testing",
        timeline_setting="Future",
    )
    data = original.to_dict()
    restored = ScienceFictionShowInfo.from_dict(data)
    assert restored.title == original.title


def test_timeline_event_table_schema():
    """Test TimelineEvent table_schema."""
    from aiss.models.shows.science_fiction_model import TimelineEvent

    schema = TimelineEvent.table_schema()
    assert len(schema) > 0
    assert any(s.name == "year" for s in schema)
    assert any(s.name == "event" for s in schema)


def test_scientific_theme_table_schema():
    """Test ScientificTheme table_schema."""
    schema = ScientificTheme.table_schema()
    assert len(schema) > 0
    assert any(s.name == "theme" for s in schema)
    assert any(s.name == "question" for s in schema)


def test_scifi_show_with_technologies():
    """Test show with technologies renders correctly."""
    show = ScienceFictionShowInfo(
        title="Tech Show",
        show_summary="A show with tech",
        technologies=[
            TechnologyConcept(
                name="Warp Drive",
                category="Propulsion",
                description="Faster than light travel",
                introduced_in="Pilot",
                scientific_basis="Alcubierre metric",
                ethical_implications="Could disrupt causality",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Technologies" in section_titles


def test_scifi_show_with_timeline():
    """Test show with timeline events renders correctly."""
    from aiss.models.shows.science_fiction_model import TimelineEvent

    show = ScienceFictionShowInfo(
        title="Timeline Show",
        show_summary="A show with timeline",
        timeline_events=[
            TimelineEvent(
                year=2150,
                event="First Contact",
                location="Mars",
                impact="Changed humanity forever",
                featured_in=["S01E01"],
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Timeline" in section_titles


def test_scifi_show_with_themes():
    """Test show with scientific themes renders correctly."""
    show = ScienceFictionShowInfo(
        title="Theme Show",
        show_summary="A show with themes",
        themes=[
            ScientificTheme(
                theme="AI Consciousness",
                question="Can machines be sentient?",
                representative_episodes=["S02E05"],
                human_implication="What makes us human?",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Themes" in section_titles


def test_scifi_show_with_critical_reception():
    """Test show with critical reception renders correctly."""
    show = ScienceFictionShowInfo(
        title="Acclaimed Show",
        show_summary="A show with reviews",
        critical_reception=[
            CriticalResponse(
                outlet="TV Guide",
                reviewer="Critic",
                score=8.5,
                summary="Great show",
                quote="Must watch",
                publication_date="2020-01-01",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Critical Reception" in section_titles


def test_scifi_show_with_audience_metrics():
    """Test show with audience metrics renders correctly."""
    show = ScienceFictionShowInfo(
        title="Popular Show",
        show_summary="A show with metrics",
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="18-49",
                average_viewers=5000000,
                share=4.5,
                engagement_notes="Very popular",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Audience Metrics" in section_titles


def test_scifi_show_with_production_companies():
    """Test show with production companies renders correctly."""
    show = ScienceFictionShowInfo(
        title="Produced Show",
        show_summary="A show with companies",
        production_companies=[
            ProductionCompanyInfo(
                name="SciFi Studios",
                founded_year=2000,
                start_year=2015,
                end_year=2020,
                country="USA",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Production Companies" in section_titles


def test_scifi_fact_pairs_run_display_variations():
    """Test different run display scenarios."""
    # Both years missing
    show1 = ScienceFictionShowInfo(
        title="No Years",
        show_summary="Test",
        release_start_year=0,
        release_end_year=0,
    )
    facts1 = dict(show1._fact_pairs())
    assert "Run" in facts1

    # Same start and end year
    show2 = ScienceFictionShowInfo(
        title="Same Year",
        show_summary="Test",
        release_start_year=2020,
        release_end_year=2020,
    )
    facts2 = dict(show2._fact_pairs())
    assert "2020" in facts2["Run"]

    # Range of years
    show3 = ScienceFictionShowInfo(
        title="Range",
        show_summary="Test",
        release_start_year=2015,
        release_end_year=2020,
    )
    facts3 = dict(show3._fact_pairs())
    assert "2015" in facts3["Run"] and "2020" in facts3["Run"]
