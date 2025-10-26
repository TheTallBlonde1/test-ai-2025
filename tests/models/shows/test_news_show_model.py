"""Tests for NewsInformationalShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.news_model import (
    AnchorProfile,
    CorrespondentReport,
    NewsInformationalShowInfo,
    SegmentBlueprint,
)


@pytest.fixture
def news_show_full():
    """Create a fully populated news show instance for testing."""
    return NewsInformationalShowInfo(
        title="Evening News Hour",
        premise="Comprehensive daily news coverage",
        show_summary="Award-winning news program covering national and international events.",
        programme_type="Evening News",
        editorial_focus=["Politics", "Business", "International Affairs"],
        verification_standards="Multiple source verification required",
        tone="Professional and authoritative",
        primary_setting="News studio",
        season_count=25,
        episode_count=6500,
        episode_length_minutes=60,
        release_start_year=1995,
        release_end_year=0,
        age_rating="TV-PG",
        broadcast_schedule="Monday-Friday 6PM",
        digital_extensions="Website, mobile app, podcast",
        anchors=[
            AnchorProfile(
                name="Jane Anchor",
                role="Lead Anchor",
                expertise="Political journalism",
                tone="Calm and measured",
                tenure_years=15,
            )
        ],
        segments=[
            SegmentBlueprint(
                name="Top Stories",
                format_type="Headline block",
                duration_minutes=20,
                hosts=["Jane Anchor"],
                focus="Breaking news",
                recurrence="Every episode",
            )
        ],
        correspondent_reports=[
            CorrespondentReport(
                correspondent="Field Reporter",
                location="Washington DC",
                topic="Congressional hearing",
                status="Airing",
                date="2024-10-25",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Columbia Journalism Review",
                reviewer="Media Critic",
                score=8.5,
                summary="Consistently high quality journalism",
                quote="Sets the standard for evening news",
                publication_date="2020-01-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 25+",
                average_viewers=7000000,
                share=5.5,
                engagement_notes="Leading evening news program",
            )
        ],
        producers=["Executive Producer"],
        production_companies=[
            ProductionCompanyInfo(
                name="News Productions",
                founded_year=1990,
                start_year=1995,
                end_year=0,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="Major Network",
                country="USA",
                start_year=1995,
                end_year=0,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Network Distribution",
                territory="US",
                release_type="Broadcast",
                start_year=1995,
                end_year=0,
                revenue=100000000,
            )
        ],
    )


def test_news_basic_creation():
    """Test basic show creation."""
    show = NewsInformationalShowInfo(title="Test News")
    assert show.title == "Test News"
    assert show.model_name == "NewsInformationalShowInfo"


def test_news_fact_pairs(news_show_full):
    """Test fact pairs generation."""
    facts = dict(news_show_full._fact_pairs())
    assert "Editorial Focus" in facts
    assert facts["Editorial Focus"] == "Politics, Business, International Affairs"
    assert "Schedule" in facts


def test_news_render_includes_content(news_show_full, console):
    """Test render includes all expected content."""
    news_show_full.render(console)
    text = console.export_text()
    assert "Evening News Hour" in text


def test_news_instruction_helpers():
    """Test instruction helper methods."""
    combined = NewsInformationalShowInfo.get_instructions(["Focus on accuracy"])
    assert "Additional context" in combined


def test_news_anchors(news_show_full):
    """Test anchors data."""
    assert len(news_show_full.anchors) == 1
    assert news_show_full.anchors[0].name == "Jane Anchor"


def test_news_roundtrip():
    """Test serialization roundtrip."""
    original = NewsInformationalShowInfo(
        title="Roundtrip News",
        premise="Testing",
        programme_type="Morning News",
    )
    data = original.to_dict()
    restored = NewsInformationalShowInfo.from_dict(data)
    assert restored.title == original.title
