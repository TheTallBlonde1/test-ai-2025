"""Puzzle / Strategy game format model."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AccessibilityFeatureInfo,
    GameFormatBase,
    GameJsonModel,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    SessionProfileInfo,
    StudioProfile,
)

instructions = "Write as a systems designer summarising a puzzle or strategy title for stakeholders. Cover the core ruleset, puzzle escalation, AI sophistication, difficulty tuning, and how players are taught to master systems. Document platform releases, post-launch content, and analytics loops so the product roadmap is clear."


class PuzzleModuleInfo(GameJsonModel):
    """Puzzle module or level pack descriptor."""

    module_name: str = Field("", description="Module or region name")
    challenge_theme: str = Field("", description="Dominant puzzle theme")
    mechanics_introduced: list[str] = Field(default_factory=list, description="Mechanics introduced in the module")
    difficulty_ramp: str = Field("", description="How difficulty scales across the module")
    completion_rate_target: float | None = Field(None, description="Target completion percentage")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="module_name", header="Module", style="magenta"),
            TableSchema(name="challenge_theme", header="Theme", style="cyan"),
            TableSchema(name="difficulty_ramp", header="Difficulty Ramp", style="yellow"),
            TableSchema(name="completion_rate_target", header="Target %"),
        ]


class StrategyScenarioInfo(GameJsonModel):
    """Strategy scenario or mission descriptor."""

    scenario_name: str = Field("", description="Scenario name")
    objective: str = Field("", description="Primary objective")
    map_type: str = Field("", description="Map type or topology")
    ai_behaviour_notes: str = Field("", description="AI behaviour or unique scripting")
    turn_limit: int | None = Field(None, description="Turn or timer limit")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="scenario_name", header="Scenario", style="magenta"),
            TableSchema(name="objective", header="Objective", style="cyan"),
            TableSchema(name="map_type", header="Map", style="yellow"),
            TableSchema(name="turn_limit", header="Turn Limit", justify="right", formatter=format_number),
        ]


class TeachingMomentInfo(GameJsonModel):
    """Tutorial or player education moment."""

    beat_name: str = Field("", description="Tutorial beat name")
    learning_goal: str = Field("", description="Skill or concept being taught")
    delivery_method: str = Field("", description="How the instruction is delivered")
    analytics_signal: str = Field("", description="Metric monitored to validate understanding")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="beat_name", header="Beat", style="magenta"),
            TableSchema(name="learning_goal", header="Learning Goal", style="cyan"),
            TableSchema(name="delivery_method", header="Delivery"),
            TableSchema(name="analytics_signal", header="Signal"),
        ]


class PuzzleStrategyGameInfo(GameFormatBase):
    """Puzzle / strategy hybrid game summary."""

    model_name: ClassVar[str] = "PuzzleStrategyGameInfo"
    description: ClassVar[str] = "Cerebral puzzle and strategy game model emphasising rulesets, difficulty curves, and mastery analytics."
    key_trait: ClassVar[str] = "Logic-first gameplay that rewards planning and optimisation"

    summary_title_fallback: ClassVar[str] = "Puzzle / Strategy Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="High-level overview of fantasy and rules")
    core_loop: str = Field("", description="Primary loop (plan, execute, evaluate)")
    ruleset_overview: str = Field("", description="Summary of key rules and win conditions")
    difficulty_philosophy: str = Field("", description="How difficulty escalates and is communicated")
    ai_capabilities: str = Field("", description="AI sophistication or adaptive systems")
    release_year: int = Field(0, description="Initial release year")
    average_session_minutes: int = Field(0, description="Average focused play session")
    target_audience: str = Field("", description="Intended player profile")
    replayability_hooks: list[str] = Field(default_factory=list, description="Hooks driving repeat play")
    monetisation_model: str = Field("", description="Monetisation (premium, DLC packs, cosmetics)")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development partners")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform release plan")
    puzzle_modules: list[PuzzleModuleInfo] = Field(default_factory=list, description="Puzzle module roadmap")
    strategy_scenarios: list[StrategyScenarioInfo] = Field(default_factory=list, description="Strategy scenarios or missions")
    gameplay_layers: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Gameplay systems")
    teaching_moments: list[TeachingMomentInfo] = Field(default_factory=list, description="Tutorial structure")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression systems")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Post-launch content cadence")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility support")
    session_profiles: list[SessionProfileInfo] = Field(default_factory=list, description="Session archetypes")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Prepare a puzzle/strategy production brief for '" + name + "', outlining rulesets, difficulty escalation, AI behaviours, teaching beats, monetisation, and live support."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys such as title, game_summary, core_loop, ruleset_overview, difficulty_philosophy, ai_capabilities, release_year, "
            "average_session_minutes, target_audience, replayability_hooks, monetisation_model, developers, publishers, platform_releases, puzzle_modules, strategy_scenarios, "
            "gameplay_layers, teaching_moments, progression_tracks, live_events, accessibility_features, session_profiles."
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
            ("Session Length", format_number(self.average_session_minutes) + " min" if self.average_session_minutes else "-"),
            ("Difficulty", self.difficulty_philosophy or "-"),
            ("AI", self.ai_capabilities or "-"),
            ("Monetisation", self.monetisation_model or "-"),
            ("Audience", self.target_audience or "-"),
        ]

    def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence]]:
        sections: list[tuple[str, List[TableSchema], Sequence]] = []
        if self.developers:
            sections.append(("Developers", StudioProfile.table_schema(), self.developers))
        if self.publishers:
            sections.append(("Publishers", StudioProfile.table_schema(), self.publishers))
        if self.platform_releases:
            sections.append(("Platform Releases", PlatformReleaseInfo.table_schema(), self.platform_releases))
        if self.puzzle_modules:
            sections.append(("Puzzle Modules", PuzzleModuleInfo.table_schema(), self.puzzle_modules))
        if self.strategy_scenarios:
            sections.append(("Scenarios", StrategyScenarioInfo.table_schema(), self.strategy_scenarios))
        if self.gameplay_layers:
            sections.append(("Gameplay Layers", GameplayMechanicHighlight.table_schema(), self.gameplay_layers))
        if self.teaching_moments:
            sections.append(("Teaching Moments", TeachingMomentInfo.table_schema(), self.teaching_moments))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.session_profiles:
            sections.append(("Session Profiles", SessionProfileInfo.table_schema(), self.session_profiles))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        system_lines = []
        if self.ruleset_overview:
            system_lines.append(f"Rules: {self.ruleset_overview}")
        if self.replayability_hooks:
            system_lines.append("Replay Hooks: " + ", ".join(self.replayability_hooks))
        systems_panel = "\n".join(system_lines)

        difficulty_panel = self.difficulty_philosophy.strip() if self.difficulty_philosophy else ""

        return [
            ("Systems Overview", systems_panel, "cyan"),
            ("Difficulty Philosophy", difficulty_panel, "magenta"),
        ]


__all__ = [
    "PuzzleStrategyGameInfo",
    "PuzzleModuleInfo",
    "StrategyScenarioInfo",
    "TeachingMomentInfo",
]
