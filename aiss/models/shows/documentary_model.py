"""Documentary / Factual TV show format models."""

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
    "Assume the role of a factual television commissioner assembling an authoritative report on a documentary or factual TV show. "
    "Map the editorial scope, narrative methodology, signature episodes, interview subjects, archival resources, and production techniques. "
    "Explain the series' educational or cultural impact, critical reception, awards journey, distribution footprint, and audience engagement so the television property feels thoroughly contextualized."
)


class DocumentaryEpisode(JsonModel):
    """Episode-level summary for documentary series."""

    title: str = Field("", description="Episode title")
    focus: str = Field("", description="Primary topic or focus")
    runtime_minutes: int = Field(0, description="Runtime in minutes")
    key_subjects: list[str] = Field(default_factory=list, description="Subjects or organisations featured")
    narrative_devices: list[str] = Field(default_factory=list, description="Narrative devices (interviews, animation)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="title", header="Episode", style="magenta"),
            TableSchema(name="focus", header="Focus", style="cyan"),
            TableSchema(name="runtime_minutes", header="Runtime", justify="right", formatter=format_runtime_minutes),
        ]


class InterviewSubject(JsonModel):
    """Key interview subject or expert."""

    name: str = Field("", description="Interview subject name")
    expertise: str = Field("", description="Expertise or perspective")
    affiliation: str = Field("", description="Affiliation or organisation")
    role_in_story: str = Field("", description="Role in the narrative")
    standout_quote: str = Field("", description="Notable quote or insight")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Subject", style="magenta", no_wrap=True),
            TableSchema(name="expertise", header="Expertise", style="cyan"),
            TableSchema(name="affiliation", header="Affiliation"),
            TableSchema(name="role_in_story", header="Story Role", style="yellow"),
        ]


class ArchiveMaterial(JsonModel):
    """Archive material leveraged in the documentary."""

    material_type: str = Field("", description="Type (archival footage, photos, letters)")
    description: str = Field("", description="Description of the material")
    source: str = Field("", description="Source or rights holder")
    year: int = Field(0, description="Year of origin or coverage")
    usage: str = Field("", description="How it is used in the narrative")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="material_type", header="Material", style="magenta"),
            TableSchema(name="source", header="Source", style="cyan"),
            TableSchema(name="year", header="Year", justify="center", formatter=format_year),
            TableSchema(name="usage", header="Usage"),
        ]


class InsightHighlight(JsonModel):
    """Key insight or takeaway delivered by the series."""

    topic: str = Field("", description="Topic area")
    takeaway: str = Field("", description="Insight or conclusion")
    supporting_evidence: list[str] = Field(default_factory=list, description="Supporting evidence or episodes")
    impact_statement: str = Field("", description="Impact on public understanding or policy")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="topic", header="Topic", style="magenta"),
            TableSchema(name="takeaway", header="Takeaway", style="cyan"),
            TableSchema(name="impact_statement", header="Impact"),
        ]


class DocumentaryFactualShowInfo(ShowFormatBase):
    """Documentary/factual show format."""

    model_name: ClassVar[str] = "DocumentaryFactualShowInfo"
    description: ClassVar[str] = "Comprehensive factual television model capturing investigative craft, storytelling design, and platform reach."
    key_trait: ClassVar[str] = "Non-fiction television that informs through investigative or observational storytelling"

    title: str = Field("", description="Series title")
    show_summary: str = Field("", description="Expanded synopsis")
    scope: str = Field("", description="Scope such as global issue, historical event")
    narrative_style: str = Field("", description="Narrative style (observational, investigative, hosted)")
    tone: str = Field("", description="Tone descriptors")
    season_count: int = Field(0, description="Seasons produced")
    episode_count: int = Field(0, description="Episodes produced")
    average_runtime_minutes: int = Field(0, description="Average runtime")
    release_start_year: int = Field(0, description="First release year")
    release_end_year: int = Field(0, description="Final release year or 0 if ongoing")
    age_rating: str = Field("", description="Content rating")
    directors: list[str] = Field(default_factory=list, description="Directors")
    narrators: list[str] = Field(default_factory=list, description="Narrators or hosts")
    cinematographers: list[str] = Field(default_factory=list, description="Cinematographers")
    production_style: str = Field("", description="Production approach (verité, re-enactments)")

    episodes: list[DocumentaryEpisode] = Field(default_factory=list, description="Key episodes")
    interview_subjects: list[InterviewSubject] = Field(default_factory=list, description="Notable interview subjects")
    archive_materials: list[ArchiveMaterial] = Field(default_factory=list, description="Archive materials")
    insights: list[InsightHighlight] = Field(default_factory=list, description="Insights delivered")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production companies")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Documentary / Factual"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [
            self.scope or "(no scope provided)",
            self.show_summary or "(no summary provided)",
        ]
        return (self.title or self.summary_title_fallback, summary_lines, "green")

    def _fact_pairs(self) -> list[tuple[str, str]]:
        run_start = format_year(self.release_start_year)
        run_end = "Present" if not self.release_end_year else format_year(self.release_end_year)
        runtime = format_runtime_minutes(self.average_runtime_minutes)
        seasons = format_number(self.season_count) if self.season_count else "-"
        episodes = format_number(self.episode_count) if self.episode_count else "-"
        if run_start == "-" and run_end == "-":
            run_display = "-"
        elif run_start == "-" or run_start == run_end:
            run_display = run_end
        else:
            run_display = f"{run_start} - {run_end}"

        return [
            ("Style", self.narrative_style or "-"),
            ("Tone", self.tone or "-"),
            ("Production Style", self.production_style or "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Runtime", runtime),
            ("Run", run_display),
            ("Rating", self.age_rating or "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.episodes:
            sections.append(("Episodes", DocumentaryEpisode.table_schema(), self.episodes))
        if self.interview_subjects:
            sections.append(("Interview Subjects", InterviewSubject.table_schema(), self.interview_subjects))
        if self.archive_materials:
            sections.append(("Archive Materials", ArchiveMaterial.table_schema(), self.archive_materials))
        if self.insights:
            sections.append(("Insights", InsightHighlight.table_schema(), self.insights))
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
        return "Deliver a richly detailed documentary or factual TV show overview for '" + name + "', highlighting scope, storytelling approach, signature episodes, key contributors, and impact."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON keys including title, show_summary, scope, narrative_style, tone, production_style, "
            "season_count, episode_count, average_runtime_minutes, release_start_year, release_end_year, age_rating, "
            "directors, narrators, cinematographers, episodes, interview_subjects, archive_materials, insights, "
            "critical_reception, audience_metrics, production_companies, broadcast_info, distribution_info."
        )
