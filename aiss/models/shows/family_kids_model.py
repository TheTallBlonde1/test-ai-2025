"""Family / Animation / Kids TV show format models."""

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
    "Act as a children's television strategy lead compiling a definitive brief on a family, animation, or kids TV show. "
    "Describe the target age range, developmental goals, educational focus, core values, character ensemble, recurring lessons, music integration, and parental guidance resources. "
    "Explain the production approach, broadcast and distribution footprint, critical reception, and audience engagement so the series is clearly positioned for family co-viewing."
)


class FamilyCharacterProfile(JsonModel):
    """Main character profile geared for family animation."""

    name: str = Field("", description="Character name")
    voice_actor: str = Field("", description="Voice actor")
    role: str = Field("", description="Role within the ensemble (protagonist, sibling, mentor)")
    species_or_type: str = Field("", description="Species or type (human, animal, fantastical)")
    personality_traits: list[str] = Field(default_factory=list, description="Personality traits")
    lesson_focus: str = Field("", description="Lesson the character often conveys")
    catchphrases: list[str] = Field(default_factory=list, description="Catchphrases or slogans")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="voice_actor", header="Voice Actor", style="cyan"),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="lesson_focus", header="Lesson Focus"),
        ]


class EducationalSegment(JsonModel):
    """Educational segment or lesson highlight."""

    episode: str = Field("", description="Episode or segment title")
    topic: str = Field("", description="Educational topic")
    skills_targeted: list[str] = Field(default_factory=list, description="Skills or values targeted")
    teaching_approach: str = Field("", description="Approach such as storytelling, music, interactive")
    takeaway: str = Field("", description="Key lesson takeaway")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="episode", header="Episode", style="magenta"),
            TableSchema(name="topic", header="Topic", style="cyan"),
            TableSchema(name="teaching_approach", header="Approach", style="yellow"),
            TableSchema(name="takeaway", header="Takeaway"),
        ]


class ParentGuideNote(JsonModel):
    """Parental guidance note supporting co-viewing."""

    topic: str = Field("", description="Topic for discussion")
    conversation_starters: list[str] = Field(default_factory=list, description="Questions parents can ask")
    emotional_notes: str = Field("", description="Emotional considerations for children")
    reinforcement_ideas: list[str] = Field(default_factory=list, description="Activities to reinforce lessons")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="topic", header="Topic", style="magenta"),
            TableSchema(name="emotional_notes", header="Emotional Notes", style="cyan"),
        ]


class MusicMoment(JsonModel):
    """Musical element utilised in the series."""

    song_title: str = Field("", description="Song or musical cue name")
    episode: str = Field("", description="Episode where the song appears")
    style: str = Field("", description="Musical style or genre")
    purpose: str = Field("", description="Purpose such as teaching, celebration, montage")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="song_title", header="Song", style="magenta"),
            TableSchema(name="episode", header="Episode", style="cyan"),
            TableSchema(name="style", header="Style"),
            TableSchema(name="purpose", header="Purpose"),
        ]


class FamilyAnimationKidsShowInfo(ShowFormatBase):
    """Family/animation/kids show format."""

    model_name: ClassVar[str] = "FamilyAnimationKidsShowInfo"
    description: ClassVar[str] = "Family and kids television intelligence model blending creative highlights, educational intent, and market positioning."
    key_trait: ClassVar[str] = "Family-friendly TV storytelling that balances developmental goals with entertainment"

    title: str = Field("", description="Series title")
    show_summary: str = Field("", description="Expanded synopsis")
    premise: str = Field("", description="Core premise")
    format_type: str = Field("", description="Format (animated series, mixed media, live-action hybrid)")
    target_age_range: str = Field("", description="Intended age range")
    educational_focus: list[str] = Field(default_factory=list, description="Educational domains (social-emotional, STEM)")
    core_values: list[str] = Field(default_factory=list, description="Values emphasised")
    tone: str = Field("", description="Tone descriptors (wholesome, adventurous)")
    season_count: int = Field(0, description="Seasons produced")
    episode_count: int = Field(0, description="Episodes produced")
    average_runtime_minutes: int = Field(0, description="Average runtime")
    release_start_year: int = Field(0, description="First release year")
    release_end_year: int = Field(0, description="Latest release year or 0 if ongoing")
    age_rating: str = Field("", description="Content rating")
    creators: list[str] = Field(default_factory=list, description="Series creators")
    showrunners: list[str] = Field(default_factory=list, description="Showrunners")
    educational_advisors: list[str] = Field(default_factory=list, description="Educational consultants")

    characters: list[FamilyCharacterProfile] = Field(default_factory=list, description="Main characters")
    educational_segments: list[EducationalSegment] = Field(default_factory=list, description="Educational segments")
    parent_guides: list[ParentGuideNote] = Field(default_factory=list, description="Parental guidance notes")
    music: list[MusicMoment] = Field(default_factory=list, description="Musical moments")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production companies")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Family / Kids Series"

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
            ("Format", self.format_type or "-"),
            ("Target Age", self.target_age_range or "-"),
            ("Educational Focus", ", ".join(self.educational_focus) if self.educational_focus else "-"),
            ("Core Values", ", ".join(self.core_values) if self.core_values else "-"),
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
            sections.append(("Characters", FamilyCharacterProfile.table_schema(), self.characters))
        if self.educational_segments:
            sections.append(("Educational Segments", EducationalSegment.table_schema(), self.educational_segments))
        if self.parent_guides:
            sections.append(("Parent Guides", ParentGuideNote.table_schema(), self.parent_guides))
        if self.music:
            sections.append(("Music Moments", MusicMoment.table_schema(), self.music))
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
        return "Deliver a comprehensive family or kids TV show profile for '" + name + "', spotlighting educational aims, character ensemble, signature lessons, and reception."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys such as title, show_summary, premise, format_type, target_age_range, "
            "educational_focus, core_values, tone, season_count, episode_count, average_runtime_minutes, "
            "release_start_year, release_end_year, age_rating, creators, showrunners, educational_advisors, "
            "characters, educational_segments, parent_guides, music, critical_reception, audience_metrics, "
            "production_companies, broadcast_info, distribution_info."
        )
