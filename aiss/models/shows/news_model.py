"""News / Informational TV show format models."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_runtime_minutes, format_year

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
    "Position yourself as a broadcast news strategist assembling a definitive dossier on a news or informational TV show. "
    "Detail the anchor team, correspondents, recurring segments, editorial focus, verification standards, production operations, scheduling cadence, and digital extensions. "
    "Summarize signature coverage moments, critical reception, awards, and audience metrics so the television programme's authority and reach are unmistakable."
)


class AnchorProfile(JsonModel):
    """Anchor or presenter profile."""

    name: str = Field("", description="Anchor/presenter name")
    role: str = Field("", description="Role (lead anchor, correspondent, analyst)")
    expertise: str = Field("", description="Coverage expertise")
    tone: str = Field("", description="On-air tone")
    tenure_years: int = Field(0, description="Years with the programme")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Anchor", style="magenta", no_wrap=True),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="expertise", header="Expertise", style="cyan"),
            TableSchema(name="tenure_years", header="Tenure", justify="center", formatter=format_number),
        ]


class SegmentBlueprint(JsonModel):
    """Recurring segment blueprint."""

    name: str = Field("", description="Segment name")
    format_type: str = Field("", description="Format (headline block, panel, explainer)")
    duration_minutes: int = Field(0, description="Typical duration")
    hosts: list[str] = Field(default_factory=list, description="Hosts or contributors")
    focus: str = Field("", description="Coverage focus")
    recurrence: str = Field("", description="Frequency within programme")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Segment", style="magenta"),
            TableSchema(name="format_type", header="Format", style="cyan"),
            TableSchema(name="duration_minutes", header="Duration", justify="center", formatter=format_runtime_minutes),
            TableSchema(name="focus", header="Focus"),
        ]


class CorrespondentReport(JsonModel):
    """Field report summary."""

    correspondent: str = Field("", description="Correspondent name")
    location: str = Field("", description="Location of report")
    topic: str = Field("", description="Topic covered")
    status: str = Field("", description="Status (airing, developing, follow-up)")
    date: str = Field("", description="Date of report")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="correspondent", header="Correspondent", style="magenta"),
            TableSchema(name="location", header="Location", style="cyan"),
            TableSchema(name="topic", header="Topic"),
            TableSchema(name="status", header="Status", style="yellow"),
        ]


class FactCheckProcess(JsonModel):
    """Fact-checking or verification summary."""

    step: str = Field("", description="Process step")
    description: str = Field("", description="Details of the verification step")
    responsible_team: str = Field("", description="Editorial team responsible")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="step", header="Step", style="magenta"),
            TableSchema(name="responsible_team", header="Team", style="cyan"),
            TableSchema(name="description", header="Description"),
        ]


class NewsInformationalShowInfo(ShowFormatBase):
    """News/informational programme model."""

    model_name: ClassVar[str] = "NewsInformationalShowInfo"
    description: ClassVar[str] = "Television news intelligence model capturing editorial architecture, on-air talent, and platform footprint."
    key_trait: ClassVar[str] = "Timely, verified public-interest journalism delivered as a TV programme"

    title: str = Field("", description="Programme name")
    show_summary: str = Field("", description="Expanded synopsis")
    network: str = Field("", description="Network or platform")
    premiere_year: int = Field(0, description="Launch year")
    broadcast_schedule: str = Field("", description="Broadcast cadence (daily, weekly)")
    runtime_minutes: int = Field(0, description="Runtime")
    production_location: str = Field("", description="Primary production location")
    editorial_focus: list[str] = Field(default_factory=list, description="Coverage pillars")
    tone: str = Field("", description="Editorial tone")
    fact_check_philosophy: str = Field("", description="Editorial fact-check stance")
    verification_sources: list[str] = Field(default_factory=list, description="Typical verification sources")
    digital_platforms: list[str] = Field(default_factory=list, description="Digital or streaming outlets")
    executive_producers: list[str] = Field(default_factory=list, description="Executive producers")

    anchors: list[AnchorProfile] = Field(default_factory=list, description="Anchors and presenters")
    segment_blueprints: list[SegmentBlueprint] = Field(default_factory=list, description="Recurring segments")
    correspondent_reports: list[CorrespondentReport] = Field(default_factory=list, description="Field reports")
    fact_check_process: list[FactCheckProcess] = Field(default_factory=list, description="Fact-checking workflow")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production companies")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Syndication or distribution")

    summary_title_fallback: ClassVar[str] = "News / Informational"

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
            ("Location", self.production_location or "-"),
            ("Tone", self.tone or "-"),
            ("Editorial Focus", ", ".join(self.editorial_focus) if self.editorial_focus else "-"),
            ("Verification", self.fact_check_philosophy or "-"),
            ("Digital", ", ".join(self.digital_platforms) if self.digital_platforms else "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.anchors:
            sections.append(("Anchors", AnchorProfile.table_schema(), self.anchors))
        if self.segment_blueprints:
            sections.append(("Segments", SegmentBlueprint.table_schema(), self.segment_blueprints))
        if self.correspondent_reports:
            sections.append(("Correspondent Reports", CorrespondentReport.table_schema(), self.correspondent_reports))
        if self.fact_check_process:
            sections.append(("Fact-Check Process", FactCheckProcess.table_schema(), self.fact_check_process))
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
        return "Deliver a comprehensive news or informational TV show overview for '" + name + "', covering talent lineup, segment structure, editorial standards, distribution, and audience performance."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON fields including title, show_summary, network, premiere_year, broadcast_schedule, "
            "runtime_minutes, production_location, editorial_focus, tone, fact_check_philosophy, verification_sources, "
            "digital_platforms, executive_producers, anchors, segment_blueprints, correspondent_reports, "
            "fact_check_process, critical_reception, audience_metrics, production_companies, broadcast_info, "
            "distribution_info."
        )
