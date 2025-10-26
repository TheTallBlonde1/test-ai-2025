"""Sports and Racing game format model."""

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
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
)

instructions = "Summarise a sports or racing game like a franchise executive. Detail league licences, athlete or vehicle rosters, season cadence, live competitions, and monetisation programs. Explain physics fidelity, skill gaps, accessibility, online infrastructure, and community broadcast hooks."


class LeagueLicenseProfile(GameJsonModel):
    """League or competition license."""

    name: str = Field("", description="League or competition name")
    scope: str = Field("", description="Scope (regional, global, historic)")
    format_overview: str = Field("", description="Format of competition")
    renewal_term: str = Field("", description="License term or renewal notes")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="League", style="magenta"),
            TableSchema(name="scope", header="Scope", style="cyan"),
            TableSchema(name="format_overview", header="Format", style="yellow"),
            TableSchema(name="renewal_term", header="Renewal"),
        ]


class AthleteVehicleProfile(GameJsonModel):
    """Athlete, team, or vehicle roster entry."""

    name: str = Field("", description="Athlete, team, or vehicle name")
    classification: str = Field("", description="Role, class, or series")
    headline_rating: str = Field("", description="Headline rating or stat")
    signature_strength: str = Field("", description="Signature strength or trait")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(name="classification", header="Class", style="cyan"),
            TableSchema(name="headline_rating", header="Rating", style="yellow"),
            TableSchema(name="signature_strength", header="Signature"),
        ]


class SportsModeProfile(GameJsonModel):
    """Core game mode or season experience."""

    mode_name: str = Field("", description="Mode name")
    structure: str = Field("", description="Structure (season, bracket, career)")
    key_features: list[str] = Field(default_factory=list, description="Notable features")
    online_enabled: bool = Field(False, description="Whether online play is supported")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="mode_name", header="Mode", style="magenta"),
            TableSchema(name="structure", header="Structure", style="cyan"),
            TableSchema(name="online_enabled", header="Online"),
        ]


class SportsRacingGameInfo(GameFormatBase):
    """Sports and racing genre format."""

    model_name: ClassVar[str] = "SportsRacingGameInfo"
    description: ClassVar[str] = "Sports and racing game model covering licences, rosters, physics, and live service cadence."
    key_trait: ClassVar[str] = "Authentic competition blended with live content and monetisation programs"

    summary_title_fallback: ClassVar[str] = "Sports / Racing Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="High-level positioning")
    core_loop: str = Field("", description="Loop such as race, upgrade, compete, broadcast")
    sport_focus: str = Field("", description="Sport or racing discipline focus")
    licence_strategy: str = Field("", description="Strategy for licences or athlete rights")
    physics_fidelity: str = Field("", description="Level of physics simulation")
    skill_gap_statement: str = Field("", description="Positioning on skill gap and coaching")
    broadcast_hooks: str = Field("", description="Presentation and broadcast features")
    monetisation_model: str = Field("", description="Monetisation approach")
    live_season_plan: str = Field("", description="Season cadence or live program")
    release_year: int = Field(0, description="Initial release year")
    average_match_minutes: float = Field(0.0, description="Average match or race length")

    developers: list[StudioProfile] = Field(default_factory=list, description="Developers")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishers")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platforms")
    league_licenses: list[LeagueLicenseProfile] = Field(default_factory=list, description="League licences")
    roster: list[AthleteVehicleProfile] = Field(default_factory=list, description="Roster entries")
    modes: list[SportsModeProfile] = Field(default_factory=list, description="Game modes")
    mechanics: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Core mechanics")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression systems")
    economy_loops: list[EconomyLoopInfo] = Field(default_factory=list, description="Economy loops")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live events or competitions")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility features")
    audio_design: list[AudioDesignCue] = Field(default_factory=list, description="Audio and crowd presentation")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Provide a sports or racing franchise overview for '" + name + "', covering licences, roster depth, modes, physics, monetisation, live seasons, and broadcast hooks."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys like title, game_summary, core_loop, sport_focus, licence_strategy, physics_fidelity, skill_gap_statement, "
            "broadcast_hooks, monetisation_model, live_season_plan, release_year, average_match_minutes, developers, publishers, platform_releases, league_licenses, roster, "
            "modes, mechanics, progression_tracks, economy_loops, live_events, accessibility_features, audio_design."
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
                "Match Length",
                format_number(self.average_match_minutes) + " min" if self.average_match_minutes else "-",
            ),
            ("Licence Strategy", self.licence_strategy or "-"),
            ("Physics", self.physics_fidelity or "-"),
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
        if self.league_licenses:
            sections.append(("Licences", LeagueLicenseProfile.table_schema(), self.league_licenses))
        if self.roster:
            sections.append(("Roster", AthleteVehicleProfile.table_schema(), self.roster))
        if self.modes:
            sections.append(("Modes", SportsModeProfile.table_schema(), self.modes))
        if self.mechanics:
            sections.append(("Mechanics", GameplayMechanicHighlight.table_schema(), self.mechanics))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.economy_loops:
            sections.append(("Economy", EconomyLoopInfo.table_schema(), self.economy_loops))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.audio_design:
            sections.append(("Audio Design", AudioDesignCue.table_schema(), self.audio_design))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        competition_panel = "\n".join(
            filter(
                None,
                (
                    f"Sport Focus: {self.sport_focus}" if self.sport_focus else "",
                    f"Live Season: {self.live_season_plan}" if self.live_season_plan else "",
                    f"Broadcast: {self.broadcast_hooks}" if self.broadcast_hooks else "",
                ),
            )
        )
        skill_panel = "\n".join(
            filter(
                None,
                (
                    f"Skill Gap: {self.skill_gap_statement}" if self.skill_gap_statement else "",
                    f"Physics Fidelity: {self.physics_fidelity}" if self.physics_fidelity else "",
                ),
            )
        )
        return [
            ("Competition", competition_panel, "cyan"),
            ("Skill & Physics", skill_panel, "magenta"),
        ]


__all__ = [
    "SportsRacingGameInfo",
    "LeagueLicenseProfile",
    "AthleteVehicleProfile",
    "SportsModeProfile",
]
