"""Thriller / Crime / Mystery TV show format models."""

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
    "Operate as a scripted television analyst preparing a gripping briefing on a thriller, crime, or mystery TV show. "
    "Lay out the investigative team, signature cases, antagonists, narrative structure, pacing devices, tonal palette, and thematic obsessions. "
    "Discuss production context, subject-matter consultants, broadcast strategy, and critical versus audience response so the suspense-driven television property feels distinctive."
)


class InvestigatorProfile(JsonModel):
    """Lead investigator, detective, or protagonist profile."""

    name: str = Field("", description="Investigator name")
    actor: str = Field("", description="Performer")
    role: str = Field("", description="Role within the unit (lead detective, profiler, etc.)")
    specialty: str = Field("", description="Forensic, psychological, undercover, etc.")
    personal_motivation: str = Field("", description="Driving personal stakes")
    moral_alignment: str = Field("", description="Moral compass or grey areas")
    status: str = Field("", description="Current status within the story")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Investigator", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="specialty", header="Specialty"),
            TableSchema(name="moral_alignment", header="Alignment"),
        ]


class MajorCaseFile(JsonModel):
    """Signature case or mystery arc."""

    case_name: str = Field("", description="Case title or identifier")
    season: int = Field(0, description="Season number")
    synopsis: str = Field("", description="Summary of the case")
    stakes: str = Field("", description="Why the case matters")
    key_twist: str = Field("", description="Major twist revealed")
    resolution_status: str = Field("", description="Solved, unresolved, ongoing")
    antagonists_involved: list[str] = Field(default_factory=list, description="Key antagonists tied to the case")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="case_name", header="Case", style="magenta"),
            TableSchema(name="season", header="Season", justify="center", formatter=format_year),
            TableSchema(name="stakes", header="Stakes", style="yellow"),
            TableSchema(name="resolution_status", header="Status", style="cyan"),
            TableSchema(name="key_twist", header="Key Twist"),
        ]


class AntagonistProfile(JsonModel):
    """Notable antagonist or criminal figure."""

    name: str = Field("", description="Antagonist name")
    actor: str = Field("", description="Portraying actor")
    motive: str = Field("", description="Driving motive")
    methodology: str = Field("", description="Signature modus operandi")
    affiliation: str = Field("", description="Organisation or affiliation")
    season_presence: list[int] = Field(default_factory=list, description="Seasons where they appear")
    fate: str = Field("", description="Fate within the narrative")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Antagonist", style="magenta"),
            TableSchema(name="motive", header="Motive", style="yellow"),
            TableSchema(name="methodology", header="Method"),
            TableSchema(name="affiliation", header="Affiliation", style="cyan"),
            TableSchema(name="fate", header="Fate"),
        ]


class ThrillerShowInfo(ShowFormatBase):
    """Thriller/crime/mystery show format."""

    model_name: ClassVar[str] = "ThrillerShowInfo"
    description: ClassVar[str] = "Suspense television intelligence model spotlighting investigative craft, tension architecture, and market positioning."
    key_trait: ClassVar[str] = "High-stakes crime or mystery TV engineered for sustained suspense"

    title: str = Field("", description="Series title")
    tagline: str = Field("", description="Tagline or hook")
    show_summary: str = Field("", description="Detailed synopsis")
    subgenre: str = Field("", description="Police procedural, psychological thriller, espionage, etc.")
    narrative_structure: str = Field("", description="Serialised, anthology, episodic with arcs")
    tone: str = Field("", description="Tone descriptors (dark, gritty, cerebral)")
    themes: list[str] = Field(default_factory=list, description="Major themes explored")
    violence_level: str = Field("", description="Violence/gore rating")
    age_rating: str = Field("", description="Content rating")
    season_count: int = Field(0, description="Number of seasons")
    episode_count: int = Field(0, description="Number of episodes")
    average_runtime_minutes: int = Field(0, description="Average runtime per episode")
    release_start_year: int = Field(0, description="Initial release year")
    release_end_year: int = Field(0, description="Final release year or 0 if ongoing")
    creators: list[str] = Field(default_factory=list, description="Series creators")
    showrunners: list[str] = Field(default_factory=list, description="Showrunners")
    consultants: list[str] = Field(default_factory=list, description="Law enforcement/subject matter consultants")

    investigators: list[InvestigatorProfile] = Field(default_factory=list, description="Investigative team members")
    major_cases: list[MajorCaseFile] = Field(default_factory=list, description="Signature cases or arcs")
    antagonists: list[AntagonistProfile] = Field(default_factory=list, description="Primary antagonists")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical reception excerpts")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience response and ratings")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production entities")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Thriller Series"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [
            self.tagline or "(no tagline provided)",
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
            ("Subgenre", self.subgenre or "-"),
            ("Tone", self.tone or "-"),
            ("Structure", self.narrative_structure or "-"),
            ("Themes", ", ".join(self.themes) if self.themes else "-"),
            ("Violence", self.violence_level or "-"),
            ("Age Rating", self.age_rating or "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Run", run_display),
            ("Runtime", runtime),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.investigators:
            sections.append(("Investigators", InvestigatorProfile.table_schema(), self.investigators))
        if self.major_cases:
            sections.append(("Major Cases", MajorCaseFile.table_schema(), self.major_cases))
        if self.antagonists:
            sections.append(("Antagonists", AntagonistProfile.table_schema(), self.antagonists))
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
        return "Deliver a high-tension thriller TV show analysis for '" + name + "', covering investigators, signature cases, antagonists, structure, and reception."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys including title, tagline, show_summary, subgenre, "
            "narrative_structure, tone, themes, violence_level, age_rating, season_count, episode_count, "
            "average_runtime_minutes, release_start_year, release_end_year, creators, showrunners, consultants, "
            "investigators, major_cases, antagonists, critical_reception, audience_metrics, production_companies, "
            "broadcast_info, distribution_info."
        )
