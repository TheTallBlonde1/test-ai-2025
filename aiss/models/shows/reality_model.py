"""Reality / Competition / Lifestyle TV show format models."""

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
    "Assume the perspective of an unscripted television format analyst preparing a definitive brief on a reality, competition, or lifestyle TV show. "
    "Break down the host and judge lineup, contestant archetypes, challenge architecture, episodic phases, prize mechanics, production design, and filming locations. "
    "Highlight tone, audience participation pathways, critical reception, and engagement metrics so the unscripted television property stands apart in the market."
)


class HostJudgeProfile(JsonModel):
    """Host or judge profile."""

    name: str = Field("", description="Name of the host or judge")
    role: str = Field("", description="Role on the show (host, head judge, mentor)")
    expertise: str = Field("", description="Professional background or expertise")
    personality_traits: list[str] = Field(default_factory=list, description="Notable on-screen traits")
    seasons_present: list[int] = Field(default_factory=list, description="Seasons they appeared")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Name", style="magenta", no_wrap=True),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="expertise", header="Expertise", style="cyan"),
        ]


class ParticipantProfile(JsonModel):
    """Participant or contestant archetype."""

    name: str = Field("", description="Participant name")
    archetype: str = Field("", description="Archetype or narrative role (underdog, strategist)")
    background: str = Field("", description="Background story or profession")
    standout_skills: list[str] = Field(default_factory=list, description="Key skills or strengths")
    season_appearance: int = Field(0, description="Season participated")
    notable_moments: list[str] = Field(default_factory=list, description="Highlight moments")
    final_outcome: str = Field("", description="Result such as winner, finalist, eliminated week 5")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Participant", style="magenta"),
            TableSchema(name="archetype", header="Archetype", style="yellow"),
            TableSchema(name="background", header="Background", style="cyan"),
            TableSchema(name="final_outcome", header="Outcome"),
        ]


class ChallengeInfo(JsonModel):
    """Recurring challenge or task."""

    name: str = Field("", description="Challenge name")
    challenge_type: str = Field("", description="Skill tested or format type")
    description: str = Field("", description="Overview of the challenge")
    stakes: str = Field("", description="What is at stake")
    reward: str = Field("", description="Reward or advantage")
    frequency: str = Field("", description="How often it appears")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Challenge", style="magenta"),
            TableSchema(name="challenge_type", header="Type", style="cyan"),
            TableSchema(name="stakes", header="Stakes", style="yellow"),
            TableSchema(name="reward", header="Reward"),
        ]


class FormatPhase(JsonModel):
    """A phase within each episode or season arc."""

    phase_name: str = Field("", description="Phase name (auditions, bootcamp, live shows)")
    description: str = Field("", description="What happens during the phase")
    elimination_format: str = Field("", description="How eliminations are handled")
    audience_participation: str = Field("", description="Voting, live audience, social engagement")
    signature_elements: list[str] = Field(default_factory=list, description="Signature elements or twists")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="phase_name", header="Phase", style="magenta"),
            TableSchema(name="elimination_format", header="Elimination", style="yellow"),
            TableSchema(name="audience_participation", header="Audience Participation", style="cyan"),
            TableSchema(name="description", header="Description"),
        ]


class RealityCompetitionLifestyleShowInfo(ShowFormatBase):
    """Reality / competition / lifestyle show format."""

    model_name: ClassVar[str] = "RealityCompetitionLifestyleShowInfo"
    description: ClassVar[str] = "Unscripted television intelligence model emphasizing format structure, on-camera talent, and audience hooks."
    key_trait: ClassVar[str] = "Competition or lifestyle TV storytelling powered by real participants"

    title: str = Field("", description="Series title")
    show_summary: str = Field("", description="Expanded synopsis")
    format_description: str = Field("", description="Format overview")
    subgenre: list[str] = Field(default_factory=list, description="Subgenres such as competition, makeover, docu-series")
    tone: str = Field("", description="Tone descriptors (uplifting, intense)")
    prize: str = Field("", description="Grand prize or goal")
    filming_locations: list[str] = Field(default_factory=list, description="Primary filming locations")
    season_count: int = Field(0, description="Seasons produced")
    episode_count: int = Field(0, description="Episodes produced")
    average_runtime_minutes: int = Field(0, description="Average runtime per episode")
    release_start_year: int = Field(0, description="First release year")
    release_end_year: int = Field(0, description="Most recent year or 0 if ongoing")
    age_rating: str = Field("", description="Content rating")
    creators: list[str] = Field(default_factory=list, description="Series creators")
    showrunners: list[str] = Field(default_factory=list, description="Showrunners or executive producers")

    hosts_and_judges: list[HostJudgeProfile] = Field(default_factory=list, description="Hosts and judges")
    participants: list[ParticipantProfile] = Field(default_factory=list, description="Representative participants")
    challenges: list[ChallengeInfo] = Field(default_factory=list, description="Signature challenges")
    format_phases: list[FormatPhase] = Field(default_factory=list, description="Episode/season phases")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Ratings and engagement")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production companies")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Reality / Competition"

    def _summary_panel(self) -> tuple[str, list[str], str]:
        summary_lines = [
            self.format_description or "(no format description)",
            self.show_summary or "(no summary)",
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
            ("Subgenre", ", ".join(self.subgenre) if self.subgenre else "-"),
            ("Tone", self.tone or "-"),
            ("Prize", self.prize or "-"),
            ("Locations", ", ".join(self.filming_locations) if self.filming_locations else "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Runtime", runtime),
            ("Run", run_display),
            ("Rating", self.age_rating or "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.hosts_and_judges:
            sections.append(("Hosts & Judges", HostJudgeProfile.table_schema(), self.hosts_and_judges))
        if self.participants:
            sections.append(("Participants", ParticipantProfile.table_schema(), self.participants))
        if self.challenges:
            sections.append(("Challenges", ChallengeInfo.table_schema(), self.challenges))
        if self.format_phases:
            sections.append(("Format Phases", FormatPhase.table_schema(), self.format_phases))
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
        return "Deliver a definitive reality, competition, or lifestyle TV show breakdown for '" + name + "', spotlighting talent, contestant archetypes, challenges, format phases, and reception."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON fields including title, show_summary, format_description, subgenre, tone, prize, "
            "filming_locations, season_count, episode_count, average_runtime_minutes, release_start_year, "
            "release_end_year, age_rating, creators, showrunners, hosts_and_judges, participants, challenges, "
            "format_phases, critical_reception, audience_metrics, production_companies, broadcast_info, distribution_info."
        )
