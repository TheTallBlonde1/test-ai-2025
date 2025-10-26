"""Action / Adventure / Fantasy TV show format models."""

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
    "Adopt the voice of a premium television development analyst preparing a sweeping dossier on an action, adventure, or fantasy TV show. "
    "Chart the world-building foundations, heroic parties, quest arcs, signature locations, artifacts, production scale, stunt and visual effects approach, and release cadence. "
    "Surface thematic throughlines, tone evolution, creative leadership, and the television distribution footprint alongside critical reception and audience performance so the series feels cinematic yet distinctly serialized."
)


class HeroProfile(JsonModel):
    """Lead hero or ensemble member profile."""

    name: str = Field("", description="Character name")
    actor: str = Field("", description="Portraying actor or voice actor")
    role: str = Field("", description="Role within the party (protagonist, mentor, anti-hero)")
    abilities: list[str] = Field(default_factory=list, description="Signature abilities or powers")
    affiliations: list[str] = Field(default_factory=list, description="Allied factions or guilds")
    notable_items: list[str] = Field(default_factory=list, description="Weapons or artifacts carried")
    arc_summary: str = Field("", description="Summary of the character's journey")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Hero", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Performer", style="cyan"),
            TableSchema(name="role", header="Role", style="yellow"),
            TableSchema(name="arc_summary", header="Arc Summary"),
        ]


class QuestArc(JsonModel):
    """Major quest or campaign storyline."""

    quest_name: str = Field("", description="Name of the quest")
    season: int = Field(0, description="Season focus")
    objective: str = Field("", description="Primary objective of the quest")
    antagonists: list[str] = Field(default_factory=list, description="Antagonists opposing the quest")
    allies: list[str] = Field(default_factory=list, description="Key allies aiding the quest")
    stakes: str = Field("", description="Consequences of success/failure")
    resolution: str = Field("", description="Outcome of the quest")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="quest_name", header="Quest", style="magenta"),
            TableSchema(name="season", header="Season", justify="center", formatter=format_year),
            TableSchema(name="objective", header="Objective", style="cyan"),
            TableSchema(name="stakes", header="Stakes", style="yellow"),
            TableSchema(name="resolution", header="Resolution"),
        ]


class WorldLocation(JsonModel):
    """Important world location or realm."""

    name: str = Field("", description="Location name")
    locale_type: str = Field("", description="Type of locale (kingdom, realm, station, planet)")
    description: str = Field("", description="Notable description")
    controlling_faction: str = Field("", description="Faction controlling the location")
    first_appearance: str = Field("", description="Episode/season introduced")
    narrative_significance: str = Field("", description="Why the location matters")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Location", style="magenta"),
            TableSchema(name="locale_type", header="Type", style="cyan"),
            TableSchema(name="controlling_faction", header="Faction", style="yellow"),
            TableSchema(name="narrative_significance", header="Significance"),
        ]


class ArtifactInfo(JsonModel):
    """Legendary artifact or magical item."""

    name: str = Field("", description="Artifact name")
    classification: str = Field("", description="Type (weapon, relic, spellbook)")
    powers: list[str] = Field(default_factory=list, description="Abilities or boons granted")
    wielders: list[str] = Field(default_factory=list, description="Notable wielders")
    origin: str = Field("", description="Origin story or creation details")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Artifact", style="magenta"),
            TableSchema(name="classification", header="Type", style="cyan"),
            TableSchema(name="origin", header="Origin"),
        ]


