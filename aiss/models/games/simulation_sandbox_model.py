"""Simulation and Sandbox game format model."""

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
    StudioProfile,
)

instructions = "Summarise a simulation or sandbox game as a systems design director. Describe simulation depth, player authored creativity, systemic interactions, and technical constraints. Highlight progression, economy loops, creator tools, live updates, and how players share or monetise creations."


class SimulationSystemProfile(GameJsonModel):
    """Key simulation system or rule set."""

    name: str = Field("", description="System name (eg. weather, AI, physics)")
    scope: str = Field("", description="Scope or coverage of the simulation")
    fidelity: str = Field("", description="Level of accuracy or granularity")
    player_influence: str = Field("", description="How players interact or influence it")
    emergent_outcomes: list[str] = Field(default_factory=list, description="Notable emergent outcomes")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="System", style="magenta"),
            TableSchema(name="scope", header="Scope", style="cyan"),
            TableSchema(name="fidelity", header="Fidelity", style="yellow"),
            TableSchema(name="player_influence", header="Player Influence"),
        ]


class CreatorToolProfile(GameJsonModel):
    """User generated content tool or pipeline."""

    tool_name: str = Field("", description="Tool or editor name")
    capabilities: str = Field("", description="What the tool enables")
    access_level: str = Field("", description="Who can access it (core loop, advanced, external)")
    sharing_channel: str = Field("", description="How creations are shared")
    monetisation: str = Field("", description="Monetisation options if any")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="tool_name", header="Tool", style="magenta"),
            TableSchema(name="capabilities", header="Capabilities", style="cyan"),
            TableSchema(name="access_level", header="Access", style="yellow"),
            TableSchema(name="sharing_channel", header="Sharing"),
            TableSchema(name="monetisation", header="Monetisation"),
        ]


class SimulationSandboxGameInfo(GameFormatBase):
    """Simulation/Sandbox genre format."""

    model_name: ClassVar[str] = "SimulationSandboxGameInfo"
    description: ClassVar[str] = "Simulation and sandbox game model focusing on systemic depth, creation tools, and player-driven stories."
    key_trait: ClassVar[str] = "Player-authored creativity layered on deep systemic simulation"

    summary_title_fallback: ClassVar[str] = "Simulation / Sandbox Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="High level concept and fantasy")
    core_loop: str = Field("", description="Primary loop for creation, management, or experimentation")
    simulation_scope: str = Field("", description="Scope of simulation (city, life, ecosystem, physics)")
    player_authorship: str = Field("", description="How players shape the world or content")
    tech_constraints: str = Field("", description="Key technical constraints or systems limits")
    release_year: int = Field(0, description="Initial release year")
    average_session_minutes: float = Field(0.0, description="Typical session length in minutes")
    sharing_infrastructure: str = Field("", description="Infrastructure for sharing creations")
    monetisation_model: str = Field("", description="Monetisation approach")
    live_update_cadence: str = Field("", description="Cadence of updates or expansions")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development studios")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform support")
    simulation_systems: list[SimulationSystemProfile] = Field(default_factory=list, description="Core systems")
    creator_tools: list[CreatorToolProfile] = Field(default_factory=list, description="Creation tools")
    mechanics: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Key mechanics")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression or unlock paths")
    economy_loops: list[EconomyLoopInfo] = Field(default_factory=list, description="Economy loops")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live events or seasons")
    narrative_beats: list[NarrativeBeatInfo] = Field(default_factory=list, description="Signature player stories or missions")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility support")
    audio_design: list[AudioDesignCue] = Field(default_factory=list, description="Audio and ambience highlights")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Provide a simulation and sandbox overview for '" + name + "', detailing systemic depth, creation tools, progression, economies, sharing infrastructure, and live update plans."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys like title, game_summary, core_loop, simulation_scope, player_authorship, tech_constraints, release_year, "
            "average_session_minutes, sharing_infrastructure, monetisation_model, live_update_cadence, developers, publishers, platform_releases, simulation_systems, "
            "creator_tools, mechanics, progression_tracks, economy_loops, live_events, narrative_beats, accessibility_features, audio_design."
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
                "Session Length",
                format_number(self.average_session_minutes) + " min" if self.average_session_minutes else "-",
            ),
            ("Player Authorship", self.player_authorship or "-"),
            ("Sharing", self.sharing_infrastructure or "-"),
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
        if self.simulation_systems:
            sections.append(("Simulation Systems", SimulationSystemProfile.table_schema(), self.simulation_systems))
        if self.creator_tools:
            sections.append(("Creator Tools", CreatorToolProfile.table_schema(), self.creator_tools))
        if self.mechanics:
            sections.append(("Mechanics", GameplayMechanicHighlight.table_schema(), self.mechanics))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.economy_loops:
            sections.append(("Economy Loops", EconomyLoopInfo.table_schema(), self.economy_loops))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.narrative_beats:
            sections.append(("Narrative Moments", NarrativeBeatInfo.table_schema(), self.narrative_beats))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.audio_design:
            sections.append(("Audio Design", AudioDesignCue.table_schema(), self.audio_design))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        systems_panel = "\n".join(
            filter(
                None,
                (
                    f"Simulation Scope: {self.simulation_scope}" if self.simulation_scope else "",
                    f"Tech Constraints: {self.tech_constraints}" if self.tech_constraints else "",
                    f"Live Cadence: {self.live_update_cadence}" if self.live_update_cadence else "",
                ),
            )
        )
        creation_panel = "\n".join(
            filter(
                None,
                (
                    f"Authorship: {self.player_authorship}" if self.player_authorship else "",
                    f"Sharing: {self.sharing_infrastructure}" if self.sharing_infrastructure else "",
                ),
            )
        )
        return [
            ("Systems", systems_panel, "cyan"),
            ("Player Creation", creation_panel, "magenta"),
        ]


__all__ = [
    "SimulationSandboxGameInfo",
    "SimulationSystemProfile",
    "CreatorToolProfile",
]
