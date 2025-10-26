"""Tests for ActionAdventureGameInfo model."""

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
    TechnicalBenchmarkInfo,
)
from aiss.models.games.action_adventure_model import ActionAdventureGameInfo


@pytest.fixture
def action_adventure_game_full():
    """Create a fully populated action adventure game instance for testing."""
    return ActionAdventureGameInfo(
        title="Legends of the Forgotten Realm",
        game_summary="Epic fantasy adventure across mystical lands",
        core_loop="Explore, combat, solve puzzles, upgrade",
        world_setting="Post-apocalyptic fantasy world with ancient technology",
        hero_profile="Skilled warrior seeking to restore balance to the realm",
        camera_perspective="third-person",
        release_year=2024,
        average_completion_hours=35.0,
        completionist_hours=85.0,
        exploration_focus="open world with hub regions",
        combat_identity=["Combo-based melee", "Tactical ranged", "Elemental magic"],
        puzzle_integrations=["Environmental puzzles", "Ancient mechanisms", "Light manipulation"],
        difficulty_modes=["Story", "Normal", "Hard", "Master"],
        monetisation_model="Premium with optional cosmetic DLC",
        endgame_structure="New Game Plus with additional challenges and lore",
        player_agency_features=["Branching dialogue", "Multiple endings", "Skill tree customization"],
        platforms=["PC", "PlayStation 5", "Xbox Series X"],
        developers=[
            StudioProfile(
                name="Epic Quest Studios",
                role="lead developer",
                headquarters="Montreal, Canada",
                team_size=200,
                notable_credits=["Quest Saga", "Ancient Chronicles"],
                technology_stack=["Unreal Engine 5", "Custom Animation System"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Global Games Publishing",
                role="publisher",
                headquarters="Los Angeles, USA",
                team_size=75,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - Steam",
                release_date="2024-09-20",
                edition="Deluxe",
                resolution_target="4K",
                frame_rate_target="60 FPS",
                platform_features=["Ray Tracing", "Ultra HD Textures"],
            )
        ],
        signature_mechanics=[
            GameplayMechanicHighlight(
                mechanic="Grappling Hook Traversal",
                category="traversal",
                description="Dynamic grappling system for vertical exploration",
                player_impact="Enables creative navigation and combat opportunities",
                mastery_curve="Medium - skill-based with combo potential",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Hero Level",
                track_type="XP",
                unlocks=["Skills", "Equipment Slots", "Abilities"],
                pacing="Balanced curve with milestone rewards",
                hard_cap=50,
            )
        ],
        narrative_beats=[
            NarrativeBeatInfo(
                beat_name="The Awakening",
                synopsis="Hero discovers ancient powers",
                branching_choice="Accept power or seek alternative",
                emotional_tone="Mysterious and awe-inspiring",
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="The Lost Expedition DLC",
                cadence="6 months post-launch",
                focus="New region with story expansion",
                rewards=["Legendary weapons", "Unique armor sets"],
                retention_goal="Bring back lapsed players",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Subtitle Customization",
                status="Implemented",
                notes="Size, color, and background opacity options",
                platform_support=["All platforms"],
            )
        ],
        technical_benchmarks=[
            TechnicalBenchmarkInfo(
                scenario="Dense forest combat sequence",
                hardware_profile="RTX 4080 / Ryzen 9 5900X",
                target_metrics="4K @ 60 FPS",
                measured_metrics="4K @ 63 FPS average",
                optimisation_notes="DLSS Balanced mode with ray tracing",
            )
        ],
        audio_design=[
            AudioDesignCue(
                cue_name="Forgotten Realm Theme",
                composer="Jane Smith",
                style="Orchestral with ethnic influences",
                gameplay_trigger="Exploration and discovery moments",
            )
        ],
    )


def test_action_adventure_basic_creation():
    """Test basic action adventure game creation."""
    game = ActionAdventureGameInfo(title="Test Adventure")
    assert game.title == "Test Adventure"
    assert game.model_name == "ActionAdventureGameInfo"


def test_action_adventure_fact_pairs(action_adventure_game_full):
    """Test fact pairs generation."""
    facts = dict(action_adventure_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "35" in facts["Completion (hrs)"]
    assert "85" in facts["Completionist"]


def test_action_adventure_extra_panels(action_adventure_game_full):
    """Test extra panels generation."""
    panels = action_adventure_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "World & Protagonist" in panel_titles
    assert "Endgame Loop" in panel_titles


def test_action_adventure_render_includes_content(action_adventure_game_full, console):
    """Test render includes all expected content."""
    action_adventure_game_full.render(console)
    text = console.export_text()
    assert "Legends of the Forgotten Realm" in text
    assert "Epic fantasy adventure" in text


def test_action_adventure_instruction_helpers():
    """Test instruction helper methods."""
    combined = ActionAdventureGameInfo.get_instructions(["Focus on narrative depth"])
    assert "Additional context" in combined or "Focus on narrative depth" in combined

    prompt = ActionAdventureGameInfo.get_user_prompt("Test Adventure")
    assert "Test Adventure" in prompt
    assert "action-adventure" in prompt.lower() or "adventure" in prompt.lower()

    formatted = ActionAdventureGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_action_adventure_combat_identity(action_adventure_game_full):
    """Test combat identity list."""
    assert len(action_adventure_game_full.combat_identity) == 3
    assert "Combo-based melee" in action_adventure_game_full.combat_identity


def test_action_adventure_puzzle_integrations(action_adventure_game_full):
    """Test puzzle integrations."""
    assert len(action_adventure_game_full.puzzle_integrations) == 3
    assert "Environmental puzzles" in action_adventure_game_full.puzzle_integrations


def test_action_adventure_difficulty_modes(action_adventure_game_full):
    """Test difficulty modes."""
    assert len(action_adventure_game_full.difficulty_modes) == 4
    assert "Story" in action_adventure_game_full.difficulty_modes
    assert "Master" in action_adventure_game_full.difficulty_modes


def test_action_adventure_table_sections(action_adventure_game_full):
    """Test table sections generation."""
    sections = action_adventure_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Publishers" in section_titles
    assert "Signature Mechanics" in section_titles
    assert "Narrative Beats" in section_titles


def test_action_adventure_empty_optional_fields(console):
    """Test game with minimal data."""
    game = ActionAdventureGameInfo(
        title="Minimal Adventure",
        game_summary="Basic adventure game",
        core_loop="Explore and fight",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Completion (hrs)"] == "-"


def test_action_adventure_roundtrip():
    """Test serialization roundtrip."""
    original = ActionAdventureGameInfo(
        title="Roundtrip Adventure",
        game_summary="Testing serialization",
        core_loop="test -> verify -> iterate",
        release_year=2024,
        average_completion_hours=25.5,
        camera_perspective="third-person",
    )
    data = original.to_dict()
    restored = ActionAdventureGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.average_completion_hours == original.average_completion_hours
    assert restored.camera_perspective == original.camera_perspective


def test_action_adventure_player_agency(action_adventure_game_full):
    """Test player agency features."""
    assert len(action_adventure_game_full.player_agency_features) == 3
    assert "Multiple endings" in action_adventure_game_full.player_agency_features


def test_action_adventure_world_setting(action_adventure_game_full):
    """Test world setting is accessible."""
    assert action_adventure_game_full.world_setting
    assert "Post-apocalyptic fantasy" in action_adventure_game_full.world_setting
