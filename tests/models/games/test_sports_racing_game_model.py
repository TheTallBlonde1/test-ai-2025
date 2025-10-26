"""Tests for SportsRacingGameInfo model."""

import pytest

from aiss.models.games._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    EconomyLoopInfo,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
)
from aiss.models.games.sports_racing_model import (
    AthleteVehicleProfile,
    LeagueLicenseProfile,
    SportsModeProfile,
    SportsRacingGameInfo,
)


@pytest.fixture
def sports_racing_game_full():
    """Create a fully populated sports racing game instance for testing."""
    return SportsRacingGameInfo(
        title="Grand Prix Ultimate",
        game_summary="Authentic racing simulation with esports focus",
        core_loop="Race, upgrade, compete, broadcast",
        sport_focus="Formula-style circuit racing",
        licence_strategy="FIA licensing with historic vehicles",
        physics_fidelity="Simulation-grade tire and aerodynamic modeling",
        skill_gap_statement="High skill ceiling with comprehensive driving assists",
        broadcast_hooks="Dynamic camera system and real-time telemetry overlay",
        monetisation_model="Premium with season pass for new content",
        live_season_plan="Quarterly seasons aligned with real racing calendar",
        release_year=2024,
        average_match_minutes=25.0,
        developers=[
            StudioProfile(
                name="Velocity Studios",
                role="lead developer",
                headquarters="Milan, Italy",
                team_size=180,
                notable_credits=["Speed Masters", "Racing Legends"],
                technology_stack=["Custom Physics Engine", "Photogrammetry"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Racing Games Inc",
                role="publisher",
                headquarters="London, UK",
                team_size=80,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PlayStation 5",
                release_date="2024-04-15",
                edition="Standard",
                resolution_target="4K",
                frame_rate_target="60 FPS",
                platform_features=["DualSense Haptics", "3D Audio", "Ray Tracing"],
            ),
            PlatformReleaseInfo(
                platform="Xbox Series X",
                release_date="2024-04-15",
                edition="Standard",
                resolution_target="4K",
                frame_rate_target="60 FPS",
                platform_features=["Quick Resume", "120 FPS mode"],
            ),
        ],
        league_licenses=[
            LeagueLicenseProfile(
                name="International Racing Championship",
                scope="Global",
                format_overview="Season-based circuit racing",
                renewal_term="5-year exclusive",
            )
        ],
        roster=[
            AthleteVehicleProfile(
                name="Thunder X1",
                classification="Formula Class A",
                headline_rating="98 Speed",
                signature_strength="Superior cornering stability",
            ),
            AthleteVehicleProfile(
                name="Phoenix GT",
                classification="Formula Class B",
                headline_rating="95 Speed",
                signature_strength="Excellent acceleration",
            ),
        ],
        modes=[
            SportsModeProfile(
                mode_name="Career Mode",
                structure="Multi-season progression",
                key_features=["Team management", "Contract negotiations", "R&D upgrades"],
                online_enabled=False,
            ),
            SportsModeProfile(
                mode_name="Online Championship",
                structure="Seasonal competitive ladder",
                key_features=["Ranked matchmaking", "Safety rating", "Live timing"],
                online_enabled=True,
            ),
        ],
        mechanics=[
            GameplayMechanicHighlight(
                mechanic="Dynamic Weather",
                category="simulation",
                description="Real-time weather affecting track conditions",
                player_impact="Requires strategic tire and setup changes",
                mastery_curve="High - weather reading is crucial",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Driver Level",
                track_type="XP",
                unlocks=["Vehicles", "Liveries", "Tracks"],
                pacing="Balanced with milestone rewards",
                hard_cap=100,
            )
        ],
        economy_loops=[
            EconomyLoopInfo(
                loop_name="Team Currency",
                loop_type="core",
                inputs=["Race performance", "Challenges"],
                outputs=["Vehicle upgrades", "Customization"],
                monetisation_hook="Premium currency for instant unlocks",
                retention_goal="Daily engagement through challenges",
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Season Pass: Spring Championship",
                cadence="Quarterly",
                focus="New tracks and vehicles",
                rewards=["Exclusive liveries", "Championship points"],
                retention_goal="Seasonal player retention",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Comprehensive Driving Assists",
                status="Implemented",
                notes="Adjustable ABS, traction control, and racing line",
                platform_support=["All platforms"],
            )
        ],
        audio_design=[
            AudioDesignCue(
                cue_name="Engine Audio System",
                composer="Sound Design Team",
                style="Recorded engine samples with dynamic mixing",
                gameplay_trigger="Real-time based on engine state and exhaust",
            )
        ],
    )


def test_sports_racing_basic_creation():
    """Test basic sports racing game creation."""
    game = SportsRacingGameInfo(title="Test Racing")
    assert game.title == "Test Racing"
    assert game.model_name == "SportsRacingGameInfo"


def test_sports_racing_fact_pairs(sports_racing_game_full):
    """Test fact pairs generation."""
    facts = dict(sports_racing_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "25" in facts["Match Length"]
    assert "FIA" in facts["Licence Strategy"]


def test_sports_racing_extra_panels(sports_racing_game_full):
    """Test extra panels generation."""
    panels = sports_racing_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Competition" in panel_titles
    assert "Skill & Physics" in panel_titles


def test_sports_racing_render_includes_content(sports_racing_game_full, console):
    """Test render includes all expected content."""
    sports_racing_game_full.render(console)
    text = console.export_text()
    assert "Grand Prix Ultimate" in text
    assert "Authentic racing" in text


def test_sports_racing_instruction_helpers():
    """Test instruction helper methods."""
    combined = SportsRacingGameInfo.get_instructions(["Emphasize realism"])
    assert isinstance(combined, str)

    prompt = SportsRacingGameInfo.get_user_prompt("Test Racing")
    assert "Test Racing" in prompt

    formatted = SportsRacingGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_sports_racing_league_licenses(sports_racing_game_full):
    """Test league license profiles."""
    assert len(sports_racing_game_full.league_licenses) == 1
    license_info = sports_racing_game_full.league_licenses[0]
    assert license_info.name == "International Racing Championship"
    assert license_info.scope == "Global"


def test_sports_racing_roster(sports_racing_game_full):
    """Test roster profiles."""
    assert len(sports_racing_game_full.roster) == 2
    assert sports_racing_game_full.roster[0].name == "Thunder X1"
    assert "98 Speed" in sports_racing_game_full.roster[0].headline_rating


def test_sports_racing_modes(sports_racing_game_full):
    """Test sports mode profiles."""
    assert len(sports_racing_game_full.modes) == 2
    assert sports_racing_game_full.modes[0].mode_name == "Career Mode"
    assert sports_racing_game_full.modes[0].online_enabled is False
    assert sports_racing_game_full.modes[1].online_enabled is True


def test_sports_racing_table_sections(sports_racing_game_full):
    """Test table sections generation."""
    sections = sports_racing_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Licences" in section_titles
    assert "Roster" in section_titles
    assert "Modes" in section_titles


def test_sports_racing_empty_optional_fields(console):
    """Test game with minimal data."""
    game = SportsRacingGameInfo(
        title="Minimal Racing",
        game_summary="Basic racing",
        core_loop="Race and win",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Match Length"] == "-"


def test_sports_racing_roundtrip():
    """Test serialization roundtrip."""
    original = SportsRacingGameInfo(
        title="Roundtrip Racing",
        game_summary="Testing serialization",
        core_loop="test -> verify",
        release_year=2024,
        average_match_minutes=20.0,
        sport_focus="Testing",
    )
    data = original.to_dict()
    restored = SportsRacingGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.average_match_minutes == original.average_match_minutes
    assert restored.sport_focus == original.sport_focus


def test_league_license_profile_table_schema():
    """Test LeagueLicenseProfile has table schema."""
    schema = LeagueLicenseProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "League" in headers


def test_athlete_vehicle_profile_table_schema():
    """Test AthleteVehicleProfile has table schema."""
    schema = AthleteVehicleProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Name" in headers


def test_sports_mode_profile_table_schema():
    """Test SportsModeProfile has table schema."""
    schema = SportsModeProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Mode" in headers


def test_sports_racing_physics_fidelity(sports_racing_game_full):
    """Test physics fidelity documentation."""
    assert sports_racing_game_full.physics_fidelity
    assert "tire" in sports_racing_game_full.physics_fidelity.lower()


def test_sports_racing_broadcast_hooks(sports_racing_game_full):
    """Test broadcast hooks."""
    assert sports_racing_game_full.broadcast_hooks
    assert "camera" in sports_racing_game_full.broadcast_hooks.lower()
