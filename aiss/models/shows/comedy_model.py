"""Comedy TV show format models."""

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
    "Act as a senior television insights researcher compiling a definitive report on a comedy TV show. "
    "Deliver an expansive overview of the premise, tonal pillars, comedic engines, ensemble dynamics, "
    "signature running gags, representative episodes, production context, and the critical and audience response. "
    "Surface broadcast and distribution footprint, any live audience or improvisational elements, and how the humour "
    "evolved across seasons so the television comedy feels richly differentiated."
)


class ComedyCharacterProfile(JsonModel):
    """Representation of a comedic character and their humour style."""

    name: str = Field("", description="Character name")
    actor: str = Field("", description="Performer or voice actor")
    comedic_role: str = Field("", description="Role type e.g. straight person, prankster, deadpan")
    signature_gag: str = Field("", description="Memorable gag or comedic device")
    relationships: list[str] = Field(default_factory=list, description="Key relationships or dynamics")
    catchphrases: list[str] = Field(default_factory=list, description="Recurring catchphrases if any")
    spotlight_episodes: list[str] = Field(default_factory=list, description="Episodes featuring the character prominently")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="comedic_role", header="Role", style="yellow"),
            TableSchema(name="signature_gag", header="Signature Gag"),
        ]


class ComedyEpisodeBeat(JsonModel):
    """Episode-level comedic structure."""

    episode_title: str = Field("", description="Episode title or sketch collection name")
    season: int = Field(0, description="Season number")
    comedic_engine: str = Field("", description="Primary comedic mechanism driving the episode")
    core_conflict: str = Field("", description="Conflict or scenario the episode revolves around")
    guest_stars: list[str] = Field(default_factory=list, description="Notable guest stars")
    resolution: str = Field("", description="How the episode resolves or buttons the joke")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="episode_title", header="Episode", style="magenta"),
            TableSchema(name="season", header="Season", justify="center", formatter=format_year),
            TableSchema(name="comedic_engine", header="Comedic Engine", style="cyan"),
            TableSchema(name="resolution", header="Resolution"),
        ]


class RunningGagInfo(JsonModel):
    """Recurring gag or motif utilised throughout the comedy."""

    name: str = Field("", description="Name of the running gag")
    description: str = Field("", description="What makes the gag notable")
    first_appearance: str = Field("", description="Episode or season where the gag debuted")
    frequency: str = Field("", description="How often the gag appears")
    notable_variations: list[str] = Field(default_factory=list, description="Memorable variations of the gag")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Running Gag", style="magenta"),
            TableSchema(name="first_appearance", header="First Seen", style="cyan"),
            TableSchema(name="frequency", header="Frequency", style="yellow"),
            TableSchema(name="description", header="Description"),
        ]


class ComedyShowInfo(ShowFormatBase):
    """Comedy-specific show information."""

    model_name: ClassVar[str] = "ComedyShowInfo"
    description: ClassVar[str] = "Comprehensive intelligence model for humour-driven television series, balancing creative, production, and market context."
    key_trait: ClassVar[str] = "Television comedy storytelling anchored by recurring humour engines"

    title: str = Field("", description="Title of the comedy series")
    premise: str = Field("", description="One-line premise or hook")
    show_summary: str = Field("", description="Expanded synopsis of the comedic approach")
    format_type: str = Field("", description="Sitcom, sketch, mockumentary, dramedy, etc.")
    humour_styles: list[str] = Field(default_factory=list, description="Comedic styles leveraged (satire, slapstick, etc.)")
    tone: str = Field("", description="General tone (lighthearted, absurdist, dark)")
    primary_setting: str = Field("", description="Core setting or workplace")
    season_count: int = Field(0, description="Number of seasons")
    episode_count: int = Field(0, description="Total episodes")
    episode_length_minutes: int = Field(0, description="Typical runtime per episode")
    release_start_year: int = Field(0, description="First air year")
    release_end_year: int = Field(0, description="Final air year or 0 if ongoing")
    age_rating: str = Field("", description="Content rating")
    live_audience: bool = Field(False, description="Whether the show uses a live audience or laugh track")
    improv_elements: str = Field("", description="Extent of improvisation or loose scripting")

    characters: list[ComedyCharacterProfile] = Field(default_factory=list, description="Principal comedic characters")
    episode_beats: list[ComedyEpisodeBeat] = Field(default_factory=list, description="Representative episodes or sketches")
    running_gags: list[RunningGagInfo] = Field(default_factory=list, description="Signature recurring gags")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical reactions")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience performance metrics")

    writers_room: list[str] = Field(default_factory=list, description="Key writers or showrunners")
    directors: list[str] = Field(default_factory=list, description="Notable directors")
    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production companies involved")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Comedy Series"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [
            self.premise or "(no premise provided)",
            self.show_summary or "(no summary provided)",
        ]
        return (self.title or self.summary_title_fallback, summary_lines, "green")

    def _fact_pairs(self) -> list[tuple[str, str]]:
        run_start = format_year(self.release_start_year)
        run_end = "Present" if not self.release_end_year else format_year(self.release_end_year)
        episode_length = format_runtime_minutes(self.episode_length_minutes)
        seasons = format_number(self.season_count) if self.season_count else "-"
        episodes = format_number(self.episode_count) if self.episode_count else "-"
        if run_start == "-" and run_end == "-":
            run_display = "-"
        elif run_start == "-" or run_start == run_end:
            run_display = run_end
        else:
            run_display = f"{run_start} - {run_end}"

        return [
            ("Format", self.format_type or "-"),
            ("Tone", self.tone or "-"),
            ("Humour Styles", ", ".join(self.humour_styles) if self.humour_styles else "-"),
            ("Setting", self.primary_setting or "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Episode Length", episode_length),
            ("Audience", "Live" if self.live_audience else "Single-camera"),
            ("Improv", self.improv_elements or "-"),
            ("Run", run_display),
            ("Rating", self.age_rating or "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.characters:
            sections.append(("Characters", ComedyCharacterProfile.table_schema(), self.characters))
        if self.running_gags:
            sections.append(("Running Gags", RunningGagInfo.table_schema(), self.running_gags))
        if self.episode_beats:
            sections.append(("Episode Beats", ComedyEpisodeBeat.table_schema(), self.episode_beats))
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
        return "Produce a richly detailed comedy TV show brief for '" + name + "', emphasizing tone, ensemble chemistry, standout comedic beats, and performance metrics."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON including fields such as title, premise, show_summary, format_type, "
            "humour_styles, tone, primary_setting, season_count, episode_count, "
            "episode_length_minutes, release_start_year, release_end_year, age_rating, "
            "live_audience, improv_elements, writers_room, directors, characters, "
            "episode_beats, running_gags, critical_reception, audience_metrics, "
            "production_companies, broadcast_info, distribution_info."
        )
