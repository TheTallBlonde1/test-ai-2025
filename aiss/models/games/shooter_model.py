"""Shooter (FPS / TPS) game format model."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_runtime_minutes, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AccessibilityFeatureInfo,
    EconomyModelInfo,
    EsportsEventInfo,
    GameFormatBase,
    GameJsonModel,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    MultiplayerModeInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    SessionProfileInfo,
    StudioProfile,
    TechnicalBenchmarkInfo,
)

instructions = (
    "Adopt the lens of a competitive shooter product lead preparing a pitch deck. "
    "Explain the gunplay vision, movement tech, map philosophy, competitive rules, and service roadmap. "
    "Clarify platform releases, economy plans, anti-cheat posture, and esports aspirations so stakeholders grasp the shooter’s lifecycle."
)


class WeaponArchetypeInfo(GameJsonModel):
    """Weapon archetype with handling notes."""

    name: str = Field("", description="Weapon archetype name")
    role: str = Field("", description="Intended gameplay role")
    fire_rate_profile: str = Field("", description="Fire rate or burst cadence")
    optimal_range: str = Field("", description="Best engagement range")
    skill_ceiling: str = Field("", description="Mastery requirement or difficulty")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Weapon", style="magenta"),
            TableSchema(name="role", header="Role", style="cyan"),
            TableSchema(name="optimal_range", header="Range", style="yellow"),
            TableSchema(name="skill_ceiling", header="Skill Ceiling"),
        ]


class MapRotationInfo(GameJsonModel):
    """Playable map or battleground descriptor."""

    map_name: str = Field("", description="Map name")
    environment: str = Field("", description="Environment or biome")
    layout_identity: str = Field("", description="Layout identity (three-lane, arena, large-scale)")
    mode_alignment: list[str] = Field(default_factory=list, description="Supported modes")
    callouts: list[str] = Field(default_factory=list, description="Key areas or callouts")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="map_name", header="Map", style="magenta"),
            TableSchema(name="environment", header="Environment", style="cyan"),
            TableSchema(name="layout_identity", header="Layout", style="yellow"),
            TableSchema(name="mode_alignment", header="Modes"),
        ]


class ShooterGameInfo(GameFormatBase):
    """Shooter-specific format with competitive emphasis."""

    model_name: ClassVar[str] = "ShooterGameInfo"
    description: ClassVar[str] = "Shooter genre model articulating gunplay pillars, map rotation, competitive structure, and live service rhythm."
    key_trait: ClassVar[str] = "Precision gunplay married with fast tactical decision-making"

    summary_title_fallback: ClassVar[str] = "Shooter Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="Framing narrative or setting context")
    core_loop: str = Field("", description="Primary loop (engage, reposition, secure objective)")
    combat_philosophy: str = Field("", description="Gunplay feel and time-to-kill philosophy")
    movement_signature: str = Field("", description="Traversal systems and high-skill expression")
    player_perspective: str = Field("", description="Perspective (first-person, third-person, hybrid)")
    release_year: int = Field(0, description="Launch year")
    match_length_minutes: int = Field(0, description="Average match length in minutes")
    netcode_strategy: str = Field("", description="Server architecture and tick-rate goals")
    anti_cheat_approach: str = Field("", description="Anti-cheat tooling or partnerships")
    crossplay_support: bool = Field(False, description="Whether crossplay is enabled")
    ranked_focus: str = Field("", description="Ranked philosophy and unlock pacing")
    monetisation_model: str = Field("", description="Free-to-play, premium, battle pass cadence")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development partners")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform release plan")
    weapon_archetypes: list[WeaponArchetypeInfo] = Field(default_factory=list, description="Weapon archetypes")
    gameplay_pillars: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Signature gunplay or systems")
    map_rotation: list[MapRotationInfo] = Field(default_factory=list, description="Map roster")
    multiplayer_modes: list[MultiplayerModeInfo] = Field(default_factory=list, description="Playable modes")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression and mastery systems")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live service beats")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility support")
    economy_models: list[EconomyModelInfo] = Field(default_factory=list, description="Economy/monetisation layers")
    esports_events: list[EsportsEventInfo] = Field(default_factory=list, description="Esports initiatives")
    technical_benchmarks: list[TechnicalBenchmarkInfo] = Field(default_factory=list, description="Performance benchmarks")
    session_profiles: list[SessionProfileInfo] = Field(default_factory=list, description="Average play session shapes")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return (
            "Compile a shooter genre production brief for '"
            + name
            + "', detailing gunplay goals, movement tech, map rotation, multiplayer modes, monetisation, and competitive aspirations."
        )

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions
            + "\nOUTPUT FORMAT:\nReturn JSON with keys such as title, game_summary, core_loop, combat_philosophy, movement_signature, player_perspective, release_year, "
            "match_length_minutes, netcode_strategy, anti_cheat_approach, crossplay_support, ranked_focus, monetisation_model, developers, publishers, platform_releases, "
            "weapon_archetypes, gameplay_pillars, map_rotation, multiplayer_modes, progression_tracks, live_events, accessibility_features, economy_models, esports_events, "
            "technical_benchmarks, session_profiles."
        )

    def _summary_panel(self) -> tuple[str, Sequence[str], str]:
        title = self.title or self.summary_title_fallback
        lines = [line for line in (self.core_loop, self.game_summary) if isinstance(line, str) and line.strip()]
        if not lines:
            lines.append("(no summary provided)")
        return title, lines, self.summary_panel_style

    def _fact_pairs(self) -> Sequence[tuple[str, str]]:
        return [
            ("Release Year", format_year(self.release_year)),
            ("Perspective", self.player_perspective or "-"),
            ("Match Length", format_runtime_minutes(self.match_length_minutes) if self.match_length_minutes else "-"),
            ("Crossplay", "Enabled" if self.crossplay_support else "Unavailable"),
            ("Netcode", self.netcode_strategy or "-"),
            ("Anti-Cheat", self.anti_cheat_approach or "-"),
            ("Ranked", self.ranked_focus or "-"),
            ("Monetisation", self.monetisation_model or "-"),
        ]

    def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence]]:
        sections: list[tuple[str, List[TableSchema], Sequence]] = []
        if self.developers:
            sections.append(("Developers", StudioProfile.table_schema(), self.developers))
        if self.publishers:
            sections.append(("Publishers", StudioProfile.table_schema(), self.publishers))
        if self.platform_releases:
            sections.append(("Platform Releases", PlatformReleaseInfo.table_schema(), self.platform_releases))
        if self.weapon_archetypes:
            sections.append(("Weapon Archetypes", WeaponArchetypeInfo.table_schema(), self.weapon_archetypes))
        if self.gameplay_pillars:
            sections.append(("Gameplay Pillars", GameplayMechanicHighlight.table_schema(), self.gameplay_pillars))
        if self.map_rotation:
            sections.append(("Map Pool", MapRotationInfo.table_schema(), self.map_rotation))
        if self.multiplayer_modes:
            sections.append(("Multiplayer Modes", MultiplayerModeInfo.table_schema(), self.multiplayer_modes))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.economy_models:
            sections.append(("Economy", EconomyModelInfo.table_schema(), self.economy_models))
        if self.esports_events:
            sections.append(("Esports", EsportsEventInfo.table_schema(), self.esports_events))
        if self.technical_benchmarks:
            sections.append(("Tech Benchmarks", TechnicalBenchmarkInfo.table_schema(), self.technical_benchmarks))
        if self.session_profiles:
            sections.append(("Player Sessions", SessionProfileInfo.table_schema(), self.session_profiles))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        combat_panel_lines = []
        if self.combat_philosophy:
            combat_panel_lines.append(f"Gunplay: {self.combat_philosophy}")
        if self.movement_signature:
            combat_panel_lines.append(f"Movement: {self.movement_signature}")
        combat_panel = "\n".join(combat_panel_lines)

        service_lines = []
        if self.ranked_focus:
            service_lines.append(f"Ranked: {self.ranked_focus}")
        if self.monetisation_model:
            service_lines.append(f"Economy: {self.monetisation_model}")
        service_panel = "\n".join(service_lines)

        return [
            ("Combat & Movement", combat_panel, "cyan"),
            ("Service Overview", service_panel, "magenta"),
        ]


__all__ = ["ShooterGameInfo", "WeaponArchetypeInfo", "MapRotationInfo"]
