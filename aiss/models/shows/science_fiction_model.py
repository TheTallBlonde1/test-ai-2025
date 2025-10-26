"""Science fiction TV show format models."""

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
    "Write as a speculative television researcher compiling a high-impact briefing on a science fiction TV show. "
    "Explain the premise, world-building, core ensemble, speculative technologies, timeline disruptions, scientific disciplines explored, and philosophical questions posed. "
    "Outline production design choices, effects methodology, distribution footprint, critical reception, and audience response so the sci-fi television property feels visionary and distinct."
)


class SciFiCharacterProfile(JsonModel):
    """Key science fiction character with speciality details."""

    name: str = Field("", description="Character name")
    actor: str = Field("", description="Performer or voice actor")
    role: str = Field("", description="Role aboard the crew or in the narrative")
    species_or_origin: str = Field("", description="Species or planetary/system origin")
    specialization: str = Field("", description="Scientific or tactical specialty")
    ethical_alignment: str = Field("", description="Moral stance or philosophy")
    arc_summary: str = Field("", description="Character arc overview")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Performer", style="cyan"),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="specialization", header="Specialization"),
            TableSchema(name="species_or_origin", header="Origin"),
        ]


class TechnologyConcept(JsonModel):
    """Speculative technology or scientific concept."""

    name: str = Field("", description="Technology or concept name")
    category: str = Field("", description="Type (AI, propulsion, biotech, etc.)")
    description: str = Field("", description="Explanation of the technology")
    introduced_in: str = Field("", description="Episode/season introduced")
    scientific_basis: str = Field("", description="Real-world science foundation, if any")
    ethical_implications: str = Field("", description="Ethical or societal impact")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Technology", style="magenta"),
            TableSchema(name="category", header="Category", style="cyan"),
            TableSchema(name="scientific_basis", header="Scientific Basis"),
            TableSchema(name="ethical_implications", header="Ethical Implications"),
        ]


class TimelineEvent(JsonModel):
    """Significant event in the narrative timeline."""

    year: int = Field(0, description="In-universe year or timeframe")
    event: str = Field("", description="Event description")
    location: str = Field("", description="Location or region affected")
    impact: str = Field("", description="Impact on narrative or society")
    featured_in: list[str] = Field(default_factory=list, description="Episodes or seasons featuring the event")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="year", header="Year", justify="center", formatter=format_year),
            TableSchema(name="event", header="Event", style="magenta"),
            TableSchema(name="location", header="Location", style="cyan"),
            TableSchema(name="impact", header="Impact"),
        ]


class ScientificTheme(JsonModel):
    """Philosophical or scientific theme explored."""

    theme: str = Field("", description="Theme name")
    question: str = Field("", description="Core question posed")
    representative_episodes: list[str] = Field(default_factory=list, description="Episodes exploring the theme")
    human_implication: str = Field("", description="Human or societal implication highlighted")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="theme", header="Theme", style="magenta"),
            TableSchema(name="question", header="Guiding Question", style="cyan"),
            TableSchema(name="human_implication", header="Human Implication"),
        ]


class ScienceFictionShowInfo(ShowFormatBase):
    """Science fiction focused show format."""

    model_name: ClassVar[str] = "ScienceFictionShowInfo"
    description: ClassVar[str] = "Speculative television intelligence model synthesizing world-building, scientific themes, and production context."
    key_trait: ClassVar[str] = "Technology-driven TV storytelling exploring future-facing ideas"

    title: str = Field("", description="Series title")
    show_summary: str = Field("", description="Detailed synopsis")
    premise: str = Field("", description="Premise or hook")
    world_setting: str = Field("", description="Universe/setting description")
    subgenre: str = Field("", description="Cyberpunk, space opera, hard sci-fi, etc.")
    scientific_focus: list[str] = Field(default_factory=list, description="Scientific disciplines explored")
    philosophical_questions: list[str] = Field(default_factory=list, description="Key philosophical questions")
    tone: str = Field("", description="Tone descriptors")
    season_count: int = Field(0, description="Seasons produced")
    episode_count: int = Field(0, description="Episodes produced")
    average_runtime_minutes: int = Field(0, description="Average runtime")
    age_rating: str = Field("", description="Content rating")
    release_start_year: int = Field(0, description="First release year")
    release_end_year: int = Field(0, description="Final release year or 0 if ongoing")
    creators: list[str] = Field(default_factory=list, description="Series creators")
    showrunners: list[str] = Field(default_factory=list, description="Showrunners")
    scientific_consultants: list[str] = Field(default_factory=list, description="Scientific advisors")

    characters: list[SciFiCharacterProfile] = Field(default_factory=list, description="Primary characters")
    technologies: list[TechnologyConcept] = Field(default_factory=list, description="Speculative technologies")
    timeline_events: list[TimelineEvent] = Field(default_factory=list, description="Timeline events")
    themes: list[ScientificTheme] = Field(default_factory=list, description="Scientific or philosophical themes")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production companies")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Science Fiction Series"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [
            self.premise or "(no premise provided)",
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
            ("Setting", self.world_setting or "-"),
            ("Subgenre", self.subgenre or "-"),
            ("Scientific Focus", ", ".join(self.scientific_focus) if self.scientific_focus else "-"),
            ("Philosophical Questions", "; ".join(self.philosophical_questions) if self.philosophical_questions else "-"),
            ("Tone", self.tone or "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Runtime", runtime),
            ("Run", run_display),
            ("Rating", self.age_rating or "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.characters:
            sections.append(("Characters", SciFiCharacterProfile.table_schema(), self.characters))
        if self.technologies:
            sections.append(("Technologies", TechnologyConcept.table_schema(), self.technologies))
        if self.timeline_events:
            sections.append(("Timeline", TimelineEvent.table_schema(), self.timeline_events))
        if self.themes:
            sections.append(("Themes", ScientificTheme.table_schema(), self.themes))
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
        return "Produce a comprehensive science fiction TV show briefing for '" + name + "', highlighting world-building, speculative technology, timeline events, and creative reception."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON keys such as title, show_summary, premise, world_setting, subgenre, scientific_focus, "
            "philosophical_questions, tone, season_count, episode_count, average_runtime_minutes, age_rating, "
            "release_start_year, release_end_year, creators, showrunners, scientific_consultants, characters, "
            "technologies, timeline_events, themes, critical_reception, audience_metrics, production_companies, "
            "broadcast_info, distribution_info."
        )
