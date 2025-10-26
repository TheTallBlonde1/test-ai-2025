"""Drama TV show format models.

Defines a drama-specific format that emphasises character arcs, serialized
story beats, and critical recognition. The public entry point
`DramaShowInfo` satisfies `ModelFormatProtocol` so it can be consumed by
existing OpenAI helpers.
"""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_runtime_minutes, format_year

from ..shared import TableSchema, compose_instructions
from ._base import AudienceEngagement, BroadcastInfo, CriticalResponse, DistributionInfo, JsonModel, ProductionCompanyInfo, ShowFormatBase

instructions = (
    "Adopt the voice of a prestige television development executive compiling an in-depth dossier on a drama TV show. "
    "Deliver a nuanced overview of the premise, tonal identity, primary themes, principal characters and their emotional arcs, "
    "serialized storylines with conflict and resolution markers, awards trajectory, and international distribution strategy. "
    "Weave in critical reception highlights and audience metrics so the television drama feels fully positioned in the market."
)


class DramaCharacterProfile(JsonModel):
    """Character-centric data with an emphasis on emotional development."""

    name: str = Field("", description="Character full name")
    actor: str = Field("", description="Actor portraying the character")
    arc_summary: str = Field("", description="Summary of the core emotional arc")
    driving_conflict: str = Field("", description="Primary internal/external conflict")
    key_relationships: list[str] = Field(default_factory=list, description="Key relationships that define the character")
    season_introduced: int = Field(0, description="Season where the character enters the narrative")
    current_status: str = Field("", description="Status at latest season (active, deceased, imprisoned, etc.)")
    notable_episodes: list[str] = Field(default_factory=list, description="Episodes pivotal to the character arc")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="arc_summary", header="Arc Summary"),
            TableSchema(name="driving_conflict", header="Conflict"),
            TableSchema(name="season_introduced", header="Introduced", justify="center", formatter=format_year),
            TableSchema(name="current_status", header="Status", style="yellow"),
        ]


class DramaStoryArc(JsonModel):
    """Serialized storyline encapsulating conflict and resolution."""

    arc_title: str = Field("", description="Name of the arc or storyline")
    season_focus: int = Field(0, description="Season in which the arc is central")
    episode_span: str = Field("", description="Episodes covering the arc (e.g., S02E01-S02E08)")
    synopsis: str = Field("", description="Concise overview of the storyline")
    primary_themes: list[str] = Field(default_factory=list, description="Themes explored in the arc")
    resolution_status: str = Field("", description="Resolved, cliffhanger, ongoing, etc.")
    key_turning_point: str = Field("", description="Defining twist or escalation point")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="arc_title", header="Arc", style="magenta"),
            TableSchema(name="season_focus", header="Season", justify="center", formatter=format_year),
            TableSchema(name="episode_span", header="Episodes", style="cyan"),
            TableSchema(name="resolution_status", header="Status", style="yellow"),
            TableSchema(name="key_turning_point", header="Turning Point"),
        ]


class DramaAwardRecognition(JsonModel):
    """Award and nomination tracking for the drama series."""

    award_body: str = Field("", description="Award organisation (Emmys, Golden Globes, etc.)")
    category: str = Field("", description="Category of the nomination")
    year: int = Field(0, description="Year of the nomination")
    recipient: str = Field("", description="Series, actor, director, etc. that received the nomination")
    result: str = Field("", description="Winner, Nominee, Pending")
    notes: str = Field("", description="Context such as specific episode or season")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="year", header="Year", justify="center", formatter=format_year),
            TableSchema(name="award_body", header="Award", style="magenta"),
            TableSchema(name="category", header="Category", style="cyan"),
            TableSchema(name="recipient", header="Recipient"),
            TableSchema(name="result", header="Result", style="yellow"),
        ]


class DramaShowInfo(ShowFormatBase):
    """Drama-specific format implementing ModelFormatProtocol."""

    model_name: ClassVar[str] = "DramaShowInfo"
    description: ClassVar[str] = "Detailed television drama intelligence model capturing serialized storytelling, character evolution, and industry recognition."
    key_trait: ClassVar[str] = "Emotionally charged serialized TV drama anchored by character arcs"

    title: str = Field("", description="Official title of the drama")
    logline: str = Field("", description="High-level premise statement")
    show_summary: str = Field("", description="Expanded synopsis of the series")
    tone: str = Field("", description="Overall tonal qualities (gritty, heartfelt, etc.)")
    themes: list[str] = Field(default_factory=list, description="Dominant themes explored")
    primary_setting: str = Field("", description="Main setting or locale")
    season_count: int = Field(0, description="Total number of seasons")
    episode_count: int = Field(0, description="Total episodes produced")
    average_runtime_minutes: int = Field(0, description="Average runtime per episode in minutes")
    age_rating: str = Field("", description="Official content rating")
    release_start_year: int = Field(0, description="Initial release year")
    release_end_year: int = Field(0, description="Most recent release year or 0 if ongoing")
    showrunners: list[str] = Field(default_factory=list, description="Showrunner(s) leading the series")
    head_writers: list[str] = Field(default_factory=list, description="Head writers")
    directors: list[str] = Field(default_factory=list, description="Notable directors or producing directors")
    composers: list[str] = Field(default_factory=list, description="Lead composers or music supervisors")

    characters: list[DramaCharacterProfile] = Field(default_factory=list, description="Principal characters and arcs")
    major_story_arcs: list[DramaStoryArc] = Field(default_factory=list, description="Serialized arcs driving the narrative")
    awards: list[DramaAwardRecognition] = Field(default_factory=list, description="Awards and nominations history")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical reviews and pull quotes")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Viewership and demographic metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Studios and production companies")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners by region")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution/licensing footprint")

    summary_title_fallback: ClassVar[str] = "Drama Series"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [
            self.logline or "(no logline provided)",
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
            ("Tone", self.tone or "-"),
            ("Themes", ", ".join(self.themes) if self.themes else "-"),
            ("Setting", self.primary_setting or "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Avg Runtime", runtime),
            ("Age Rating", self.age_rating or "-"),
            ("Run", run_display),
            ("Showrunners", ", ".join(self.showrunners) if self.showrunners else "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.characters:
            sections.append(("Characters", DramaCharacterProfile.table_schema(), self.characters))
        if self.major_story_arcs:
            sections.append(("Story Arcs", DramaStoryArc.table_schema(), self.major_story_arcs))
        if self.awards:
            sections.append(("Awards", DramaAwardRecognition.table_schema(), self.awards))
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
        return "Deliver a richly layered drama TV show brief for '" + name + "', covering character journeys, serialized arcs, tonal themes, awards profile, and distribution reach."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn a JSON object with keys such as title, logline, show_summary, "
            "tone, themes, primary_setting, season_count, episode_count, "
            "average_runtime_minutes, age_rating, release_start_year, release_end_year, "
            "showrunners, head_writers, directors, composers, characters, major_story_arcs, "
            "awards, critical_reception, audience_metrics, production_companies, broadcast_info, "
            "distribution_info."
        )
