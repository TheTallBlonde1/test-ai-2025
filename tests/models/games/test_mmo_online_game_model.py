"""Tests for MmoOnlineGameInfo model."""

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
    SocialFeatureInfo,
    StudioProfile,
)
from aiss.models.games.mmo_online_model import (
    CommunityProgramProfile,
    EndgameActivityProfile,
    MmoOnlineGameInfo,
    ServerArchitectureProfile,
)


@pytest.fixture
def mmo_online_game_full():
    """Create a fully populated MMO online game instance for testing."""
    return MmoOnlineGameInfo(
        title="Eternal Realms Online",
        game_summary="Persistent fantasy MMO with dynamic world events",
        core_loop="Quest, raid, compete, socialize",
        world_structure="Seamless open world with instanced dungeons",
        social_vision="Guild-centric with cross-server activities",
        operations_cadence="Bi-weekly patches with quarterly expansions",
        monetisation_pillars="Subscription + optional cosmetics",
        retention_levers="Daily rewards, seasonal events, guild progression",
        release_year=2024,
        peak_concurrency_target=500000,
        developers=[
            StudioProfile(
                name="Massive World Studios",
                role="lead developer",
                headquarters="Austin, Texas",
                team_size=350,
                notable_credits=["World Quest", "Legends MMO"],
                technology_stack=["Custom Engine", "Cloud Infrastructure"],
            )
        ],
        publishers=[
            StudioProfile(
                name="Online Games Corp",
                role="publisher",
                headquarters="San Francisco, USA",
                team_size=120,
            )
        ],
        platform_releases=[
            PlatformReleaseInfo(
                platform="PC - Windows",
                release_date="2024-06-15",
                edition="Standard",
                resolution_target="4K",
                frame_rate_target="60 FPS",
                platform_features=["DirectX 12", "Ray Tracing"],
            )
        ],
        server_architecture=[
            ServerArchitectureProfile(
                name="Megaserver Architecture",
                capacity="50,000 concurrent per realm",
                matchmaking_scope="Cross-realm for dungeons and PvP",
                region_support="NA, EU, Asia, OCE",
            )
        ],
        social_features=[
            SocialFeatureInfo(
                feature_name="Guild System",
                surface_area="Guild halls and management UI",
                communication_tools=["Voice chat", "Text channels", "Event calendar"],
                safety_tooling="Automated moderation with reporting",
                retention_role="Provides social anchors and progression goals",
            )
        ],
        mechanics=[
            GameplayMechanicHighlight(
                mechanic="Dynamic Event System",
                category="world events",
                description="Large-scale events that reshape zones",
                player_impact="Creates emergent social gameplay",
                mastery_curve="Low entry, high coordination ceiling",
            )
        ],
        progression_tracks=[
            ProgressionTrackInfo(
                track_name="Character Level",
                track_type="XP",
                unlocks=["Skills", "Zones", "Equipment Tiers"],
                pacing="Guided early, open-ended endgame",
                hard_cap=60,
            )
        ],
        economy_loops=[
            EconomyLoopInfo(
                loop_name="Crafting Economy",
                loop_type="core",
                inputs=["Gathered materials", "Dungeon drops"],
                outputs=["Player equipment", "Consumables"],
                monetisation_hook="Cosmetic patterns available in shop",
                retention_goal="Player interdependence and trading",
            )
        ],
        endgame_activities=[
            EndgameActivityProfile(
                activity_name="Mythic Raids",
                description="20-player challenging raid content",
                recommended_team="20 coordinated players",
                rewards=["Legendary gear", "Cosmetic titles", "Mounts"],
            )
        ],
        live_events=[
            LiveServiceEventInfo(
                event_name="Summer Festival",
                cadence="Annual",
                focus="Limited-time quests and rewards",
                rewards=["Seasonal cosmetics", "Event currency"],
                retention_goal="Re-engage dormant players",
            )
        ],
        community_programs=[
            CommunityProgramProfile(
                program_name="Creator Partner Program",
                focus="Content creators and streamers",
                cadence="Ongoing",
                incentives=["Early access", "Exclusive items", "Revenue share"],
            )
        ],
        narrative_beats=[
            NarrativeBeatInfo(
                beat_name="The Sundering",
                synopsis="World-changing event that opens new zones",
                branching_choice="Faction alignment choice",
                emotional_tone="Epic and consequential",
            )
        ],
        accessibility_features=[
            AccessibilityFeatureInfo(
                feature="Colorblind Support",
                status="Implemented",
                notes="Multiple colorblind modes with UI adjustments",
                platform_support=["PC"],
            )
        ],
        audio_design=[
            AudioDesignCue(
                cue_name="Realm Theme",
                composer="Orchestra Ensemble",
                style="Epic orchestral",
                gameplay_trigger="Zone transitions and major events",
            )
        ],
    )


