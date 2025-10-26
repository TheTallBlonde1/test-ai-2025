"""Tests for RolePlayingGameInfo model."""

import pytest

from aiss.models.games._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    NarrativeBeatInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
)
from aiss.models.games.role_playing_model import (
    CharacterClassProfile,
    CompanionProfile,
    FactionProfile,
    RolePlayingGameInfo,
)


@pytest.fixture
def role_playing_game_full():
    """Create a fully populated role-playing game instance for testing."""
    return RolePlayingGameInfo(
        title="Chronicles of Eternity",
        game_summary="Deep RPG with branching narrative and rich character development",
        core_loop="Explore, quest, combat, upgrade, make choices",
        world_setting="High fantasy realm with political intrigue",
        timeline_context="Post-war reconstruction era with lingering tensions",
        protagonist_identity="Fully customizable hero with flexible class system",
        release_year=2024,
        estimated_campaign_hours=80.0,
        build_flexibility="Classless system with skill-based progression",
        choice_consequence_map="Branching storylines with meaningful faction impacts",
        monetisation_model="Premium with narrative expansion DLCs",
        post_launch_story_plan="Quarterly story chapters with new companions",
        developers=[
            StudioProfile(
                name="Epic RPG Studios",
                role="lead developer",
                headquarters="Warsaw, Poland",
                team_size=250,
                notable_credits=["Fantasy Chronicles", "Legends of the North"],
                technology_stack=["REDengine", "Custom Dialogue System"],
            )
        ],
        publishers=[
            StudioProfile(
                name="RPG Publishing House",
                role="publisher",
                headquarters="Paris, France",
                team_size=90,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - GOG",
                release_date="2024-11-12",
                edition="Collector's",
                resolution_target="4K",
                frame_rate_target="60 FPS",
                platform_features=["DRM-Free", "Cloud Saves"],
            )
        ],
        factions=[
            FactionProfile(
                faction_name="The Silver Order",
                ideology="Traditional values and magical preservation",
                territory="Northern Highlands",
                relationship_state="Neutral with opportunity for alliance",
                rewards=["Enchanted weapons", "Silver armor set"],
            ),
            FactionProfile(
                faction_name="The Free Traders",
                ideology="Commercial freedom and innovation",
                territory="Coastal cities",
                relationship_state="Friendly",
                rewards=["Rare materials", "Trading discounts"],
            ),
        ],
        character_classes=[
            CharacterClassProfile(
                class_name="Battle Mage",
                combat_role="Hybrid DPS with crowd control",
                resource_model="Mana and stamina dual system",
                signature_abilities=["Arcane Blade", "Elemental Burst", "Shield Ward"],
                complexity_rating="Advanced",
            ),
            CharacterClassProfile(
                class_name="Shadow Walker",
                combat_role="Stealth DPS with mobility",
                resource_model="Energy regeneration",
                signature_abilities=["Backstab", "Shadow Step", "Smoke Bomb"],
                complexity_rating="Intermediate",
            ),
        ],
        companions=[
            CompanionProfile(
                name="Aria Stormwind",
                origin="Silver Order exile",
                combat_synergy="Ranged support with healing",
                loyalty_arc="Redemption quest involving her order",
                romanceable=True,
            ),
            CompanionProfile(
                name="Graven the Bold",
                origin="Free Traders champion",
                combat_synergy="Tank with crowd control",
                loyalty_arc="Family legacy and honor",
                romanceable=False,
            ),
        ],
        systems=[
            GameplayMechanicHighlight(
                mechanic="Reputation System",
                category="social",
                description="Dynamic faction relationships based on choices",
                player_impact="Unlocks unique quests and endings",
                mastery_curve="Complex with cascading consequences",
            )
        ],
        narrative_beats=[
            NarrativeBeatInfo(
                beat_name="The Council's Decision",
                synopsis="Player mediates critical faction negotiation",
                branching_choice="Support tradition or innovation",
                emotional_tone="Tense political drama",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Skill Mastery",
                track_type="Skill points",
                unlocks=["Passive bonuses", "Ultimate abilities"],
                pacing="Player-driven specialization",
                hard_cap=100,
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Winter's Tale DLC",
                cadence="3 months post-launch",
                focus="New story arc with companion",
                rewards=["Legendary gear", "Mount"],
                retention_goal="Story continuation",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Difficulty Sliders",
                status="Implemented",
                notes="Granular control over combat and puzzle difficulty",
                platform_support=["All platforms"],
            )
        ],
        audio_design=[
            AudioDesignCue(
                cue_name="Chronicles Main Theme",
                composer="Symphony Orchestra",
                style="Epic orchestral with folk instruments",
                gameplay_trigger="Main menu and pivotal story moments",
            )
        ],
    )


