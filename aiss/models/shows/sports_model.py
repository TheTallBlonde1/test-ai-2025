"""Sports TV show format models."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_runtime_minutes, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    JsonModel,
    ProductionCompanyInfo,
    ShowFormatBase,
)

instructions = (
    "Step into the role of a sports television programming strategist preparing a comprehensive dossier on a sports TV show. "
    "Detail the presenter and analyst bench, recurring coverage segments, featured teams or athletes, seasonal event calendar, rights landscape, production approach, digital extensions, and monetization tactics. "
    "Capture distribution footprint, critical response, and audience performance so the sports television brand stands out."
)


class SportsPresenter(JsonModel):
    """Anchor, analyst, or commentator profile."""

    name: str = Field("", description="Presenter name")
    role: str = Field("", description="Role (host, analyst, sideline reporter)")
    expertise: str = Field("", description="Primary sport or expertise area")
    former_athlete: bool = Field(False, description="Whether the presenter previously competed professionally")
    tone: str = Field("", description="On-air tone or personality")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Presenter", style="magenta", no_wrap=True),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="expertise", header="Expertise", style="cyan"),
            TableSchema(name="tone", header="Tone"),
        ]


class CoverageSegment(JsonModel):
    """Recurring coverage segment."""

    name: str = Field("", description="Segment name")
    sport: str = Field("", description="Sport or league focus")
    focus: str = Field("", description="Segment focus (analysis, highlights, interviews)")
    schedule_slot: str = Field("", description="Where it appears in the programme")
    hosts: list[str] = Field(default_factory=list, description="Hosts or analysts on segment")
    duration_minutes: int = Field(0, description="Typical duration")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Segment", style="magenta"),
            TableSchema(name="sport", header="Sport", style="cyan"),
            TableSchema(name="focus", header="Focus", style="yellow"),
            TableSchema(name="duration_minutes", header="Duration", justify="center", formatter=format_runtime_minutes),
        ]


class TeamAthleteFeature(JsonModel):
    """Feature story on a team or athlete."""

    subject: str = Field("", description="Team or athlete name")
    league: str = Field("", description="League or competition")
    feature_type: str = Field("", description="Profile, documentary, tactical breakdown")
    storyline: str = Field("", description="Narrative angle")
    stats_highlight: str = Field("", description="Stat or record emphasised")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="subject", header="Subject", style="magenta"),
            TableSchema(name="league", header="League", style="cyan"),
            TableSchema(name="feature_type", header="Feature Type", style="yellow"),
            TableSchema(name="stats_highlight", header="Highlight"),
        ]


class SeasonEventBlock(JsonModel):
    """Seasonal coverage block or event."""

    event_name: str = Field("", description="Event or competition name")
    start_date: str = Field("", description="Start date (ISO)")
    end_date: str = Field("", description="End date (ISO)")
    coverage_plan: str = Field("", description="Coverage approach")
    rights_holder: str = Field("", description="Broadcast rights holder")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="event_name", header="Event", style="magenta"),
            TableSchema(name="start_date", header="Start", style="cyan"),
            TableSchema(name="end_date", header="End"),
            TableSchema(name="coverage_plan", header="Coverage Plan"),
            TableSchema(name="rights_holder", header="Rights Holder", style="yellow"),
        ]


class StatHighlight(JsonModel):
    """Highlight stat used within coverage."""

    metric: str = Field("", description="Metric tracked")
    leader: str = Field("", description="Current leader or team")
    timeframe: str = Field("", description="Timeframe for the metric")
    context: str = Field("", description="Contextual note or comparison")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="metric", header="Metric", style="magenta"),
            TableSchema(name="leader", header="Leader", style="cyan"),
            TableSchema(name="timeframe", header="Timeframe", style="yellow"),
            TableSchema(name="context", header="Context"),
        ]


class SportsShowInfo(ShowFormatBase):
    """Sports programme format."""

    model_name: ClassVar[str] = "SportsShowInfo"
    description: ClassVar[str] = "Sports television intelligence model encapsulating live and studio coverage strategy, rights positioning, and audience impact."
    key_trait: ClassVar[str] = "Rights-driven sports TV coverage blending live action and analysis"

    title: str = Field("", description="Programme title")
    show_summary: str = Field("", description="Expanded synopsis")
    network: str = Field("", description="Network or platform")
    premiere_year: int = Field(0, description="Year launched")
    broadcast_schedule: str = Field("", description="Broadcast cadence")
    runtime_minutes: int = Field(0, description="Runtime")
    sports_covered: list[str] = Field(default_factory=list, description="Sports or leagues covered")
    flagship_elements: list[str] = Field(default_factory=list, description="Flagship segments or shows")
    production_style: str = Field("", description="Studio, remote, hybrid")
    tone: str = Field("", description="Tone (energetic, analytical)")
    rights_overview: str = Field("", description="Broadcast rights landscape")
    digital_strategy: list[str] = Field(default_factory=list, description="Digital or social extensions")
    monetization: list[str] = Field(default_factory=list, description="Sponsorship or monetization tactics")
    executive_producers: list[str] = Field(default_factory=list, description="Executive producers")

    presenters: list[SportsPresenter] = Field(default_factory=list, description="Presenters and analysts")
    coverage_segments: list[CoverageSegment] = Field(default_factory=list, description="Recurring segments")
    team_features: list[TeamAthleteFeature] = Field(default_factory=list, description="Team or athlete features")
    seasonal_events: list[SeasonEventBlock] = Field(default_factory=list, description="Seasonal event coverage")
    stat_highlights: list[StatHighlight] = Field(default_factory=list, description="Highlighted statistics")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical or trade response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience performance metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production partners")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Sports Programme"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [self.show_summary or "(no summary provided)"]
        return (self.title or self.summary_title_fallback, summary_lines, "green")

    def _fact_pairs(self) -> list[tuple[str, str]]:
        runtime = format_runtime_minutes(self.runtime_minutes)
        return [
            ("Network", self.network or "-"),
            ("Premiered", format_year(self.premiere_year)),
            ("Schedule", self.broadcast_schedule or "-"),
            ("Runtime", runtime),
            ("Sports", ", ".join(self.sports_covered) if self.sports_covered else "-"),
            ("Flagship", ", ".join(self.flagship_elements) if self.flagship_elements else "-"),
            ("Production", self.production_style or "-"),
            ("Tone", self.tone or "-"),
            ("Rights", self.rights_overview or "-"),
            ("Digital", ", ".join(self.digital_strategy) if self.digital_strategy else "-"),
            ("Monetization", ", ".join(self.monetization) if self.monetization else "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.presenters:
            sections.append(("Presenters", SportsPresenter.table_schema(), self.presenters))
        if self.coverage_segments:
            sections.append(("Coverage Segments", CoverageSegment.table_schema(), self.coverage_segments))
        if self.team_features:
            sections.append(("Team/Athlete Features", TeamAthleteFeature.table_schema(), self.team_features))
        if self.seasonal_events:
            sections.append(("Seasonal Events", SeasonEventBlock.table_schema(), self.seasonal_events))
        if self.stat_highlights:
            sections.append(("Stat Highlights", StatHighlight.table_schema(), self.stat_highlights))
        if self.critical_reception:
            sections.append(("Critical Reception", CriticalResponse.table_schema(), self.critical_reception))
        if self.audience_metrics:
            sections.append(("Audience Metrics", AudienceEngagement.table_schema(), self.audience_metrics))
        if self.production_companies:
            sections.append(("Production Companies", ProductionCompanyInfo.table_schema(), self.production_companies))
        if self.broadcast_info:
            sections.append(("Broadcast", BroadcastInfo.table_schema(), self.broadcast_info))
        if self.distribution_info:
            sections.append(("Distribution", DistributionInfo.table_schema(), self.distribution_info))
        return sections

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Deliver a full-spectrum sports TV show overview for '" + name + "', detailing presenters, coverage segments, seasonal plans, rights context, and performance metrics."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON keys including title, show_summary, network, premiere_year, broadcast_schedule, runtime_minutes, "
            "sports_covered, flagship_elements, production_style, tone, rights_overview, digital_strategy, monetization, "
            "executive_producers, presenters, coverage_segments, team_features, seasonal_events, stat_highlights, "
            "critical_reception, audience_metrics, production_companies, broadcast_info, distribution_info."
        )
