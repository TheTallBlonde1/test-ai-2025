"""Tests for HorrorSurvivalGameInfo model."""

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
from aiss.models.games.horror_survival_model import (
    HorrorSurvivalGameInfo,
    ScenarioStructureProfile,
    SurvivalResourceProfile,
    ThreatProfile,
)


@pytest.fixture
def horror_survival_game_full():
    """Create a fully populated horror survival game instance for testing."""
    return HorrorSurvivalGameInfo(
        title="Shadows of the Abyss",
        game_summary="Psychological horror with survival resource management",
        core_loop="Scavenge, survive, escape",
        horror_subgenre="psychological horror with cosmic elements",
        threat_design_philosophy="Unpredictable AI that learns player patterns",
        tension_delivery="Dynamic tension system with scripted scares",
        vulnerability_model="Limited resources force difficult choices",
        monetisation_model="Premium with story DLC expansions",
        live_update_strategy="Quarterly content drops with new scenarios",
        release_year=2024,
        average_session_minutes=90.0,
        developers=[
            StudioProfile(
                name="Dread Interactive",
                role="lead developer",
                headquarters="Stockholm, Sweden",
                team_size=85,
                notable_credits=["Night Terrors", "The Descent"],
                technology_stack=["Unity", "Custom AI System"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Fear Publishing",
                role="publisher",
                headquarters="London, UK",
                team_size=40,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - Steam",
                release_date="2024-10-31",
                edition="Standard",
                resolution_target="1440p",
                frame_rate_target="60 FPS",
                platform_features=["HDR", "3D Audio"],
            )
        ],
        threats=[
            ThreatProfile(
                name="The Stalker",
                behaviour="Adaptive AI that tracks player movement patterns",
                escalation="Becomes more aggressive as player progresses",
                counterplay="Stealth and distraction mechanics",
            ),
            ThreatProfile(
                name="Void Entities",
                behaviour="Random spawns in darkness",
                escalation="Increase in number and speed over time",
                counterplay="Light sources and environmental traps",
            ),
        ],
        survival_resources=[
            SurvivalResourceProfile(
                resource_name="Battery Charges",
                scarcity_model="Very limited, scattered across environment",
                acquisition_method="Exploration and puzzle solving",
                usage_pressure="Required for flashlight and essential tools",
            ),
            SurvivalResourceProfile(
                resource_name="Medical Supplies",
                scarcity_model="Rare, hidden in dangerous areas",
                acquisition_method="Risk/reward exploration",
                usage_pressure="Health doesn't regenerate naturally",
            ),
        ],
        scenarios=[
            ScenarioStructureProfile(
                scenario_name="The Abandoned Facility",
                objective="Find the keycard and escape before dawn",
                tension_curve="Slow build with explosive finale",
                coop_support="1-2 players",
            )
        ],
        mechanics=[
            GameplayMechanicHighlight(
                mechanic="Sanity System",
                category="survival",
                description="Witnessing horrors affects perception and controls",
                player_impact="Creates psychological pressure beyond physical threats",
                mastery_curve="Complex - managing sanity is key to success",
            )
        ],
        narrative_beats=[
            NarrativeBeatInfo(
                beat_name="The First Encounter",
                synopsis="Player's first direct confrontation with the unknown",
                branching_choice="Fight or hide",
                emotional_tone="Terror and helplessness",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Survival Skills",
                track_type="Experience",
                unlocks=["Crafting recipes", "Movement techniques"],
                pacing="Slow but meaningful",
                hard_cap=25,
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Halloween Special: The Manor",
                cadence="Annual",
                focus="Time-limited horror scenario",
                rewards=["Exclusive cosmetics", "Achievement"],
                retention_goal="Seasonal player return",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Jumpscare Warning",
                status="Optional",
                notes="Visual indicators before scripted scares",
                platform_support=["All platforms"],
            )
        ],
        audio_design=[
            AudioDesignCue(
                cue_name="Heartbeat Tension",
                composer="Alex Nightmare",
                style="Atmospheric drones with rhythmic elements",
                gameplay_trigger="Proximity to threats",
            )
        ],
    )


def test_horror_survival_basic_creation():
    """Test basic horror survival game creation."""
    game = HorrorSurvivalGameInfo(title="Test Horror")
    assert game.title == "Test Horror"
    assert game.model_name == "HorrorSurvivalGameInfo"


def test_horror_survival_fact_pairs(horror_survival_game_full):
    """Test fact pairs generation."""
    facts = dict(horror_survival_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "90" in facts["Session Length"]
    assert "psychological" in facts["Subgenre"].lower()


def test_horror_survival_extra_panels(horror_survival_game_full):
    """Test extra panels generation."""
    panels = horror_survival_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Fear Design" in panel_titles
    assert "Survival Plan" in panel_titles


def test_horror_survival_render_includes_content(horror_survival_game_full, console):
    """Test render includes all expected content."""
    horror_survival_game_full.render(console)
    text = console.export_text()
    assert "Shadows of the Abyss" in text
    assert "Psychological horror" in text or "psychological horror" in text


def test_horror_survival_instruction_helpers():
    """Test instruction helper methods."""
    combined = HorrorSurvivalGameInfo.get_instructions(["Emphasize atmosphere"])
    assert isinstance(combined, str)

    prompt = HorrorSurvivalGameInfo.get_user_prompt("Test Horror")
    assert "Test Horror" in prompt

    formatted = HorrorSurvivalGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_horror_survival_threats(horror_survival_game_full):
    """Test threat profiles."""
    assert len(horror_survival_game_full.threats) == 2
    assert horror_survival_game_full.threats[0].name == "The Stalker"
    assert "Adaptive AI" in horror_survival_game_full.threats[0].behaviour


def test_horror_survival_resources(horror_survival_game_full):
    """Test survival resources."""
    assert len(horror_survival_game_full.survival_resources) == 2
    assert horror_survival_game_full.survival_resources[0].resource_name == "Battery Charges"


def test_horror_survival_scenarios(horror_survival_game_full):
    """Test scenario structure."""
    assert len(horror_survival_game_full.scenarios) == 1
    scenario = horror_survival_game_full.scenarios[0]
    assert scenario.scenario_name == "The Abandoned Facility"
    assert "1-2 players" in scenario.coop_support


def test_horror_survival_table_sections(horror_survival_game_full):
    """Test table sections generation."""
    sections = horror_survival_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Threats" in section_titles
    assert "Resources" in section_titles
    assert "Scenarios" in section_titles


def test_horror_survival_empty_optional_fields(console):
    """Test game with minimal data."""
    game = HorrorSurvivalGameInfo(
        title="Minimal Horror",
        game_summary="Basic horror",
        core_loop="Run and hide",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Session Length"] == "-"


def test_horror_survival_roundtrip():
    """Test serialization roundtrip."""
    original = HorrorSurvivalGameInfo(
        title="Roundtrip Horror",
        game_summary="Testing serialization",
        core_loop="survive -> escape",
        release_year=2024,
        horror_subgenre="survival horror",
        average_session_minutes=60.0,
    )
    data = original.to_dict()
    restored = HorrorSurvivalGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.horror_subgenre == original.horror_subgenre
    assert restored.average_session_minutes == original.average_session_minutes


def test_threat_profile_table_schema():
    """Test ThreatProfile has table schema."""
    schema = ThreatProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Threat" in headers


def test_survival_resource_profile_table_schema():
    """Test SurvivalResourceProfile has table schema."""
    schema = SurvivalResourceProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Resource" in headers


def test_scenario_structure_profile_table_schema():
    """Test ScenarioStructureProfile has table schema."""
    schema = ScenarioStructureProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Scenario" in headers
