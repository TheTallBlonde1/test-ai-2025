"""Shared game model base classes and helpers.

This module mirrors the structure used by the movie and show packages
but tailors the reusable helpers for interactive video game coverage.
Concrete game formats subclass :class:`GameFormatBase` and lean on the
lightweight data classes defined here for consistent table rendering.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar, List, Sequence, TypeVar

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

from aiss.utils import (
    format_money,
    format_number,
    format_runtime_minutes,
    render_table_from_schema,
)

from ..shared import TableSchema

T = TypeVar("T", bound="GameJsonModel")


def _dump_model(instance: BaseModel) -> dict[str, Any]:  # pragma: no cover - simple helper
    try:
        return instance.model_dump()
    except AttributeError:
        return instance.dict()  # type: ignore[call-arg]


class GameJsonModel(BaseModel):
    """Extend Pydantic with JSON convenience helpers for game data."""

    def to_dict(self) -> dict[str, Any]:
        return _dump_model(self)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        return cls(**data)

    @classmethod
    def from_json(cls: type[T], json_file_path: Path | str) -> T:
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


class GameFormatBase(GameJsonModel):
    """Runtime base class for all concrete game formats."""

    summary_title_fallback: ClassVar[str] = "Video Game"
    summary_panel_style: ClassVar[str] = "green"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary", "elevator_pitch")
    facts_panel_title: ClassVar[str] = "Game Snapshot"
    facts_panel_style: ClassVar[str] = "blue"

    wikipedia_summary: str = Field(
        "",
        exclude=True,
        description="Runtime-only hint populated after parsing for richer rendering.",
    )

    def render_wikipedia_summary(self, console: Console) -> None:
        hint_text = self.wikipedia_summary.strip()
        if not hint_text:
            return
        console.print(Panel(hint_text, title="Context", expand=False, style="yellow"))

    def _summary_panel(self) -> tuple[str, Sequence[str], str]:
        title_value = getattr(self, "title", "") or self.summary_title_fallback
        lines: list[str] = []
        for attribute in self.summary_attributes:
            value = getattr(self, attribute, None)
            if isinstance(value, str) and value.strip():
                lines.append(value.strip())
        if not lines:
            fallback = getattr(self, "game_summary", None)
            if isinstance(fallback, str) and fallback.strip():
                lines.append(fallback.strip())
        if not lines:
            lines.append("(no summary provided)")
        return title_value, lines, self.summary_panel_style

    def _fact_pairs(self) -> Sequence[tuple[str, str]]:
        return []

    def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence[GameJsonModel]]]:
        return []

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        return []

    def render(self, console: Console) -> None:
        summary_title, summary_lines, summary_style = self._summary_panel()
        summary_body = "\n\n".join(line for line in summary_lines if line.strip())
        if not summary_body.strip():
            summary_body = "(no summary provided)"
        console.print(Panel(summary_body, title=summary_title, expand=False, style=summary_style))

        self.render_wikipedia_summary(console)

        fact_pairs = list(self._fact_pairs())
        if fact_pairs:
            facts_text = ", ".join(f"{label}: {value}" for label, value in fact_pairs)
            console.print(Panel(facts_text, title=self.facts_panel_title, expand=False, style=self.facts_panel_style))

        for title, schema, rows in self._table_sections():
            if rows:
                render_table_from_schema(title, schema, list(rows), console)

        for panel_title, body, style in self._extra_panels():
            if body:
                console.print(Panel(body, title=panel_title, expand=False, style=style or "cyan"))


class StudioProfile(GameJsonModel):
    """Developer or publishing studio contribution."""

    name: str = Field("", description="Studio name")
    role: str = Field("", description="Role on the project (lead developer, co-development, publisher)")
    headquarters: str = Field("", description="Primary headquarters or region")
    team_size: int | None = Field(None, description="Approximate team size dedicated to this project")
    notable_credits: list[str] = Field(default_factory=list, description="Prior notable releases or franchises")
    technology_stack: list[str] = Field(default_factory=list, description="Key tools, engines, or pipelines used")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Studio", style="magenta", no_wrap=True),
            TableSchema(name="role", header="Role", style="cyan"),
            TableSchema(name="headquarters", header="Region", style="yellow"),
            TableSchema(name="team_size", header="Team Size", justify="right", formatter=format_number),
            TableSchema(name="notable_credits", header="Notable Credits"),
        ]


class PlatformReleaseInfo(GameJsonModel):
    """Platform-specific release details."""

    platform: str = Field("", description="Platform name (console, PC storefront, cloud)")
    release_date: str = Field("", description="Release date or window")
    edition: str = Field("", description="Edition or SKU identifier")
    resolution_target: str = Field("", description="Advertised resolution target")
    frame_rate_target: str = Field("", description="Advertised frame-rate target")
    platform_features: list[str] = Field(default_factory=list, description="Unique platform features supported")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="platform", header="Platform", style="magenta", no_wrap=True),
            TableSchema(name="release_date", header="Release", style="cyan"),
            TableSchema(name="edition", header="Edition", style="yellow"),
            TableSchema(name="resolution_target", header="Resolution"),
            TableSchema(name="frame_rate_target", header="Frame Rate"),
        ]


class GameplayMechanicHighlight(GameJsonModel):
    """Signature gameplay mechanic or system."""

    mechanic: str = Field("", description="Mechanic or system name")
    category: str = Field("", description="Category (combat, traversal, progression, etc.)")
    description: str = Field("", description="How the mechanic works")
    player_impact: str = Field("", description="Why it matters to players")
    mastery_curve: str = Field("", description="Skill depth or learning curve")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="mechanic", header="Mechanic", style="magenta", no_wrap=True),
            TableSchema(name="category", header="Category", style="cyan"),
            TableSchema(name="player_impact", header="Impact", style="yellow"),
            TableSchema(name="mastery_curve", header="Mastery"),
        ]


class MultiplayerModeInfo(GameJsonModel):
    """Multiplayer mode descriptor."""

    mode_name: str = Field("", description="Mode name")
    mode_type: str = Field("", description="Structure (PvP, PvE, co-op, arena)")
    max_players: int | None = Field(None, description="Maximum concurrent players")
    is_ranked: bool = Field(False, description="Whether ranked progression is available")
    cross_play: bool = Field(False, description="Cross-platform support flag")
    description: str = Field("", description="Summary of objectives or flow")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="mode_name", header="Mode", style="magenta", no_wrap=True),
            TableSchema(name="mode_type", header="Type", style="cyan"),
            TableSchema(name="max_players", header="Players", justify="right", formatter=format_number),
            TableSchema(name="is_ranked", header="Ranked"),
            TableSchema(name="cross_play", header="Cross-Play"),
        ]


class LiveServiceEventInfo(GameJsonModel):
    """Live operations or seasonal event entry."""

    event_name: str = Field("", description="Event name")
    cadence: str = Field("", description="Cadence or schedule")
    focus: str = Field("", description="Primary content or theme")
    rewards: list[str] = Field(default_factory=list, description="Rewards or unlocks")
    retention_goal: str = Field("", description="Player behaviour the event targets")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="event_name", header="Event", style="magenta"),
            TableSchema(name="cadence", header="Cadence", style="cyan"),
            TableSchema(name="focus", header="Focus", style="yellow"),
            TableSchema(name="rewards", header="Rewards"),
        ]


class AccessibilityFeatureInfo(GameJsonModel):
    """Accessibility option support."""

    feature: str = Field("", description="Feature name")
    status: str = Field("", description="Implementation status")
    notes: str = Field("", description="Additional detail")
    platform_support: list[str] = Field(default_factory=list, description="Platforms where the feature ships")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="feature", header="Feature", style="magenta"),
            TableSchema(name="status", header="Status", style="cyan"),
            TableSchema(name="platform_support", header="Platforms"),
        ]


class ProgressionTrackInfo(GameJsonModel):
    """Progression layer or upgrade path."""

    track_name: str = Field("", description="Track or system name")
    track_type: str = Field("", description="Type (XP, gear score, reputation)")
    unlocks: list[str] = Field(default_factory=list, description="Key unlocks or rewards")
    pacing: str = Field("", description="Expected pacing or cadence")
    hard_cap: int | None = Field(None, description="Level or score cap if applicable")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="track_name", header="Track", style="magenta"),
            TableSchema(name="track_type", header="Type", style="cyan"),
            TableSchema(name="hard_cap", header="Cap", justify="right", formatter=format_number),
            TableSchema(name="pacing", header="Pacing"),
        ]


class NarrativeBeatInfo(GameJsonModel):
    """Narrative beat or quest milestone."""

    beat_name: str = Field("", description="Beat name")
    synopsis: str = Field("", description="Beat synopsis")
    branching_choice: str = Field("", description="Choice or divergence available")
    emotional_tone: str = Field("", description="Tone or mood")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="beat_name", header="Beat", style="magenta"),
            TableSchema(name="synopsis", header="Synopsis", style="cyan"),
            TableSchema(name="branching_choice", header="Choice", style="yellow"),
            TableSchema(name="emotional_tone", header="Tone"),
        ]


class AudioDesignCue(GameJsonModel):
    """Audio design highlight."""

    cue_name: str = Field("", description="Cue title or track")
    composer: str = Field("", description="Composer or audio lead")
    style: str = Field("", description="Musical or sonic style")
    gameplay_trigger: str = Field("", description="When/why the cue plays")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="cue_name", header="Cue", style="magenta"),
            TableSchema(name="composer", header="Composer", style="cyan"),
            TableSchema(name="style", header="Style", style="yellow"),
            TableSchema(name="gameplay_trigger", header="Trigger"),
        ]


class EconomyModelInfo(GameJsonModel):
    """In-game economy or monetisation model."""

    currency: str = Field("", description="Currency name")
    acquisition: list[str] = Field(default_factory=list, description="How players earn the currency")
    spending: list[str] = Field(default_factory=list, description="Where currency is spent")
    monetisation_type: str = Field("", description="Premium, cosmetic-only, power, subscription")
    average_spend: int | None = Field(None, description="Average spend or price point in cents")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="currency", header="Currency", style="magenta"),
            TableSchema(name="monetisation_type", header="Type", style="cyan"),
            TableSchema(name="average_spend", header="Avg Spend", justify="right", formatter=format_money),
            TableSchema(name="acquisition", header="Acquisition"),
        ]


class EconomyLoopInfo(GameJsonModel):
    """Loop describing currency flow or resource economy."""

    loop_name: str = Field("", description="Loop or system name")
    loop_type: str = Field("", description="Type such as core, auxiliary, endgame")
    inputs: list[str] = Field(default_factory=list, description="Primary inputs or earn vectors")
    outputs: list[str] = Field(default_factory=list, description="Outputs or spend vectors")
    monetisation_hook: str = Field("", description="How monetisation interfaces with the loop")
    retention_goal: str = Field("", description="Retention or behavioural goal")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="loop_name", header="Loop", style="magenta"),
            TableSchema(name="loop_type", header="Type", style="cyan"),
            TableSchema(name="monetisation_hook", header="Monetisation", style="yellow"),
            TableSchema(name="retention_goal", header="Retention"),
        ]


class TechnicalBenchmarkInfo(GameJsonModel):
    """Technical benchmark or performance target."""

    scenario: str = Field("", description="Scenario or location")
    hardware_profile: str = Field("", description="Hardware profile tested")
    target_metrics: str = Field("", description="Target performance metrics")
    measured_metrics: str = Field("", description="Observed metrics")
    optimisation_notes: str = Field("", description="Key optimisation notes")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="scenario", header="Scenario", style="magenta"),
            TableSchema(name="hardware_profile", header="Hardware", style="cyan"),
            TableSchema(name="target_metrics", header="Target"),
            TableSchema(name="measured_metrics", header="Measured"),
        ]


class EsportsEventInfo(GameJsonModel):
    """Esports ecosystem entry."""

    event_name: str = Field("", description="Event or league name")
    tier: str = Field("", description="Tier (grassroots, pro, major)")
    region: str = Field("", description="Primary region")
    prize_pool: int | None = Field(None, description="Prize pool amount")
    broadcast_partners: list[str] = Field(default_factory=list, description="Broadcast or streaming partners")
    format_notes: str = Field("", description="Notable format or rule set details")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="event_name", header="Event", style="magenta"),
            TableSchema(name="tier", header="Tier", style="cyan"),
            TableSchema(name="region", header="Region", style="yellow"),
            TableSchema(name="prize_pool", header="Prize Pool", justify="right", formatter=format_money),
        ]


class SessionProfileInfo(GameJsonModel):
    """Average play session characteristics."""

    activity: str = Field("", description="Activity focus for the session")
    average_duration_minutes: int | None = Field(None, description="Average session length in minutes")
    player_goal: str = Field("", description="Why players log in")
    engagement_metric: str = Field("", description="Metric tracked (DAU, retention)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="activity", header="Activity", style="magenta"),
            TableSchema(
                name="average_duration_minutes",
                header="Duration",
                style="cyan",
                justify="right",
                formatter=format_runtime_minutes,
            ),
            TableSchema(name="player_goal", header="Player Goal", style="yellow"),
            TableSchema(name="engagement_metric", header="Metric"),
        ]


class SocialFeatureInfo(GameJsonModel):
    """Social system descriptor for persistent games."""

    feature_name: str = Field("", description="Feature or system name")
    surface_area: str = Field("", description="Where players encounter it (hub, UI, guild)")
    communication_tools: list[str] = Field(default_factory=list, description="Communication tools provided")
    safety_tooling: str = Field("", description="Moderation or safety support")
    retention_role: str = Field("", description="How the feature supports retention")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="feature_name", header="Feature", style="magenta"),
            TableSchema(name="surface_area", header="Surface", style="cyan"),
            TableSchema(name="safety_tooling", header="Safety", style="yellow"),
            TableSchema(name="retention_role", header="Retention"),
        ]


__all__ = [
    "GameFormatBase",
    "GameJsonModel",
    "StudioProfile",
    "PlatformReleaseInfo",
    "GameplayMechanicHighlight",
    "MultiplayerModeInfo",
    "LiveServiceEventInfo",
    "AccessibilityFeatureInfo",
    "ProgressionTrackInfo",
    "NarrativeBeatInfo",
    "AudioDesignCue",
    "EconomyModelInfo",
    "TechnicalBenchmarkInfo",
    "EsportsEventInfo",
    "SessionProfileInfo",
    "EconomyLoopInfo",
    "SocialFeatureInfo",
]