class ActionAdventureFantasyShowInfo(ShowFormatBase):
    """Action/adventure/fantasy show format."""

    model_name: ClassVar[str] = "ActionAdventureFantasyShowInfo"
    description: ClassVar[str] = "High-energy television adventure model capturing world-building depth, serialized quest structure, and production ecosystem insights."
    key_trait: ClassVar[str] = "Serialized action-fantasy television driven by quests and expansive settings"

    title: str = Field("", description="Series title")
    show_summary: str = Field("", description="Expanded synopsis")
    tagline: str = Field("", description="Marketing tagline")
    world_setting: str = Field("", description="Primary world or universe description")
    genre_mix: list[str] = Field(default_factory=list, description="Blend of subgenres (space opera, epic fantasy, etc.)")
    tone: str = Field("", description="Tone descriptors")
    core_themes: list[str] = Field(default_factory=list, description="Themes like heroism, destiny, loyalty")
    season_count: int = Field(0, description="Seasons produced")
    episode_count: int = Field(0, description="Episodes produced")
    average_runtime_minutes: int = Field(0, description="Average runtime per episode")
    age_rating: str = Field("", description="Content rating")
    visual_style: str = Field("", description="Notes on cinematography or aesthetic")
    effects_approach: str = Field("", description="Practical, CGI heavy, hybrid")
    release_start_year: int = Field(0, description="First release year")
    release_end_year: int = Field(0, description="Most recent year or 0 if ongoing")
    creators: list[str] = Field(default_factory=list, description="Series creators")
    showrunners: list[str] = Field(default_factory=list, description="Showrunners")
    stunt_coordinators: list[str] = Field(default_factory=list, description="Stunt or action coordinators")

    heroes: list[HeroProfile] = Field(default_factory=list, description="Heroic ensemble")
    quest_arcs: list[QuestArc] = Field(default_factory=list, description="Major quest arcs")
    world_locations: list[WorldLocation] = Field(default_factory=list, description="Key locations")
    artifacts: list[ArtifactInfo] = Field(default_factory=list, description="Important artifacts")
    critical_reception: list[CriticalResponse] = Field(default_factory=list, description="Critical response")
    audience_metrics: list[AudienceEngagement] = Field(default_factory=list, description="Audience metrics")

    production_companies: list[ProductionCompanyInfo] = Field(default_factory=list, description="Production partners")
    broadcast_info: list[BroadcastInfo] = Field(default_factory=list, description="Broadcast partners")
    distribution_info: list[DistributionInfo] = Field(default_factory=list, description="Distribution footprint")

    summary_title_fallback: ClassVar[str] = "Action/Adventure/Fantasy"

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
            ("World", self.world_setting or "-"),
            ("Genre Mix", ", ".join(self.genre_mix) if self.genre_mix else "-"),
            ("Tone", self.tone or "-"),
            ("Themes", ", ".join(self.core_themes) if self.core_themes else "-"),
            ("Visual Style", self.visual_style or "-"),
            ("Effects", self.effects_approach or "-"),
            ("Seasons", seasons),
            ("Episodes", episodes),
            ("Run", run_display),
            ("Runtime", runtime),
            ("Rating", self.age_rating or "-"),
        ]

    def _table_sections(self) -> list[tuple[str, List[TableSchema], list[JsonModel]]]:
        sections: list[tuple[str, List[TableSchema], list[JsonModel]]] = []
        if self.heroes:
            sections.append(("Heroes", HeroProfile.table_schema(), self.heroes))
        if self.quest_arcs:
            sections.append(("Quest Arcs", QuestArc.table_schema(), self.quest_arcs))
        if self.world_locations:
            sections.append(("World Locations", WorldLocation.table_schema(), self.world_locations))
        if self.artifacts:
            sections.append(("Artifacts", ArtifactInfo.table_schema(), self.artifacts))
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
        return "Craft a richly detailed action, adventure, or fantasy TV show brief for '" + name + "', highlighting world-building, heroic ensembles, landmark quests, production scale, and reception."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON containing fields including title, show_summary, tagline, world_setting, genre_mix, "
            "tone, core_themes, season_count, episode_count, average_runtime_minutes, age_rating, visual_style, "
            "effects_approach, release_start_year, release_end_year, creators, showrunners, stunt_coordinators, "
            "heroes, quest_arcs, world_locations, artifacts, critical_reception, audience_metrics, "
            "production_companies, broadcast_info, distribution_info."
        )
