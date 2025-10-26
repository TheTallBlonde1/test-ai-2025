"""Tests for ComedyShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.comedy_model import (
    ComedyCharacterProfile,
    ComedyEpisodeBeat,
    ComedyShowInfo,
    RunningGagInfo,
)


@pytest.fixture
def comedy_show_full():
    """Create a fully populated comedy show instance for testing."""
    return ComedyShowInfo(
        title="The Office Chronicles",
        premise="A documentary crew films the daily chaos of a paper company",
        show_summary="Mockumentary following the absurd lives of office workers dealing with an eccentric boss.",
        format_type="Mockumentary sitcom",
        humour_styles=["Cringe comedy", "Satire", "Character-driven"],
        tone="Lighthearted with occasional heartfelt moments",
        primary_setting="Scranton, PA office",
        season_count=9,
        episode_count=201,
        episode_length_minutes=22,
        release_start_year=2005,
        release_end_year=2013,
        age_rating="TV-14",
        live_audience=False,
        improv_elements="Significant improvisation in interviews",
        characters=[
            ComedyCharacterProfile(
                name="Michael Scott",
                actor="Steve Carell",
                comedic_role="Oblivious boss",
                signature_gag="That's what she said",
                relationships=["Dwight (protégé)", "Jim (frenemy)"],
                catchphrases=["That's what she said"],
                spotlight_episodes=["S02E01 - The Dundies", "S07E22 - Goodbye Michael"],
            ),
            ComedyCharacterProfile(
                name="Jim Halpert",
                actor="John Krasinski",
                comedic_role="Prankster / straight man",
                signature_gag="Pranks on Dwight",
                relationships=["Pam (love interest)", "Dwight (nemesis)"],
                catchphrases=[],
                spotlight_episodes=["S03E23 - The Job"],
            ),
        ],
        episode_beats=[
            ComedyEpisodeBeat(
                episode_title="The Dundies",
                season=2,
                comedic_engine="Award ceremony gone wrong",
                core_conflict="Michael's inappropriate awards",
                guest_stars=[],
                resolution="Pam drunk, Jim confession foreshadowed",
            ),
            ComedyEpisodeBeat(
                episode_title="Dinner Party",
                season=4,
                comedic_engine="Cringe dinner with boss",
                core_conflict="Michael and Jan's toxic relationship on display",
                guest_stars=["Jan Levinson"],
                resolution="Everyone leaves traumatized",
            ),
        ],
        running_gags=[
            RunningGagInfo(
                name="That's what she said",
                description="Michael's inappropriate joke",
                first_appearance="S01E01",
                frequency="Multiple times per season",
                notable_variations=["Christmas special variation", "Oscar's delivery"],
            ),
            RunningGagInfo(
                name="Jim's pranks on Dwight",
                description="Elaborate pranks targeting Dwight",
                first_appearance="S01E01",
                frequency="Almost every episode",
                notable_variations=["Jell-O stapler", "Asian Jim", "Fax from future Dwight"],
            ),
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Entertainment Weekly",
                reviewer="Ken Tucker",
                score=9.0,
                summary="Brilliant character comedy",
                quote="The Office is the best comedy on television",
                publication_date="2006-09-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 18-49",
                average_viewers=8000000,
                share=4.5,
                engagement_notes="Peak viewership in seasons 3-5",
            )
        ],
        writers_room=["Greg Daniels", "Mindy Kaling", "B.J. Novak"],
        directors=["Greg Daniels", "Paul Feig"],
        production_companies=[
            ProductionCompanyInfo(
                name="Deedle-Dee Productions",
                founded_year=2004,
                start_year=2005,
                end_year=2013,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="NBC",
                country="USA",
                start_year=2005,
                end_year=2013,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="NBCUniversal",
                territory="Worldwide",
                release_type="Broadcast + Streaming",
                start_year=2005,
                end_year=0,
                revenue=500000000,
            )
        ],
    )


def test_comedy_basic_creation():
    """Test basic show creation."""
    show = ComedyShowInfo(title="Test Comedy")
    assert show.title == "Test Comedy"
    assert show.model_name == "ComedyShowInfo"


def test_comedy_fact_pairs(comedy_show_full):
    """Test fact pairs generation."""
    facts = dict(comedy_show_full._fact_pairs())
    assert facts["Format"] == "Mockumentary sitcom"
    assert "Lighthearted" in facts["Tone"]
    assert facts["Run"] == "2005 - 2013"


def test_comedy_table_sections(comedy_show_full):
    """Test table sections generation."""
    sections = comedy_show_full._table_sections()
    assert sections
    titles = {title for title, _, _ in sections}
    assert "Characters" in titles
    assert "Running Gags" in titles
    assert "Episode Beats" in titles


def test_comedy_render_includes_content(comedy_show_full, console):
    """Test render includes all expected content."""
    comedy_show_full.render(console)
    text = console.export_text()
    assert "The Office Chronicles" in text
    assert "Mockumentary" in text or "mockumentary" in text


def test_comedy_instruction_helpers():
    """Test instruction helper methods."""
    combined = ComedyShowInfo.get_instructions(["Focus on timing"])
    assert "Additional context" in combined
    assert "Focus on timing" in combined

    prompt = ComedyShowInfo.get_user_prompt("Test Comedy")
    assert "Test Comedy" in prompt

    formatted = ComedyShowInfo.json_format_instructions()
    assert "JSON" in formatted


def test_comedy_characters(comedy_show_full):
    """Test characters data."""
    assert len(comedy_show_full.characters) == 2
    assert comedy_show_full.characters[0].name == "Michael Scott"
    assert "Oblivious boss" in comedy_show_full.characters[0].comedic_role


def test_comedy_episode_beats(comedy_show_full):
    """Test episode beats data."""
    assert len(comedy_show_full.episode_beats) == 2
    assert comedy_show_full.episode_beats[0].episode_title == "The Dundies"
    assert comedy_show_full.episode_beats[0].season == 2


def test_comedy_running_gags(comedy_show_full):
    """Test running gags data."""
    assert len(comedy_show_full.running_gags) == 2
    assert comedy_show_full.running_gags[0].name == "That's what she said"
    assert "S01E01" in comedy_show_full.running_gags[0].first_appearance


def test_comedy_live_audience_field(comedy_show_full):
    """Test live audience field."""
    assert comedy_show_full.live_audience is False


def test_comedy_improv_elements(comedy_show_full):
    """Test improv elements field."""
    assert "improvisation" in comedy_show_full.improv_elements


def test_comedy_empty_optional_fields(console):
    """Test show with minimal data."""
    show = ComedyShowInfo(
        title="Minimal Comedy",
        premise="Basic premise",
    )
    show.render(console)
    facts = dict(show._fact_pairs())
    assert isinstance(facts, dict)


def test_comedy_roundtrip():
    """Test serialization roundtrip."""
    original = ComedyShowInfo(
        title="Roundtrip Comedy",
        premise="Testing serialization",
        season_count=3,
        episode_count=30,
        format_type="Sitcom",
        tone="Funny",
    )
    data = original.to_dict()
    restored = ComedyShowInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.format_type == original.format_type
    assert restored.tone == original.tone


def test_comedy_character_profile_table_schema():
    """Test ComedyCharacterProfile has table schema."""
    schema = ComedyCharacterProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Character" in headers


def test_comedy_episode_beat_table_schema():
    """Test ComedyEpisodeBeat has table schema."""
    schema = ComedyEpisodeBeat.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Episode" in headers


def test_running_gag_info_table_schema():
    """Test RunningGagInfo has table schema."""
    schema = RunningGagInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Running Gag" in headers
