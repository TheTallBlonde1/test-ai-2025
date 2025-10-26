"""Tests for ThrillerShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.thriller_model import (
    InvestigatorProfile,
    MajorCaseFile,
    ThrillerShowInfo,
)


@pytest.fixture
def thriller_show_full():
    """Create a fully populated thriller show instance for testing."""
    return ThrillerShowInfo(
        title="Dark Investigation",
        premise="Elite detective unit solves complex crimes",
        show_summary="Psychological thriller following a team of investigators.",
        subgenre="Crime Procedural with psychological elements",
        narrative_structure="Serialized with case-of-week elements",
        tone="Dark and suspenseful",
        primary_setting="Metropolitan police department",
        core_themes=["Justice", "Morality", "Truth"],
        season_count=8,
        episode_count=160,
        average_runtime_minutes=45,
        release_start_year=2012,
        release_end_year=2020,
        age_rating="TV-14",
        pacing_style="Slow-burn with intense moments",
        tension_devices=["Red herrings", "Character secrets", "Time pressure"],
        investigators=[
            InvestigatorProfile(
                name="Detective Sarah Hunt",
                actor="Lead Actress",
                role="Lead Detective",
                specialty="Psychological profiling",
                personal_motivation="Sister's unsolved murder",
                moral_alignment="Pragmatic with strong ethics",
                status="Active",
            )
        ],
        major_cases=[
            MajorCaseFile(
                case_name="The Mirror Killer",
                season=3,
                synopsis="Serial killer leaves cryptic mirror messages",
                stakes="Multiple victims, media pressure",
                key_twist="Killer is victim of original crime",
                resolution_status="Solved",
                antagonists_involved=["Mirror Killer"],
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="TV Thriller Review",
                reviewer="Crime TV Critic",
                score=8.7,
                summary="Gripping psychological thriller",
                quote="Masterclass in suspense",
                publication_date="2013-10-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 25-54",
                average_viewers=6000000,
                share=4.2,
                engagement_notes="High episode retention",
            )
        ],
        showrunners=["Showrunner Name"],
        head_writers=["Head Writer"],
        crime_consultants=["Former FBI Agent"],
        production_companies=[
            ProductionCompanyInfo(
                name="Thriller Productions",
                founded_year=2008,
                start_year=2011,
                end_year=2020,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="Crime Network",
                country="USA",
                start_year=2012,
                end_year=2020,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Crime Distribution",
                territory="Worldwide",
                release_type="Broadcast + Streaming",
                start_year=2012,
                end_year=0,
                revenue=180000000,
            )
        ],
    )


def test_thriller_basic_creation():
    """Test basic show creation."""
    show = ThrillerShowInfo(title="Test Thriller")
    assert show.title == "Test Thriller"
    assert show.model_name == "ThrillerShowInfo"


def test_thriller_fact_pairs(thriller_show_full):
    """Test fact pairs generation."""
    facts = dict(thriller_show_full._fact_pairs())
    assert "Crime Procedural" in facts["Subgenre"]


def test_thriller_render_includes_content(thriller_show_full, console):
    """Test render includes all expected content."""
    thriller_show_full.render(console)
    text = console.export_text()
    assert "Dark Investigation" in text


def test_thriller_instruction_helpers():
    """Test instruction helper methods."""
    combined = ThrillerShowInfo.get_instructions(["Focus on suspense"])
    assert "Additional context" in combined


def test_thriller_investigators(thriller_show_full):
    """Test investigators data."""
    assert len(thriller_show_full.investigators) == 1
    assert thriller_show_full.investigators[0].name == "Detective Sarah Hunt"


def test_thriller_roundtrip():
    """Test serialization roundtrip."""
    original = ThrillerShowInfo(
        title="Roundtrip Thriller",
        premise="Testing",
        subgenre="Crime",
    )
    data = original.to_dict()
    restored = ThrillerShowInfo.from_dict(data)
    assert restored.title == original.title
