"""Action / Adventure game format model."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    GameFormatBase,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    NarrativeBeatInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
    TechnicalBenchmarkInfo,
)

instructions = (
    "Act as a franchise creative director compiling an executive briefing for an action-adventure video game. "
    "Detail the playable hero, world exploration structure, combat pillars, puzzle cadence, and how progression layers sustain player agency. "
    "Highlight signature mechanics, quest arcs, platform release nuances, accessibility support, and technical performance notes so the project feels production-ready."
)


class ActionAdventureGameInfo(GameFormatBase):
    """Game format capturing action-adventure staples."""

    model_name: ClassVar[str] = "ActionAdventureGameInfo"
    description: ClassVar[str] = "Hybrid combat, traversal, and exploration video game model focused on authored narratives and environmental discovery."
    key_trait: ClassVar[str] = "Quest-driven adventure with tactile combat and world exploration"

    summary_title_fallback: ClassVar[str] = "Action / Adventure Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="Expanded overview of the campaign and player fantasy")
    core_loop: str = Field("", description="Core gameplay loop expressed as verbs or player goals")
    world_setting: str = Field("", description="Primary setting or universe description")
    hero_profile: str = Field("", description="Lead character traits and motivations")
    camera_perspective: str = Field("", description="Camera style (third-person, isometric, side-scrolling)")
    release_year: int = Field(0, description="Initial release year")
    average_completion_hours: float = Field(0.0, description="Average hours to finish the critical path")
    completionist_hours: float = Field(0.0, description="Average hours to complete all optional content")
    exploration_focus: str = Field("", description="Structure of exploration (open world, hub-and-spoke, linear)")
    combat_identity: list[str] = Field(default_factory=list, description="Combat pillars or inspirations")
    puzzle_integrations: list[str] = Field(default_factory=list, description="Puzzle types interwoven with progression")
    difficulty_modes: list[str] = Field(default_factory=list, description="Difficulty options and assist modifiers")
    monetisation_model: str = Field("", description="Monetisation approach (premium, DLC cadence, cosmetics)")
    endgame_structure: str = Field("", description="What players pursue post-credits")
    player_agency_features: list[str] = Field(default_factory=list, description="Systems that empower player choice")
    platforms: list[str] = Field(default_factory=list, description="Primary platforms or ecosystems")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development partners")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform-specific release details")
    signature_mechanics: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Signature mechanics or systems")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression layers")
    narrative_beats: list[NarrativeBeatInfo] = Field(default_factory=list, description="Key narrative beats or quest arcs")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live events or DLC beats")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility support summary")
    technical_benchmarks: list[TechnicalBenchmarkInfo] = Field(default_factory=list, description="Performance benchmarks")
    audio_design: list[AudioDesignCue] = Field(default_factory=list, description="Audio design highlights")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return (
            "Develop a full action-adventure executive brief for '"
            + name
            +"', covering world identity, hero journey, combat and exploration pillars, and how progression plus live content sustain players."
        )

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions
            + "\nOUTPUT FORMAT:\nReturn JSON with keys such as title, game_summary, core_loop, world_setting, hero_profile, camera_perspective, release_year, "
            "average_completion_hours, completionist_hours, exploration_focus, combat_identity, puzzle_integrations, difficulty_modes, monetisation_model, "
            "endgame_structure, player_agency_features, platforms, developers, publishers, platform_releases, signature_mechanics, progression_tracks, "
            "narrative_beats, live_events, accessibility_features, technical_benchmarks, audio_design."
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
            ("Completion (hrs)", format_number(self.average_completion_hours) if self.average_completion_hours else "-"),
            (
                "Completionist",
                format_number(self.completionist_hours) if self.completionist_hours else "-",
            ),
            ("Exploration", ", ".join(self.exploration_focus.split(";")) if self.exploration_focus else "-"),
            ("Combat", ", ".join(self.combat_identity) if self.combat_identity else "-"),
            ("Difficulty", ", ".join(self.difficulty_modes) if self.difficulty_modes else "-"),
            ("Platforms", ", ".join(self.platforms) if self.platforms else "-"),
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
        if self.signature_mechanics:
            sections.append(("Signature Mechanics", GameplayMechanicHighlight.table_schema(), self.signature_mechanics))
        if self.progression_tracks:
            sections.append(("Progression Tracks", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.narrative_beats:
            sections.append(("Narrative Beats", NarrativeBeatInfo.table_schema(), self.narrative_beats))
        if self.live_events:
            sections.append(("Live Content", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.technical_benchmarks:
            sections.append(("Technical Benchmarks", TechnicalBenchmarkInfo.table_schema(), self.technical_benchmarks))
        if self.audio_design:
            sections.append(("Audio Design", AudioDesignCue.table_schema(), self.audio_design))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        world_details = []
        if self.world_setting:
            world_details.append(f"Setting: {self.world_setting}")
        if self.hero_profile:
            world_details.append(f"Hero: {self.hero_profile}")
        if self.player_agency_features:
            world_details.append("Agency: " + ", ".join(self.player_agency_features))
        if self.puzzle_integrations:
            world_details.append("Puzzle Types: " + ", ".join(self.puzzle_integrations))
        world_panel = "\n".join(world_details)

        endgame_panel = self.endgame_structure.strip() if self.endgame_structure else ""

        return [
            ("World & Protagonist", world_panel, "cyan"),
            ("Endgame Loop", endgame_panel, "magenta"),
        ]


__all__ = ["ActionAdventureGameInfo"]
