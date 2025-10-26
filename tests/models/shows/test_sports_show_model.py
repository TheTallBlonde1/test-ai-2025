"""Tests for SportsShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.sports_model import (
    CoverageSegment,
    SportsPresenter,
    SportsShowInfo,
    TeamAthleteFeature,
)


@pytest.fixture
def sports_show_full():
    """Create a fully populated sports show instance for testing."""
    return SportsShowInfo(
        title="Sports Tonight",
        premise="Comprehensive sports news and analysis",
        show_summary="Daily sports show covering all major leagues and events.",
        programme_type="Sports News",
        primary_sports_covered=["Football", "Basketball", "Baseball"],
        editorial_slant="Analytical and fair",
        tone="Energetic and informative",
        primary_setting="Sports studio",
        season_count=20,
        episode_count=5000,
        episode_length_minutes=60,
        release_start_year=2000,
        release_end_year=0,
        age_rating="TV-G",
        broadcast_schedule="Daily 7PM",
        digital_presence="Website, app, social media",
        presenters=[
            SportsPresenter(
                name="Mike Sports",
                role="Host",
                expertise="Football analysis",
                former_athlete=True,
                tone="Enthusiastic and knowledgeable",
            )
        ],
        coverage_segments=[
            CoverageSegment(
                name="Top Plays",
                sport="All sports",
                focus="Highlight reel",
                schedule_slot="Opening",
                hosts=["Mike Sports"],
                duration_minutes=10,
            )
        ],
        featured_teams_athletes=[
            TeamAthleteFeature(
                subject="Championship Team",
                league="Football",
                feature_type="Title run",
                storyline="Championship game",
                stats_highlight="Champions",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Sports Media Review",
                reviewer="Sports Critic",
                score=8.5,
                summary="Comprehensive sports coverage",
                quote="The go-to show for sports news",
                publication_date="2005-01-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Sports fans 18-54",
                average_viewers=3000000,
                share=4.5,
                engagement_notes="Consistent viewership",
            )
        ],
        producers=["Sports Producer"],
        production_companies=[
            ProductionCompanyInfo(
                name="Sports Network Productions",
                founded_year=1995,
                start_year=1999,
                end_year=0,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="Sports Network",
                country="USA",
                start_year=2000,
                end_year=0,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Sports Distribution",
                territory="US",
                release_type="Broadcast",
                start_year=2000,
                end_year=0,
                revenue=200000000,
            )
        ],
    )


def test_sports_basic_creation():
    """Test basic show creation."""
    show = SportsShowInfo(title="Test Sports")
    assert show.title == "Test Sports"
    assert show.model_name == "SportsShowInfo"


def test_sports_fact_pairs(sports_show_full):
    """Test fact pairs generation."""
    facts = dict(sports_show_full._fact_pairs())
    assert "Sports" in facts
    assert "Schedule" in facts


def test_sports_render_includes_content(sports_show_full, console):
    """Test render includes all expected content."""
    sports_show_full.render(console)
    text = console.export_text()
    assert "Sports Tonight" in text


def test_sports_instruction_helpers():
    """Test instruction helper methods."""
    combined = SportsShowInfo.get_instructions(["Focus on analysis"])
    assert "Additional context" in combined


def test_sports_presenters(sports_show_full):
    """Test presenters data."""
    assert len(sports_show_full.presenters) == 1
    assert sports_show_full.presenters[0].name == "Mike Sports"


def test_sports_roundtrip():
    """Test serialization roundtrip."""
    original = SportsShowInfo(
        title="Roundtrip Sports",
        premise="Testing",
        programme_type="Sports News",
    )
    data = original.to_dict()
    restored = SportsShowInfo.from_dict(data)
    assert restored.title == original.title


def test_team_athlete_feature_table_schema():
    """Test TeamAthleteFeature table_schema."""
    schema = TeamAthleteFeature.table_schema()
    assert len(schema) > 0
    assert any(s.name == "subject" for s in schema)
    assert any(s.name == "league" for s in schema)


def test_season_event_block_table_schema():
    """Test SeasonEventBlock table_schema."""
    from aiss.models.shows.sports_model import SeasonEventBlock

    schema = SeasonEventBlock.table_schema()
    assert len(schema) > 0
    assert any(s.name == "event_name" for s in schema)
    assert any(s.name == "start_date" for s in schema)


def test_stat_highlight_table_schema():
    """Test StatHighlight table_schema."""
    from aiss.models.shows.sports_model import StatHighlight

    schema = StatHighlight.table_schema()
    assert len(schema) > 0
    assert any(s.name == "metric" for s in schema)
    assert any(s.name == "leader" for s in schema)


def test_sports_show_with_seasonal_events():
    """Test show with seasonal events renders correctly."""
    from aiss.models.shows.sports_model import SeasonEventBlock

    show = SportsShowInfo(
        title="Events Show",
        show_summary="A show with events",
        seasonal_events=[
            SeasonEventBlock(
                event_name="Super Bowl",
                start_date="2020-02-02",
                end_date="2020-02-02",
                coverage_plan="Full coverage",
                rights_holder="CBS",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Seasonal Events" in section_titles


def test_sports_show_with_stat_highlights():
    """Test show with stat highlights renders correctly."""
    from aiss.models.shows.sports_model import StatHighlight

    show = SportsShowInfo(
        title="Stats Show",
        show_summary="A show with stats",
        stat_highlights=[
            StatHighlight(
                metric="Points Per Game",
                leader="LeBron James",
                timeframe="Season",
                context="Leading scorer",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]
    assert "Stat Highlights" in section_titles


def test_sports_show_table_sections_with_all_optional_fields():
    """Test _table_sections includes all optional sections when present."""
    from aiss.models.shows.sports_model import SeasonEventBlock, StatHighlight

    show = SportsShowInfo(
        title="Complete Show",
        show_summary="A show with all sections",
        coverage_segments=[
            CoverageSegment(
                name="Opening",
                sport="All",
                focus="News",
                schedule_slot="First",
                hosts=["Host"],
                duration_minutes=10,
            )
        ],
        team_features=[
            TeamAthleteFeature(
                subject="Team A",
                league="NFL",
                feature_type="Season Preview",
                storyline="Championship contenders",
                stats_highlight="10-0 record",
            )
        ],
        seasonal_events=[
            SeasonEventBlock(
                event_name="Playoffs",
                start_date="2020-01-01",
                end_date="2020-02-01",
                coverage_plan="Daily",
                rights_holder="ESPN",
            )
        ],
        stat_highlights=[
            StatHighlight(
                metric="Home Runs",
                leader="Babe Ruth",
                timeframe="All-Time",
                context="Record holder",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Sports Review",
                reviewer="Critic",
                score=9.0,
                summary="Excellent",
                quote="Best sports show",
                publication_date="2020-01-01",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 18-49",
                average_viewers=5000000,
                share=5.0,
                engagement_notes="High ratings",
            )
        ],
    )

    sections = show._table_sections()
    section_titles = [title for title, _, _ in sections]

    assert "Coverage Segments" in section_titles
    assert "Team/Athlete Features" in section_titles
    assert "Seasonal Events" in section_titles
    assert "Stat Highlights" in section_titles
    assert "Critical Reception" in section_titles
    assert "Audience Metrics" in section_titles