def test_role_playing_basic_creation():
    """Test basic role-playing game creation."""
    game = RolePlayingGameInfo(title="Test RPG")
    assert game.title == "Test RPG"
    assert game.model_name == "RolePlayingGameInfo"


def test_role_playing_fact_pairs(role_playing_game_full):
    """Test fact pairs generation."""
    facts = dict(role_playing_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "80" in facts["Campaign Hours"]
    assert "Classless" in facts["Build Flexibility"]


def test_role_playing_extra_panels(role_playing_game_full):
    """Test extra panels generation."""
    panels = role_playing_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Worldbuilding" in panel_titles
    assert "Player Fantasy" in panel_titles


def test_role_playing_render_includes_content(role_playing_game_full, console):
    """Test render includes all expected content."""
    role_playing_game_full.render(console)
    text = console.export_text()
    assert "Chronicles of Eternity" in text
    assert "Deep RPG" in text


def test_role_playing_instruction_helpers():
    """Test instruction helper methods."""
    combined = RolePlayingGameInfo.get_instructions(["Emphasize choice"])
    assert isinstance(combined, str)

    prompt = RolePlayingGameInfo.get_user_prompt("Test RPG")
    assert "Test RPG" in prompt
    assert "RPG" in prompt

    formatted = RolePlayingGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_role_playing_factions(role_playing_game_full):
    """Test faction profiles."""
    assert len(role_playing_game_full.factions) == 2
    assert role_playing_game_full.factions[0].faction_name == "The Silver Order"
    assert role_playing_game_full.factions[1].territory == "Coastal cities"


def test_role_playing_character_classes(role_playing_game_full):
    """Test character class profiles."""
    assert len(role_playing_game_full.character_classes) == 2
    assert role_playing_game_full.character_classes[0].class_name == "Battle Mage"
    assert "Arcane Blade" in role_playing_game_full.character_classes[0].signature_abilities


def test_role_playing_companions(role_playing_game_full):
    """Test companion profiles."""
    assert len(role_playing_game_full.companions) == 2
    assert role_playing_game_full.companions[0].name == "Aria Stormwind"
    assert role_playing_game_full.companions[0].romanceable is True
    assert role_playing_game_full.companions[1].romanceable is False


def test_role_playing_table_sections(role_playing_game_full):
    """Test table sections generation."""
    sections = role_playing_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Factions" in section_titles
    assert "Character Classes" in section_titles
    assert "Companions" in section_titles


def test_role_playing_empty_optional_fields(console):
    """Test game with minimal data."""
    game = RolePlayingGameInfo(
        title="Minimal RPG",
        game_summary="Basic RPG",
        core_loop="Quest and fight",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Campaign Hours"] == "-"


def test_role_playing_roundtrip():
    """Test serialization roundtrip."""
    original = RolePlayingGameInfo(
        title="Roundtrip RPG",
        game_summary="Testing serialization",
        core_loop="test -> verify",
        release_year=2024,
        estimated_campaign_hours=50.0,
        build_flexibility="Open",
    )
    data = original.to_dict()
    restored = RolePlayingGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.estimated_campaign_hours == original.estimated_campaign_hours
    assert restored.build_flexibility == original.build_flexibility


def test_character_class_profile_table_schema():
    """Test CharacterClassProfile has table schema."""
    schema = CharacterClassProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Class" in headers


def test_companion_profile_table_schema():
    """Test CompanionProfile has table schema."""
    schema = CompanionProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Companion" in headers


def test_faction_profile_table_schema():
    """Test FactionProfile has table schema."""
    schema = FactionProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Faction" in headers


def test_role_playing_choice_consequence_map(role_playing_game_full):
    """Test choice consequence mapping."""
    assert role_playing_game_full.choice_consequence_map
    assert "Branching" in role_playing_game_full.choice_consequence_map
