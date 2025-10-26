"""Tests for RealityCompetitionLifestyleShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.reality_model import (
    ChallengeInfo,
    HostJudgeProfile,
    ParticipantProfile,
    RealityCompetitionLifestyleShowInfo,
)


@pytest.fixture
def reality_show_full():
    """Create a fully populated reality show instance for testing."""
    return RealityCompetitionLifestyleShowInfo(
        title="Master Chef Competition",
        premise="Home cooks compete for culinary glory",
        show_summary="Intense cooking competition featuring amateur chefs.",
        format_type="Competition",
        tone="High-stakes drama",
        primary_setting="Professional kitchen",
        season_count=10,
        episode_count=200,
        episode_length_minutes=45,
        release_start_year=2010,
        release_end_year=2020,
        age_rating="TV-PG",
        prize_structure="$250,000 and cookbook deal",
        filming_locations=["Los Angeles studio"],
        hosts_and_judges=[
            HostJudgeProfile(
                name="Gordon Chef",
                role="Head Judge",
                expertise="Michelin-starred chef",
                personality_traits=["Tough", "Fair"],
                seasons_present=[1, 2, 3, 4, 5],
            )
        ],
        participants=[
            ParticipantProfile(
                name="Home Cook Jane",
                archetype="Underdog",
                background="Self-taught home cook",
                standout_skills=["Baking", "Presentation"],
                season_appearance=1,
                notable_moments=["Perfect soufflé"],
                final_outcome="Winner",
            )
        ],
        challenges=[
            ChallengeInfo(
                name="Mystery Box",
                challenge_type="Individual",
                description="Create dish from mystery ingredients",
                typical_duration_minutes=60,
                evaluation_criteria=["Creativity", "Taste", "Presentation"],
                recurrence="Every episode",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Reality TV Magazine",
                reviewer="TV Critic",
                score=8.0,
                summary="Compelling competition format",
                quote="Raises the bar for cooking shows",
                publication_date="2010-06-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 18-49",
                average_viewers=5000000,
                share=4.0,
                engagement_notes="Strong social media engagement",
            )
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Reality Productions",
                founded_year=2005,
                start_year=2009,
                end_year=2020,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="Food Network",
                country="USA",
                start_year=2010,
                end_year=2020,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Food Network Distribution",
                territory="Worldwide",
                release_type="Broadcast + Streaming",
                start_year=2010,
                end_year=0,
                revenue=150000000,
            )
        ],
    )


def test_reality_basic_creation():
    """Test basic show creation."""
    show = RealityCompetitionLifestyleShowInfo(title="Test Reality")
    assert show.title == "Test Reality"
    assert show.model_name == "RealityCompetitionLifestyleShowInfo"


def test_reality_fact_pairs(reality_show_full):
    """Test fact pairs generation."""
    facts = dict(reality_show_full._fact_pairs())
    assert "Subgenre" in facts
    assert "Tone" in facts
    assert facts["Tone"] == "High-stakes drama"


def test_reality_render_includes_content(reality_show_full, console):
    """Test render includes all expected content."""
    reality_show_full.render(console)
    text = console.export_text()
    assert "Master Chef" in text


def test_reality_instruction_helpers():
    """Test instruction helper methods."""
    combined = RealityCompetitionLifestyleShowInfo.get_instructions(["Focus on drama"])
    assert "Additional context" in combined


def test_reality_hosts_judges(reality_show_full):
    """Test hosts/judges data."""
    assert len(reality_show_full.hosts_and_judges) == 1
    assert reality_show_full.hosts_and_judges[0].name == "Gordon Chef"


def test_reality_roundtrip():
    """Test serialization roundtrip."""
    original = RealityCompetitionLifestyleShowInfo(
        title="Roundtrip Reality",
        premise="Testing",
        format_type="Competition",
    )
    data = original.to_dict()
    restored = RealityCompetitionLifestyleShowInfo.from_dict(data)
    assert restored.title == original.title
