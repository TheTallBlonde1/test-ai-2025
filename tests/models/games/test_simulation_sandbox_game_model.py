"""Tests for SimulationSandboxGameInfo model."""

import pytest

from aiss.models.games._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    EconomyLoopInfo,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    NarrativeBeatInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
)
from aiss.models.games.simulation_sandbox_model import (
    CreatorToolProfile,
    SimulationSandboxGameInfo,
    SimulationSystemProfile,
)


@pytest.fixture
def simulation_sandbox_game_full():
    """Create a fully populated simulation sandbox game instance for testing."""
    return SimulationSandboxGameInfo(
        title="Universe Builder",
        game_summary="Deep simulation sandbox with player-driven creativity",
        core_loop="Create, simulate, share, iterate",
        simulation_scope="City-scale simulation with individual agent AI",
        player_authorship="Full creative control over world building and rules",
        tech_constraints="Limited to 10,000 active agents per instance",
        release_year=2024,
        average_session_minutes=120.0,
        sharing_infrastructure="Built-in workshop with rating and discovery",
        monetisation_model="Premium with cosmetic DLC packs",
        live_update_cadence="Monthly feature updates and tool additions",
        developers=[
            StudioProfile(
                name="Sandbox Innovations",
                role="lead developer",
                headquarters="San Diego, USA",
                team_size=150,
                notable_credits=["City Dreams", "Planet Craft"],
                technology_stack=["Custom Engine", "Agent-Based Simulation"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Creative Games Ltd",
                role="publisher",
                headquarters="Amsterdam, Netherlands",
                team_size=60,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - Steam",
                release_date="2024-05-20",
                edition="Early Access",
                resolution_target="4K",
                frame_rate_target="60 FPS",
                platform_features=["Steam Workshop", "Cloud Saves", "Modding API"],
            )
        ],
        simulation_systems=[
            SimulationSystemProfile(
                name="Economy Simulation",
                scope="Supply chains and market dynamics",
                fidelity="Agent-level economic decisions",
                player_influence="Set policies and resource availability",
                emergent_outcomes=["Market crashes", "Trade route emergence", "Resource shortages"],
            ),
            SimulationSystemProfile(
                name="Weather System",
                scope="Dynamic weather affecting gameplay",
                fidelity="Regional patterns with seasonal cycles",
                player_influence="Can trigger events or set climate",
                emergent_outcomes=["Natural disasters", "Agricultural impacts"],
            ),
        ],
        creator_tools=[
            CreatorToolProfile(
                tool_name="Terrain Editor",
                capabilities="Sculpt terrain with brush tools and height maps",
                access_level="Core loop",
                sharing_channel="Workshop integration",
                monetisation="Free tool, cosmetic brushes available",
            ),
            CreatorToolProfile(
                tool_name="Logic Engine",
                capabilities="Visual scripting for custom behaviors",
                access_level="Advanced",
                sharing_channel="Workshop with dependency management",
                monetisation="Free",
            ),
        ],
        mechanics=[
            GameplayMechanicHighlight(
                mechanic="Zone Planning",
                category="management",
                description="Designate zones for different purposes",
                player_impact="Shapes city growth and agent behavior",
                mastery_curve="Medium - requires understanding of systems",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Builder Level",
                track_type="XP",
                unlocks=["Tools", "Templates", "Advanced systems"],
                pacing="Achievement-based progression",
                hard_cap=50,
            )
        ],
        economy_loops=[
            EconomyLoopInfo(
                loop_name="Creation Economy",
                loop_type="core",
                inputs=["Time investment", "Creative vision"],
                outputs=["Shareable creations", "Community recognition"],
                monetisation_hook="Premium asset packs",
                retention_goal="Creator engagement and sharing",
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Monthly Build Challenge",
                cadence="Monthly",
                focus="Themed building competition",
                rewards=["Featured placement", "Exclusive items"],
                retention_goal="Regular content creation",
            )
        ],
        narrative_beats=[
            NarrativeBeatInfo(
                beat_name="First City",
                synopsis="Tutorial: Build your first functioning city",
                branching_choice="Focus on efficiency or aesthetics",
                emotional_tone="Discovery and accomplishment",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="UI Scaling",
                status="Implemented",
                notes="Adjustable UI scale from 80% to 200%",
                platform_support=["PC"],
            )
        ],
        audio_design=[
            AudioDesignCue(
                cue_name="Ambient City Sounds",
                composer="Procedural Audio System",
                style="Dynamic ambient based on city state",
                gameplay_trigger="Background ambience that reflects city health",
            )
        ],
    )


def test_simulation_sandbox_basic_creation():
    """Test basic simulation sandbox game creation."""
    game = SimulationSandboxGameInfo(title="Test Sandbox")
    assert game.title == "Test Sandbox"
    assert game.model_name == "SimulationSandboxGameInfo"


def test_simulation_sandbox_fact_pairs(simulation_sandbox_game_full):
    """Test fact pairs generation."""
    facts = dict(simulation_sandbox_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "120" in facts["Session Length"]
    assert "workshop" in facts["Sharing"].lower()


def test_simulation_sandbox_extra_panels(simulation_sandbox_game_full):
    """Test extra panels generation."""
    panels = simulation_sandbox_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Systems" in panel_titles
    assert "Player Creation" in panel_titles


def test_simulation_sandbox_render_includes_content(simulation_sandbox_game_full, console):
    """Test render includes all expected content."""
    simulation_sandbox_game_full.render(console)
    text = console.export_text()
    assert "Universe Builder" in text
    assert "Deep simulation" in text


def test_simulation_sandbox_instruction_helpers():
    """Test instruction helper methods."""
    combined = SimulationSandboxGameInfo.get_instructions(["Focus on emergent gameplay"])
    assert isinstance(combined, str)

    prompt = SimulationSandboxGameInfo.get_user_prompt("Test Sandbox")
    assert "Test Sandbox" in prompt

    formatted = SimulationSandboxGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_simulation_sandbox_simulation_systems(simulation_sandbox_game_full):
    """Test simulation system profiles."""
    assert len(simulation_sandbox_game_full.simulation_systems) == 2
    assert simulation_sandbox_game_full.simulation_systems[0].name == "Economy Simulation"
    assert "Market crashes" in simulation_sandbox_game_full.simulation_systems[0].emergent_outcomes


def test_simulation_sandbox_creator_tools(simulation_sandbox_game_full):
    """Test creator tool profiles."""
    assert len(simulation_sandbox_game_full.creator_tools) == 2
    assert simulation_sandbox_game_full.creator_tools[0].tool_name == "Terrain Editor"
    assert simulation_sandbox_game_full.creator_tools[1].tool_name == "Logic Engine"


def test_simulation_sandbox_economy_loops(simulation_sandbox_game_full):
    """Test economy loops."""
    assert len(simulation_sandbox_game_full.economy_loops) == 1
    loop = simulation_sandbox_game_full.economy_loops[0]
    assert loop.loop_name == "Creation Economy"


def test_simulation_sandbox_table_sections(simulation_sandbox_game_full):
    """Test table sections generation."""
    sections = simulation_sandbox_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Simulation Systems" in section_titles
    assert "Creator Tools" in section_titles
    assert "Economy Loops" in section_titles


def test_simulation_sandbox_empty_optional_fields(console):
    """Test game with minimal data."""
    game = SimulationSandboxGameInfo(
        title="Minimal Sandbox",
        game_summary="Basic sandbox",
        core_loop="Build things",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Session Length"] == "-"


def test_simulation_sandbox_roundtrip():
    """Test serialization roundtrip."""
    original = SimulationSandboxGameInfo(
        title="Roundtrip Sandbox",
        game_summary="Testing serialization",
        core_loop="test -> verify",
        release_year=2024,
        average_session_minutes=90.0,
        simulation_scope="Test scope",
    )
    data = original.to_dict()
    restored = SimulationSandboxGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.average_session_minutes == original.average_session_minutes
    assert restored.simulation_scope == original.simulation_scope


def test_simulation_system_profile_table_schema():
    """Test SimulationSystemProfile has table schema."""
    schema = SimulationSystemProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "System" in headers


def test_creator_tool_profile_table_schema():
    """Test CreatorToolProfile has table schema."""
    schema = CreatorToolProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Tool" in headers


def test_simulation_sandbox_tech_constraints(simulation_sandbox_game_full):
    """Test technical constraints are documented."""
    assert simulation_sandbox_game_full.tech_constraints
    assert "10,000" in simulation_sandbox_game_full.tech_constraints
