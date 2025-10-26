"""Tests for ShooterGameInfo model."""

import pytest

from aiss.models.games._base import (
    AccessibilityFeatureInfo,
    EconomyModelInfo,
    EsportsEventInfo,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    MultiplayerModeInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    SessionProfileInfo,
    StudioProfile,
    TechnicalBenchmarkInfo,
)
from aiss.models.games.shooter_model import (
    MapRotationInfo,
    ShooterGameInfo,
    WeaponArchetypeInfo,
)


@pytest.fixture
def shooter_game_full():
    """Create a fully populated shooter game instance for testing."""
    return ShooterGameInfo(
        title="Tactical Strike Arena",
        game_summary="Fast-paced tactical shooter with strategic depth",
        core_loop="Engage, reposition, secure objective, repeat",
        combat_philosophy="Precise gunplay with low time-to-kill rewards accuracy",
        movement_signature="Fluid slide-and-vault system with momentum preservation",
        player_perspective="first-person",
        release_year=2024,
        match_length_minutes=25,
        netcode_strategy="128-tick dedicated servers with rollback compensation",
        anti_cheat_approach="Kernel-level driver with machine learning detection",
        crossplay_support=True,
        ranked_focus="Skill-based matchmaking with seasonal rank resets",
        monetisation_model="Free-to-play with premium battle pass",
        developers=[
            StudioProfile(
                name="Strike Dev Studios",
                role="lead developer",
                headquarters="Seattle, USA",
                team_size=120,
                notable_credits=["Previous Shooter", "Arena Combat"],
                technology_stack=["Unreal Engine 5", "Custom Netcode"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Big Game Publisher",
                role="publisher",
                headquarters="Tokyo, Japan",
                team_size=50,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - Steam",
                release_date="2024-03-15",
                edition="Standard",
                resolution_target="4K",
                frame_rate_target="240 FPS",
                platform_features=["Steam Workshop", "Cloud Saves"],
            ),
            PlatformReleaseInfo(
                platform="PlayStation 5",
                release_date="2024-03-15",
                edition="Console",
                resolution_target="1440p",
                frame_rate_target="120 FPS",
                platform_features=["DualSense Haptics", "Activity Cards"],
            ),
        ],
        weapon_archetypes=[
            WeaponArchetypeInfo(
                name="Assault Rifle",
                role="Versatile mid-range engagement",
                fire_rate_profile="600 RPM",
                optimal_range="20-40 meters",
                skill_ceiling="Medium",
            ),
            WeaponArchetypeInfo(
                name="Sniper Rifle",
                role="Long-range elimination",
                fire_rate_profile="Bolt-action",
                optimal_range="60+ meters",
                skill_ceiling="High",
            ),
        ],
        gameplay_pillars=[
            GameplayMechanicHighlight(
                mechanic="Tactical Positioning",
                category="combat",
                description="Cover system with destructible environments",
                player_impact="Forces strategic thinking and team coordination",
                mastery_curve="Steep - requires map knowledge and prediction",
            )
        ],
        map_rotation=[
            MapRotationInfo(
                map_name="Downtown District",
                environment="Urban cityscape",
                layout_identity="Three-lane with vertical elements",
                mode_alignment=["Team Deathmatch", "Domination", "Search & Destroy"],
                callouts=["A Site", "B Site", "Mid", "Connector", "Spawn"],
            )
        ],
        multiplayer_modes=[
            MultiplayerModeInfo(
                mode_name="Ranked Domination",
                mode_type="PvP objective control",
                max_players=10,
                is_ranked=True,
                cross_play=True,
                description="Capture and hold three zones to score points",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Player Level",
                track_type="XP",
                unlocks=["Weapons", "Attachments", "Cosmetics"],
                pacing="Linear with seasonal boosts",
                hard_cap=100,
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Season 1: New Dawn",
                cadence="3 months",
                focus="New maps and weapons",
                rewards=["Exclusive skins", "Battle pass items"],
                retention_goal="Maintain weekly active users",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Colorblind Modes",
                status="Implemented",
                notes="Protanopia, Deuteranopia, and Tritanopia modes",
                platform_support=["PC", "PlayStation 5", "Xbox Series X"],
            )
        ],
        economy_models=[
            EconomyModelInfo(
                currency="V-Coins",
                acquisition=["Battle Pass", "Weekly Challenges", "Purchase"],
                spending=["Cosmetics", "Battle Pass Tiers"],
                monetisation_type="cosmetic-only",
                average_spend=1500,
            )
        ],
        esports_events=[
            EsportsEventInfo(
                event_name="Tactical Strike Championship",
                tier="pro",
                region="Global",
                prize_pool=1000000,
                broadcast_partners=["Twitch", "YouTube Gaming"],
                format_notes="Double elimination bracket with best of 5 finals",
            )
        ],
        technical_benchmarks=[
            TechnicalBenchmarkInfo(
                scenario="Intense firefight with 10 players",
                hardware_profile="RTX 4070 / Ryzen 7 5800X",
                target_metrics="1440p @ 144 FPS",
                measured_metrics="1440p @ 152 FPS average",
                optimisation_notes="DLSS Quality mode enabled",
            )
        ],
        session_profiles=[
            SessionProfileInfo(
                activity="Competitive Ranked",
                average_duration_minutes=45,
                player_goal="Climb ranked ladder and improve skills",
                engagement_metric="Daily active users and match completion rate",
            )
        ],
    )


def test_shooter_game_basic_creation():
    """Test basic shooter game creation."""
    game = ShooterGameInfo(title="Test Shooter")
    assert game.title == "Test Shooter"
    assert game.model_name == "ShooterGameInfo"


def test_shooter_game_fact_pairs(shooter_game_full):
    """Test fact pairs generation."""
    facts = dict(shooter_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert facts["Perspective"] == "first-person"
    assert facts["Crossplay"] == "Enabled"
    assert "128-tick" in facts["Netcode"]


def test_shooter_game_extra_panels(shooter_game_full):
    """Test extra panels generation."""
    panels = shooter_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Combat & Movement" in panel_titles
    assert "Service Overview" in panel_titles


def test_shooter_game_render_includes_content(shooter_game_full, console):
    """Test render includes all expected content."""
    shooter_game_full.render(console)
    text = console.export_text()
    assert "Tactical Strike Arena" in text
    assert "Fast-paced tactical shooter" in text
    assert "first-person" in text or "Perspective" in text


def test_shooter_game_instruction_helpers():
    """Test instruction helper methods."""
    combined = ShooterGameInfo.get_instructions(["Focus on esports readiness"])
    assert "Additional context" in combined
    assert "Focus on esports readiness" in combined

    prompt = ShooterGameInfo.get_user_prompt("Test Shooter")
    assert "Test Shooter" in prompt
    assert "shooter" in prompt.lower()

    formatted = ShooterGameInfo.json_format_instructions()
    assert "shooter" in formatted.lower()
    assert "JSON" in formatted


def test_shooter_game_weapon_archetypes(shooter_game_full):
    """Test weapon archetypes are included in rendering."""
    assert len(shooter_game_full.weapon_archetypes) == 2
    assert shooter_game_full.weapon_archetypes[0].name == "Assault Rifle"
    assert shooter_game_full.weapon_archetypes[1].skill_ceiling == "High"


def test_shooter_game_map_rotation(shooter_game_full):
    """Test map rotation data."""
    assert len(shooter_game_full.map_rotation) == 1
    map_info = shooter_game_full.map_rotation[0]
    assert map_info.map_name == "Downtown District"
    assert "Three-lane" in map_info.layout_identity
    assert "A Site" in map_info.callouts


def test_shooter_game_crossplay_support(shooter_game_full):
    """Test crossplay support."""
    assert shooter_game_full.crossplay_support is True
    facts = dict(shooter_game_full._fact_pairs())
    assert facts["Crossplay"] == "Enabled"


def test_shooter_game_no_crossplay():
    """Test game without crossplay."""
    game = ShooterGameInfo(title="No Crossplay", crossplay_support=False)
    facts = dict(game._fact_pairs())
    assert facts["Crossplay"] == "Unavailable"


def test_shooter_game_table_sections(shooter_game_full):
    """Test table sections generation."""
    sections = shooter_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Publishers" in section_titles
    assert "Weapon Archetypes" in section_titles
    assert "Map Pool" in section_titles
    assert "Multiplayer Modes" in section_titles


def test_shooter_game_monetisation():
    """Test monetisation model tracking."""
    game = ShooterGameInfo(
        title="F2P Shooter",
        monetisation_model="Free-to-play with cosmetic microtransactions",
    )
    facts = dict(game._fact_pairs())
    assert "Free-to-play" in facts["Monetisation"]


def test_shooter_game_empty_optional_fields(console):
    """Test game with minimal data."""
    game = ShooterGameInfo(
        title="Minimal Shooter",
        game_summary="Basic shooter",
        core_loop="Shoot enemies",
    )
    game.render(console)  # Should not crash
    facts = dict(game._fact_pairs())
    assert facts["Crossplay"] == "Unavailable"
    assert facts["Netcode"] == "-"


def test_shooter_game_roundtrip():
    """Test serialization roundtrip."""
    original = ShooterGameInfo(
        title="Roundtrip Shooter",
        game_summary="Testing serialization",
        core_loop="test -> shoot -> verify",
        release_year=2024,
        crossplay_support=True,
        match_length_minutes=30,
    )
    data = original.to_dict()
    restored = ShooterGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.crossplay_support == original.crossplay_support
    assert restored.match_length_minutes == original.match_length_minutes


def test_weapon_archetype_table_schema():
    """Test WeaponArchetypeInfo has table schema."""
    schema = WeaponArchetypeInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Weapon" in headers


def test_map_rotation_table_schema():
    """Test MapRotationInfo has table schema."""
    schema = MapRotationInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Map" in headers


def test_shooter_game_match_length_formatting(shooter_game_full):
    """Test match length is properly formatted."""
    facts = dict(shooter_game_full._fact_pairs())
    # Should have match length in facts
    assert "Match Length" in facts
    # Should format time appropriately
    match_length = facts["Match Length"]
    assert match_length != "-"


def test_shooter_game_esports_integration(shooter_game_full):
    """Test esports data is properly stored and rendered."""
    assert len(shooter_game_full.esports_events) == 1
    event = shooter_game_full.esports_events[0]
    assert event.event_name == "Tactical Strike Championship"
    assert event.prize_pool == 1000000
    assert event.tier == "pro"


def test_shooter_game_technical_benchmarks(shooter_game_full):
    """Test technical benchmarks data."""
    assert len(shooter_game_full.technical_benchmarks) == 1
    bench = shooter_game_full.technical_benchmarks[0]
    assert "RTX 4070" in bench.hardware_profile
    assert "1440p" in bench.measured_metrics
