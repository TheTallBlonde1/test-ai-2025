"""Horror and Survival game format model."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    GameFormatBase,
    GameJsonModel,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    NarrativeBeatInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
)

instructions = "Summarise a horror or survival game as a fear architect. Explain tone, threats, survival resource tension, pacing, and how players manage vulnerability. Include level or scenario structure, co-op support, live updates, monetisation, and accessibility for scares."


class ThreatProfile(GameJsonModel):
    """Primary threat or antagonist archetype."""

    name: str = Field("", description="Threat name")
    behaviour: str = Field("", description="Behaviour pattern")
    escalation: str = Field("", description="How threat escalates")
    counterplay: str = Field("", description="Counterplay or survival strategy")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Threat", style="magenta"),
            TableSchema(name="behaviour", header="Behaviour", style="cyan"),
            TableSchema(name="escalation", header="Escalation", style="yellow"),
            TableSchema(name="counterplay", header="Counterplay"),
        ]


class SurvivalResourceProfile(GameJsonModel):
    """Critical survival resource or crafting loop."""

    resource_name: str = Field("", description="Resource name")
    scarcity_model: str = Field("", description="Scarcity model or availability")
    acquisition_method: str = Field("", description="How players acquire it")
    usage_pressure: str = Field("", description="Consumption pressure or trade-offs")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="resource_name", header="Resource", style="magenta"),
            TableSchema(name="scarcity_model", header="Scarcity", style="cyan"),
            TableSchema(name="acquisition_method", header="Acquisition", style="yellow"),
            TableSchema(name="usage_pressure", header="Pressure"),
        ]


class ScenarioStructureProfile(GameJsonModel):
    """Mission, chapter, or scenario structure element."""

    scenario_name: str = Field("", description="Scenario or level name")
    objective: str = Field("", description="Primary objective or puzzle")
    tension_curve: str = Field("", description="How tension ramps")
    coop_support: str = Field("", description="Co-op support or player count")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="scenario_name", header="Scenario", style="magenta"),
            TableSchema(name="objective", header="Objective", style="cyan"),
            TableSchema(name="tension_curve", header="Tension", style="yellow"),
            TableSchema(name="coop_support", header="Co-op"),
        ]


class HorrorSurvivalGameInfo(GameFormatBase):
    """Horror and survival genre format."""

    model_name: ClassVar[str] = "HorrorSurvivalGameInfo"
    description: ClassVar[str] = "Horror and survival game model emphasising tension, resource scarcity, and fear delivery systems."
    key_trait: ClassVar[str] = "Sustained dread with deliberate vulnerability management"

    summary_title_fallback: ClassVar[str] = "Horror / Survival Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="Tone and hook")
    core_loop: str = Field("", description="Loop (scavenge, survive, escape)")
    horror_subgenre: str = Field("", description="Subgenre such as cosmic, psychological, survival horror")
    threat_design_philosophy: str = Field("", description="Approach to threat design")
    tension_delivery: str = Field("", description="How tension and scares are delivered")
    vulnerability_model: str = Field("", description="How player vulnerability is managed")
    monetisation_model: str = Field("", description="Monetisation approach")
    live_update_strategy: str = Field("", description="Strategy for post-launch content")
    release_year: int = Field(0, description="Initial release year")
    average_session_minutes: float = Field(0.0, description="Average session length")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development studios")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform timeline")
    threats: list[ThreatProfile] = Field(default_factory=list, description="Threat roster")
    survival_resources: list[SurvivalResourceProfile] = Field(default_factory=list, description="Survival resources")
    scenarios: list[ScenarioStructureProfile] = Field(default_factory=list, description="Scenario structure")
    mechanics: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Key mechanics")
    narrative_beats: list[NarrativeBeatInfo] = Field(default_factory=list, description="Narrative beats")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression systems")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live events")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility for scares")
    audio_design: list[AudioDesignCue] = Field(default_factory=list, description="Audio and sound design cues")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Provide a horror or survival blueprint for '" + name + "', detailing threats, resource tension, scenarios, co-op, monetisation, and live update strategy."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys like title, game_summary, core_loop, horror_subgenre, threat_design_philosophy, tension_delivery, "
            "vulnerability_model, monetisation_model, live_update_strategy, release_year, average_session_minutes, developers, publishers, platform_releases, threats, "
            "survival_resources, scenarios, mechanics, narrative_beats, progression_tracks, live_events, accessibility_features, audio_design."
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
            ("Subgenre", self.horror_subgenre or "-"),
            ("Tension Delivery", self.tension_delivery or "-"),
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
        if self.threats:
            sections.append(("Threats", ThreatProfile.table_schema(), self.threats))
        if self.survival_resources:
            sections.append(("Resources", SurvivalResourceProfile.table_schema(), self.survival_resources))
        if self.scenarios:
            sections.append(("Scenarios", ScenarioStructureProfile.table_schema(), self.scenarios))
        if self.mechanics:
            sections.append(("Mechanics", GameplayMechanicHighlight.table_schema(), self.mechanics))
        if self.narrative_beats:
            sections.append(("Narrative", NarrativeBeatInfo.table_schema(), self.narrative_beats))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.audio_design:
            sections.append(("Audio Design", AudioDesignCue.table_schema(), self.audio_design))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        dread_panel = "\n".join(
            filter(
                None,
                (
                    f"Threat Philosophy: {self.threat_design_philosophy}" if self.threat_design_philosophy else "",
                    f"Vulnerability: {self.vulnerability_model}" if self.vulnerability_model else "",
                ),
            )
        )
        survival_panel = "\n".join(
            filter(
                None,
                (
                    f"Subgenre: {self.horror_subgenre}" if self.horror_subgenre else "",
                    f"Live Strategy: {self.live_update_strategy}" if self.live_update_strategy else "",
                ),
            )
        )
        return [
            ("Fear Design", dread_panel, "cyan"),
            ("Survival Plan", survival_panel, "magenta"),
        ]


__all__ = [
    "HorrorSurvivalGameInfo",
    "ThreatProfile",
    "SurvivalResourceProfile",
    "ScenarioStructureProfile",
]