def test_mmo_online_basic_creation():
    """Test basic MMO online game creation."""
    game = MmoOnlineGameInfo(title="Test MMO")
    assert game.title == "Test MMO"
    assert game.model_name == "MmoOnlineGameInfo"


def test_mmo_online_fact_pairs(mmo_online_game_full):
    """Test fact pairs generation."""
    facts = dict(mmo_online_game_full._fact_pairs())
    assert facts["Release Year"] == "2024"
    assert "500" in facts["Peak CCU"]
    assert "Bi-weekly" in facts["Operations"]


def test_mmo_online_extra_panels(mmo_online_game_full):
    """Test extra panels generation."""
    panels = mmo_online_game_full._extra_panels()
    assert panels
    panel_titles = {title for title, _, _ in panels}
    assert "Operations" in panel_titles
    assert "Community" in panel_titles


def test_mmo_online_render_includes_content(mmo_online_game_full, console):
    """Test render includes all expected content."""
    mmo_online_game_full.render(console)
    text = console.export_text()
    assert "Eternal Realms Online" in text
    assert "Persistent fantasy MMO" in text


def test_mmo_online_instruction_helpers():
    """Test instruction helper methods."""
    combined = MmoOnlineGameInfo.get_instructions(["Focus on social features"])
    assert isinstance(combined, str)

    prompt = MmoOnlineGameInfo.get_user_prompt("Test MMO")
    assert "Test MMO" in prompt
    assert "MMO" in prompt or "online" in prompt.lower()

    formatted = MmoOnlineGameInfo.json_format_instructions()
    assert "JSON" in formatted


def test_mmo_online_server_architecture(mmo_online_game_full):
    """Test server architecture profiles."""
    assert len(mmo_online_game_full.server_architecture) == 1
    arch = mmo_online_game_full.server_architecture[0]
    assert arch.name == "Megaserver Architecture"
    assert "50,000" in arch.capacity


def test_mmo_online_social_features(mmo_online_game_full):
    """Test social features."""
    assert len(mmo_online_game_full.social_features) == 1
    feature = mmo_online_game_full.social_features[0]
    assert feature.feature_name == "Guild System"
    assert "Voice chat" in feature.communication_tools


def test_mmo_online_endgame_activities(mmo_online_game_full):
    """Test endgame activities."""
    assert len(mmo_online_game_full.endgame_activities) == 1
    activity = mmo_online_game_full.endgame_activities[0]
    assert activity.activity_name == "Mythic Raids"
    assert "20" in activity.recommended_team


def test_mmo_online_economy_loops(mmo_online_game_full):
    """Test economy loops."""
    assert len(mmo_online_game_full.economy_loops) == 1
    loop = mmo_online_game_full.economy_loops[0]
    assert loop.loop_name == "Crafting Economy"


def test_mmo_online_community_programs(mmo_online_game_full):
    """Test community programs."""
    assert len(mmo_online_game_full.community_programs) == 1
    program = mmo_online_game_full.community_programs[0]
    assert program.program_name == "Creator Partner Program"


def test_mmo_online_table_sections(mmo_online_game_full):
    """Test table sections generation."""
    sections = mmo_online_game_full._table_sections()
    section_titles = {title for title, _, _ in sections}

    assert "Developers" in section_titles
    assert "Server Architecture" in section_titles
    assert "Social Systems" in section_titles
    assert "Endgame" in section_titles


def test_mmo_online_empty_optional_fields(console):
    """Test game with minimal data."""
    game = MmoOnlineGameInfo(
        title="Minimal MMO",
        game_summary="Basic MMO",
        core_loop="Play online",
    )
    game.render(console)
    facts = dict(game._fact_pairs())
    assert facts["Peak CCU"] == "-"


def test_mmo_online_roundtrip():
    """Test serialization roundtrip."""
    original = MmoOnlineGameInfo(
        title="Roundtrip MMO",
        game_summary="Testing serialization",
        core_loop="test -> verify",
        release_year=2024,
        peak_concurrency_target=100000,
        operations_cadence="Weekly",
    )
    data = original.to_dict()
    restored = MmoOnlineGameInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.peak_concurrency_target == original.peak_concurrency_target
    assert restored.operations_cadence == original.operations_cadence


def test_server_architecture_profile_table_schema():
    """Test ServerArchitectureProfile has table schema."""
    schema = ServerArchitectureProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Architecture" in headers


def test_endgame_activity_profile_table_schema():
    """Test EndgameActivityProfile has table schema."""
    schema = EndgameActivityProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Activity" in headers


def test_community_program_profile_table_schema():
    """Test CommunityProgramProfile has table schema."""
    schema = CommunityProgramProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Program" in headers
