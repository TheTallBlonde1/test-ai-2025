"""Tests for ActionAdventureFantasyShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.action_fantasy_model import (
    ActionAdventureFantasyShowInfo,
    ArtifactInfo,
    HeroProfile,
    QuestArc,
    WorldLocation,
)


@pytest.fixture
def action_fantasy_show_full():
    """Create a fully populated action/fantasy show instance for testing."""
    return ActionAdventureFantasyShowInfo(
        title="Chronicles of the Nexus",
        show_summary="A team of heroes must prevent dimensional collapse by recovering ancient artifacts.",
        tagline="Between worlds lies destiny.",
        world_setting="Multiverse spanning fantasy and sci-fi dimensions",
        genre_mix=["Epic Fantasy", "Science Fiction", "Adventure"],
        tone="Epic and dramatic with lighter moments",
        core_themes=["Destiny", "Sacrifice", "Unity"],
        season_count=5,
        episode_count=60,
        average_runtime_minutes=50,
        age_rating="TV-14",
        visual_style="Cinematic with practical sets and extensive VFX",
        effects_approach="Hybrid practical and CGI",
        release_start_year=2018,
        release_end_year=2023,
        creators=["Jane Creator"],
        showrunners=["John Showrunner"],
        stunt_coordinators=["Stunt Master"],
        heroes=[
            HeroProfile(
                name="Kira Dimensional",
                actor="Lead Actress",
                role="Protagonist",
                abilities=["Dimensional travel", "Energy manipulation"],
                affiliations=["Nexus Guild"],
                notable_items=["Nexus Crystal"],
                arc_summary="Learns to control her powers and unite the realms",
            ),
            HeroProfile(
                name="Marcus Steel",
                actor="Supporting Actor",
                role="Mentor",
                abilities=["Master swordsman", "Ancient knowledge"],
                affiliations=["Nexus Guild", "Old Guard"],
                notable_items=["Eternal Blade"],
                arc_summary="Guides Kira while confronting his past",
            ),
        ],
        quest_arcs=[
            QuestArc(
                quest_name="The Crystal Hunt",
                season=1,
                objective="Recover the Nexus Crystals before they fall into enemy hands",
                antagonists=["The Shadow Collective"],
                allies=["Nexus Guild", "Dimension Keepers"],
                stakes="Dimensional collapse if crystals are united by evil",
                resolution="Crystals secured but mentor sacrificed",
            ),
            QuestArc(
                quest_name="The Dark Realm",
                season=3,
                objective="Enter the Dark Realm to rescue prisoners",
                antagonists=["Dark Lord Vex", "Shadow Warriors"],
                allies=["Underground Resistance"],
                stakes="Loss of key allies and strategic positions",
                resolution="Successful rescue but Dark Lord escapes",
            ),
        ],
        world_locations=[
            WorldLocation(
                name="Nexus City",
                locale_type="Hub City",
                description="Central hub connecting all dimensions",
                controlling_faction="Nexus Guild",
                first_appearance="S01E01",
                narrative_significance="Home base and center of dimensional travel",
            ),
            WorldLocation(
                name="Crystal Mountains",
                locale_type="Natural Wonder",
                description="Mountain range where crystals are found",
                controlling_faction="Neutral - protected by ancient magic",
                first_appearance="S01E03",
                narrative_significance="Source of the Nexus Crystals",
            ),
        ],
        artifacts=[
            ArtifactInfo(
                name="Nexus Crystal",
                classification="Power Source",
                powers=["Dimensional travel", "Energy amplification"],
                wielders=["Kira Dimensional"],
                origin="Created by the Ancients to stabilize dimensions",
            ),
            ArtifactInfo(
                name="Eternal Blade",
                classification="Weapon",
                powers=["Cuts through dimensional barriers", "Unbreakable"],
                wielders=["Marcus Steel", "Previous Guardians"],
                origin="Forged in the First War of the Realms",
            ),
        ],
        critical_reception=[
            CriticalResponse(
                outlet="TV Critic Weekly",
                reviewer="Jane Reviewer",
                score=8.5,
                summary="Ambitious world-building with stunning visuals",
                quote="Chronicles sets a new bar for fantasy television",
                publication_date="2018-10-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 18-49",
                average_viewers=5000000,
                share=3.5,
                engagement_notes="Strong streaming performance",
            )
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Epic Productions",
                founded_year=2005,
                start_year=2017,
                end_year=2023,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="Fantasy Network",
                country="USA",
                start_year=2018,
                end_year=2023,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Global Streaming",
                territory="Worldwide",
                release_type="Streaming",
                start_year=2018,
                end_year=0,
                revenue=200000000,
            )
        ],
    )


def test_action_fantasy_basic_creation():
    """Test basic show creation."""
    show = ActionAdventureFantasyShowInfo(title="Test Show")
    assert show.title == "Test Show"
    assert show.model_name == "ActionAdventureFantasyShowInfo"


def test_action_fantasy_fact_pairs(action_fantasy_show_full):
    """Test fact pairs generation."""
    facts = dict(action_fantasy_show_full._fact_pairs())
    assert "Multiverse" in facts["World"]
    assert "Epic and dramatic" in facts["Tone"]
    assert "2018 - 2023" == facts["Run"]


def test_action_fantasy_table_sections(action_fantasy_show_full):
    """Test table sections generation."""
    sections = action_fantasy_show_full._table_sections()
    assert sections
    titles = {title for title, _, _ in sections}
    assert "Heroes" in titles
    assert "Quest Arcs" in titles
    assert "World Locations" in titles
    assert "Artifacts" in titles


def test_action_fantasy_render_includes_content(action_fantasy_show_full, console):
    """Test render includes all expected content."""
    action_fantasy_show_full.render(console)
    text = console.export_text()
    assert "Chronicles of the Nexus" in text
    assert "Between worlds lies destiny." in text


def test_action_fantasy_instruction_helpers():
    """Test instruction helper methods."""
    combined = ActionAdventureFantasyShowInfo.get_instructions(["Focus on world-building"])
    assert "Additional context" in combined
    assert "Focus on world-building" in combined

    prompt = ActionAdventureFantasyShowInfo.get_user_prompt("Test Show")
    assert "Test Show" in prompt

    formatted = ActionAdventureFantasyShowInfo.json_format_instructions()
    assert "JSON" in formatted


def test_action_fantasy_heroes(action_fantasy_show_full):
    """Test heroes data."""
    assert len(action_fantasy_show_full.heroes) == 2
    assert action_fantasy_show_full.heroes[0].name == "Kira Dimensional"
    assert "Dimensional travel" in action_fantasy_show_full.heroes[0].abilities


def test_action_fantasy_quest_arcs(action_fantasy_show_full):
    """Test quest arcs data."""
    assert len(action_fantasy_show_full.quest_arcs) == 2
    assert action_fantasy_show_full.quest_arcs[0].quest_name == "The Crystal Hunt"
    assert action_fantasy_show_full.quest_arcs[0].season == 1


def test_action_fantasy_world_locations(action_fantasy_show_full):
    """Test world locations data."""
    assert len(action_fantasy_show_full.world_locations) == 2
    assert action_fantasy_show_full.world_locations[0].name == "Nexus City"
    assert "Hub City" in action_fantasy_show_full.world_locations[0].locale_type


def test_action_fantasy_artifacts(action_fantasy_show_full):
    """Test artifacts data."""
    assert len(action_fantasy_show_full.artifacts) == 2
    assert action_fantasy_show_full.artifacts[0].name == "Nexus Crystal"
    assert "Power Source" in action_fantasy_show_full.artifacts[0].classification


def test_action_fantasy_empty_optional_fields(console):
    """Test show with minimal data."""
    show = ActionAdventureFantasyShowInfo(
        title="Minimal Show",
        show_summary="Basic show",
    )
    show.render(console)
    facts = dict(show._fact_pairs())
    assert isinstance(facts, dict)


def test_action_fantasy_roundtrip():
    """Test serialization roundtrip."""
    original = ActionAdventureFantasyShowInfo(
        title="Roundtrip Show",
        show_summary="Testing serialization",
        season_count=3,
        episode_count=30,
        world_setting="Test world",
        tone="Test tone",
    )
    data = original.to_dict()
    restored = ActionAdventureFantasyShowInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.world_setting == original.world_setting
    assert restored.tone == original.tone


def test_hero_profile_table_schema():
    """Test HeroProfile has table schema."""
    schema = HeroProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Hero" in headers


def test_quest_arc_table_schema():
    """Test QuestArc has table schema."""
    schema = QuestArc.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Quest" in headers


def test_world_location_table_schema():
    """Test WorldLocation has table schema."""
    schema = WorldLocation.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Location" in headers


def test_artifact_info_table_schema():
    """Test ArtifactInfo has table schema."""
    schema = ArtifactInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Artifact" in headers
