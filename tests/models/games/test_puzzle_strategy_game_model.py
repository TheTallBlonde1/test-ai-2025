"""Tests for PuzzleStrategyGameInfo model."""

import pytest

from aiss.models.games._base import (
    AccessibilityFeatureInfo,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    SessionProfileInfo,
    StudioProfile,
)
from aiss.models.games.puzzle_strategy_model import (
    PuzzleModuleInfo,
    PuzzleStrategyGameInfo,
    StrategyScenarioInfo,
    TeachingMomentInfo,
)


@pytest.fixture
def puzzle_strategy_game_full():
    """Create a fully populated puzzle strategy game instance for testing."""
    return PuzzleStrategyGameInfo(
        title="Mind's Edge Tactics",
        game_summary="Cerebral strategy game blending puzzles with tactical combat",
        core_loop="Plan, execute, evaluate, optimize",
        ruleset_overview="Turn-based tactics with resource management",
        difficulty_philosophy="Gradual escalation with optional challenge modes",
        ai_capabilities="Adaptive AI that learns player strategies",
        release_year=2024,
        average_session_minutes=45,
        target_audience="Strategy enthusiasts and puzzle solvers",
        replayability_hooks=["Procedural missions", "Multiple solutions", "Score chasing"],
        monetisation_model="Premium with expansion packs",
        developers=[
            StudioProfile(
                name="Cerebral Games",
                role="lead developer",
                headquarters="Cambridge, UK",
                team_size=45,
                notable_credits=["Logic Wars", "Chess Masters"],
                technology_stack=["Unity", "AI Framework"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Strategy Publishing",
                role="publisher",
                headquarters="Berlin, Germany",
                team_size=25,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - Steam",
                release_date="2024-08-10",
                edition="Standard",
                resolution_target="1080p",
                frame_rate_target="60 FPS",
                platform_features=["Steam Workshop", "Achievements"],
            ),
            PlatformReleaseInfo(
                platform="Nintendo Switch",
                release_date="2024-10-15",
                edition="Portable",
                resolution_target="720p",
                frame_rate_target="30 FPS",
                platform_features=["Touch controls", "Portable mode"],
            ),
        ],
        puzzle_modules=[
            PuzzleModuleInfo(
                module_name="Foundations",
                challenge_theme="Basic mechanics introduction",
                mechanics_introduced=["Movement", "Resource gathering", "Basic tactics"],
                difficulty_ramp="Gentle introduction with escalating complexity",
                completion_rate_target=95.0,
            ),
            PuzzleModuleInfo(
                module_name="Advanced Warfare",
                challenge_theme="Multi-objective coordination",
                mechanics_introduced=["Unit synergies", "Environmental hazards"],
                difficulty_ramp="Steep with optional hints",
                completion_rate_target=65.0,
            ),
        ],
        strategy_scenarios=[
            StrategyScenarioInfo(
                scenario_name="Desert Siege",
                objective="Capture enemy stronghold within turn limit",
                map_type="Asymmetric with chokepoints",
                ai_behaviour_notes="Defensive posture with counter-attack triggers",
                turn_limit=25,
            )
        ],
        gameplay_layers=[
            GameplayMechanicHighlight(
                mechanic="Resource Chains",
                category="strategy",
                description="Building interconnected resource production",
                player_impact="Rewards long-term planning",
                mastery_curve="High - requires optimization",
            )
        ],
        teaching_moments=[
            TeachingMomentInfo(
                beat_name="First Tactics",
                learning_goal="Understanding unit positioning",
                delivery_method="Interactive tutorial with immediate feedback",
                analytics_signal="Tutorial completion time and retry count",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Commander Rank",
                track_type="XP",
                unlocks=["New units", "Advanced scenarios"],
                pacing="Milestone-based",
                hard_cap=30,
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Weekly Challenge",
                cadence="Weekly",
                focus="Community-created scenarios",
                rewards=["Leaderboard placement", "Cosmetics"],
                retention_goal="Regular engagement",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Colorblind Mode",
                status="Implemented",
                notes="High contrast mode with patterns",
                platform_support=["PC", "Switch"],
            )
        ],
        session_profiles=[
            SessionProfileInfo(
                activity="Puzzle Solving",
                average_duration_minutes=30,
                player_goal="Complete daily challenge",
                engagement_metric="Daily active users",
            )
        ],
    )


def test_puzzle_strategy_basic_creation():
    """Test basic puzzle strategy game creation."""
    game = PuzzleStrategyGameInfo(title="Test Puzzle")
    assert game.title == "Test Puzzle"
    assert game.model_name == "PuzzleStrategyGameInfo"


def test_puzzle_strategy_fact_pairs(puzzle_strategy_game_full):
    """Test fact pairs generation."""
    facts = dict(puzzle_strategy_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "45" in facts["Session Length"]
    assert "Strategy enthusiasts" in facts["Audience"]


def test_puzzle_strategy_extra_panels(puzzle_strategy_game_full):
    """Test extra panels generation."""
    panels = puzzle_strategy_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Systems Overview" in panel_titles
    assert "Difficulty Philosophy" in panel_titles


def test_puzzle_strategy_render_includes_content(puzzle_strategy_game_full, console):
    """Test render includes all expected content."""
    puzzle_strategy_game_full.render(console)
    text = console.export_text()
    assert "Mind's Edge Tactics" in text
    assert "Cerebral strategy" in text


def test_puzzle_strategy_instruction_helpers():
    """Test instruction helper methods."""
    combined = PuzzleStrategyGameInfo.get_instructions(["Focus on replayability"])
    assert isinstance(combined, str)

    prompt = PuzzleStrategyGameInfo.get_user_prompt("Test Puzzle")
    assert "Test Puzzle" in prompt

    formatted = PuzzleStrategyGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_puzzle_strategy_puzzle_modules(puzzle_strategy_game_full):
    """Test puzzle module profiles."""
    assert len(puzzle_strategy_game_full.puzzle_modules) == 2
    assert puzzle_strategy_game_full.puzzle_modules[0].module_name == "Foundations"
    assert puzzle_strategy_game_full.puzzle_modules[0].completion_rate_target == 95.0


def test_puzzle_strategy_scenarios(puzzle_strategy_game_full):
    """Test strategy scenarios."""
    assert len(puzzle_strategy_game_full.strategy_scenarios) == 1
    scenario = puzzle_strategy_game_full.strategy_scenarios[0]
    assert scenario.scenario_name == "Desert Siege"
    assert scenario.turn_limit == 25


def test_puzzle_strategy_teaching_moments(puzzle_strategy_game_full):
    """Test teaching moments."""
    assert len(puzzle_strategy_game_full.teaching_moments) == 1
    moment = puzzle_strategy_game_full.teaching_moments[0]
    assert moment.beat_name == "First Tactics"
    assert "positioning" in moment.learning_goal


def test_puzzle_strategy_replayability_hooks(puzzle_strategy_game_full):
    """Test replayability hooks."""
    assert len(puzzle_strategy_game_full.replayability_hooks) == 3
    assert "Procedural missions" in puzzle_strategy_game_full.replayability_hooks


def test_puzzle_strategy_table_sections(puzzle_strategy_game_full):
    """Test table sections generation."""
    sections = puzzle_strategy_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Puzzle Modules" in section_titles
    assert "Scenarios" in section_titles
    assert "Teaching Moments" in section_titles


def test_puzzle_strategy_empty_optional_fields(console):
    """Test game with minimal data."""
    game = PuzzleStrategyGameInfo(
        title="Minimal Puzzle",
        game_summary="Basic puzzle game",
        core_loop="Think and solve",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Session Length"] == "-"


def test_puzzle_strategy_roundtrip():
    """Test serialization roundtrip."""
    original = PuzzleStrategyGameInfo(
        title="Roundtrip Puzzle",
        game_summary="Testing serialization",
        core_loop="test -> verify",
        release_year=2024,
        average_session_minutes=30,
        target_audience="Testers",
    )
    data = original.to_dict()
    restored = PuzzleStrategyGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.average_session_minutes == original.average_session_minutes
    assert restored.target_audience == original.target_audience


def test_puzzle_module_info_table_schema():
    """Test PuzzleModuleInfo has table schema."""
    schema = PuzzleModuleInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Module" in headers


def test_strategy_scenario_info_table_schema():
    """Test StrategyScenarioInfo has table schema."""
    schema = StrategyScenarioInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Scenario" in headers


def test_teaching_moment_info_table_schema():
    """Test TeachingMomentInfo has table schema."""
    schema = TeachingMomentInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Beat" in headers
