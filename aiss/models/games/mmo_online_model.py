"""MMO and Online Service game format model."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    EconomyLoopInfo,
    GameFormatBase,
    GameJsonModel,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    NarrativeBeatInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    SocialFeatureInfo,
    StudioProfile,
)

instructions = "Summarise an MMO or persistent online game as a live service director. Outline world structure, social systems, endgame loops, monetisation pillars, and operations cadence. Highlight server architecture, matchmaking, competitive ladders, community programs, and retention levers."


class ServerArchitectureProfile(GameJsonModel):
    """Server or shard architecture details."""

    name: str = Field("", description="Server architecture or shard name")
    capacity: str = Field("", description="Player capacity or concurrency targets")
    matchmaking_scope: str = Field("", description="Scope of matchmaking or instancing")
    region_support: str = Field("", description="Region or localisation coverage")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Architecture", style="magenta"),
            TableSchema(name="capacity", header="Capacity", style="cyan"),
            TableSchema(name="matchmaking_scope", header="Matchmaking", style="yellow"),
            TableSchema(name="region_support", header="Regions"),
        ]


class EndgameActivityProfile(GameJsonModel):
    """Endgame loop or pinnacle activity."""

    activity_name: str = Field("", description="Activity or mode name")
    description: str = Field("", description="Summary of experience")
    recommended_team: str = Field("", description="Recommended team size or composition")
    rewards: list[str] = Field(default_factory=list, description="Reward highlights")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="activity_name", header="Activity", style="magenta"),
            TableSchema(name="description", header="Description", style="cyan"),
            TableSchema(name="recommended_team", header="Team", style="yellow"),
        ]


class CommunityProgramProfile(GameJsonModel):
    """Community or creator program."""

    program_name: str = Field("", description="Program name")
    focus: str = Field("", description="Focus (creators, community events, esports)")
    cadence: str = Field("", description="Cadence or duration")
    incentives: list[str] = Field(default_factory=list, description="Incentives or rewards")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="program_name", header="Program", style="magenta"),
            TableSchema(name="focus", header="Focus", style="cyan"),
            TableSchema(name="cadence", header="Cadence", style="yellow"),
        ]


class MmoOnlineGameInfo(GameFormatBase):
    """MMO and persistent online genre format."""

    model_name: ClassVar[str] = "MmoOnlineGameInfo"
    description: ClassVar[str] = "MMO and persistent online game model focusing on operations, social systems, and endgame activities."
    key_trait: ClassVar[str] = "Always-on world with layered social, progression, and live operations"

    summary_title_fallback: ClassVar[str] = "MMO / Online Service Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="World overview and positioning")
    core_loop: str = Field("", description="Primary loop (quest, raid, compete)")
    world_structure: str = Field("", description="World structure and instancing")
    social_vision: str = Field("", description="Social experience vision")
    operations_cadence: str = Field("", description="Cadence for patches, seasons, or expansions")
    monetisation_pillars: str = Field("", description="Monetisation pillars (subs, season pass, cosmetics)")
    retention_levers: str = Field("", description="Key retention levers")
    release_year: int = Field(0, description="Launch year")
    peak_concurrency_target: int = Field(0, description="Peak concurrent players target")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development studios")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform releases")
    server_architecture: list[ServerArchitectureProfile] = Field(default_factory=list, description="Server architecture")
    social_features: list[SocialFeatureInfo] = Field(default_factory=list, description="Social systems")
    mechanics: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Key mechanics")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression systems")
    economy_loops: list[EconomyLoopInfo] = Field(default_factory=list, description="Economy loops")
    endgame_activities: list[EndgameActivityProfile] = Field(default_factory=list, description="Endgame activities")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live events")
    community_programs: list[CommunityProgramProfile] = Field(default_factory=list, description="Community programs")
    narrative_beats: list[NarrativeBeatInfo] = Field(default_factory=list, description="Narrative beats")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility features")
    audio_design: list[AudioDesignCue] = Field(default_factory=list, description="Audio design cues")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Provide an MMO or persistent online service overview for '" + name + "', covering world structure, social systems, operations cadence, monetisation pillars, and endgame activities."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys like title, game_summary, core_loop, world_structure, social_vision, operations_cadence, monetisation_pillars, "
            "retention_levers, release_year, peak_concurrency_target, developers, publishers, platform_releases, server_architecture, social_features, mechanics, "
            "progression_tracks, economy_loops, endgame_activities, live_events, community_programs, narrative_beats, accessibility_features, audio_design."
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
            (
                "Peak CCU",
                format_number(self.peak_concurrency_target) if self.peak_concurrency_target else "-",
            ),
            ("Operations", self.operations_cadence or "-"),
            ("Monetisation", self.monetisation_pillars or "-"),
            ("Retention", self.retention_levers or "-"),
        ]

    def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence]]:
        sections: list[tuple[str, List[TableSchema], Sequence]] = []
        if self.developers:
            sections.append(("Developers", StudioProfile.table_schema(), self.developers))
        if self.publishers:
            sections.append(("Publishers", StudioProfile.table_schema(), self.publishers))
        if self.platform_releases:
            sections.append(("Platform Releases", PlatformReleaseInfo.table_schema(), self.platform_releases))
        if self.server_architecture:
            sections.append(("Server Architecture", ServerArchitectureProfile.table_schema(), self.server_architecture))
        if self.social_features:
            sections.append(("Social Systems", SocialFeatureInfo.table_schema(), self.social_features))
        if self.mechanics:
            sections.append(("Mechanics", GameplayMechanicHighlight.table_schema(), self.mechanics))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.economy_loops:
            sections.append(("Economy", EconomyLoopInfo.table_schema(), self.economy_loops))
        if self.endgame_activities:
            sections.append(("Endgame", EndgameActivityProfile.table_schema(), self.endgame_activities))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.community_programs:
            sections.append(("Community Programs", CommunityProgramProfile.table_schema(), self.community_programs))
        if self.narrative_beats:
            sections.append(("Narrative", NarrativeBeatInfo.table_schema(), self.narrative_beats))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.audio_design:
            sections.append(("Audio Design", AudioDesignCue.table_schema(), self.audio_design))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        operations_panel = "\n".join(
            filter(
                None,
                (
                    f"World Structure: {self.world_structure}" if self.world_structure else "",
                    f"Operations: {self.operations_cadence}" if self.operations_cadence else "",
                ),
            )
        )
        social_panel = "\n".join(
            filter(
                None,
                (
                    f"Social Vision: {self.social_vision}" if self.social_vision else "",
                    f"Community: {self.retention_levers}" if self.retention_levers else "",
                ),
            )
        )
        return [
            ("Operations", operations_panel, "cyan"),
            ("Community", social_panel, "magenta"),
        ]


__all__ = [
    "MmoOnlineGameInfo",
    "ServerArchitectureProfile",
    "EndgameActivityProfile",
    "CommunityProgramProfile",
]
