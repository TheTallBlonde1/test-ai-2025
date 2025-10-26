"""Role-Playing Game (RPG) format model."""

from __future__ import annotations

from typing import ClassVar, List, Sequence

from pydantic import Field

from aiss.utils import format_number, format_year

from ..shared import TableSchema, compose_instructions
from ._base import (
    AccessibilityFeatureInfo,
    AudioDesignCue,
    GameFormatBase,
    GameJsonModel,
    GameplayMechanicHighlight,
    LiveServiceEventInfo,
    NarrativeBeatInfo,
    PlatformReleaseInfo,
    ProgressionTrackInfo,
    StudioProfile,
)

instructions = "Summarise an RPG as a worldbuilding director. Describe setting, factions, character classes, choice consequence systems, and how player builds evolve. Capture quest arcs, companion dynamics, monetisation, and post-launch narrative cadence so the RPG’s scope is obvious."


class CharacterClassProfile(GameJsonModel):
    """Playable class or archetype profile."""

    class_name: str = Field("", description="Class name or archetype")
    combat_role: str = Field("", description="Primary combat role")
    resource_model: str = Field("", description="Resource or energy system")
    signature_abilities: list[str] = Field(default_factory=list, description="Signature abilities or spells")
    complexity_rating: str = Field("", description="Learning complexity or recommended audience")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="class_name", header="Class", style="magenta"),
            TableSchema(name="combat_role", header="Role", style="cyan"),
            TableSchema(name="resource_model", header="Resource", style="yellow"),
            TableSchema(name="complexity_rating", header="Complexity"),
        ]


class CompanionProfile(GameJsonModel):
    """Recruitable companion or party member."""

    name: str = Field("", description="Companion name")
    origin: str = Field("", description="Origin or faction alignment")
    combat_synergy: str = Field("", description="Combat synergy or support role")
    loyalty_arc: str = Field("", description="Personal arc or loyalty quest summary")
    romanceable: bool = Field(False, description="Whether romance is available")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Companion", style="magenta"),
            TableSchema(name="origin", header="Origin", style="cyan"),
            TableSchema(name="combat_synergy", header="Synergy", style="yellow"),
            TableSchema(name="romanceable", header="Romance"),
        ]


class FactionProfile(GameJsonModel):
    """Faction or organisation description."""

    faction_name: str = Field("", description="Faction name")
    ideology: str = Field("", description="Core ideology or belief")
    territory: str = Field("", description="Primary territory or region")
    relationship_state: str = Field("", description="Relationship state with protagonist")
    rewards: list[str] = Field(default_factory=list, description="Rewards or benefits")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="faction_name", header="Faction", style="magenta"),
            TableSchema(name="ideology", header="Ideology", style="cyan"),
            TableSchema(name="territory", header="Territory", style="yellow"),
            TableSchema(name="relationship_state", header="Relationship"),
        ]


class RolePlayingGameInfo(GameFormatBase):
    """RPG genre format."""

    model_name: ClassVar[str] = "RolePlayingGameInfo"
    description: ClassVar[str] = "Role-playing game model highlighting worldbuilding, character progression, and branching narrative structure."
    key_trait: ClassVar[str] = "Character-driven storytelling with deep progression layers"

    summary_title_fallback: ClassVar[str] = "Role-Playing Game"
    summary_attributes: ClassVar[Sequence[str]] = ("core_loop", "game_summary")

    title: str = Field("", description="Game title")
    game_summary: str = Field("", description="World overview and narrative hook")
    core_loop: str = Field("", description="Loop (explore, quest, combat, upgrade)")
    world_setting: str = Field("", description="World or realm description")
    timeline_context: str = Field("", description="Timeline or lore framing")
    protagonist_identity: str = Field("", description="Player character identity or customisation scope")
    release_year: int = Field(0, description="Initial release year")
    estimated_campaign_hours: float = Field(0.0, description="Estimated hours for campaign")
    build_flexibility: str = Field("", description="Approach to player build freedom")
    choice_consequence_map: str = Field("", description="How player choices impact the world")
    monetisation_model: str = Field("", description="Monetisation approach (premium, expansions, cosmetics)")
    post_launch_story_plan: str = Field("", description="Narrative DLC or expansion roadmap")

    developers: list[StudioProfile] = Field(default_factory=list, description="Development partners")
    publishers: list[StudioProfile] = Field(default_factory=list, description="Publishing partners")
    platform_releases: list[PlatformReleaseInfo] = Field(default_factory=list, description="Platform releases")
    factions: list[FactionProfile] = Field(default_factory=list, description="Factions or organisations")
    character_classes: list[CharacterClassProfile] = Field(default_factory=list, description="Playable classes")
    companions: list[CompanionProfile] = Field(default_factory=list, description="Companion roster")
    systems: list[GameplayMechanicHighlight] = Field(default_factory=list, description="Key systems and mechanics")
    narrative_beats: list[NarrativeBeatInfo] = Field(default_factory=list, description="Major narrative beats")
    progression_tracks: list[ProgressionTrackInfo] = Field(default_factory=list, description="Progression layers")
    live_events: list[LiveServiceEventInfo] = Field(default_factory=list, description="Live events or expansions")
    accessibility_features: list[AccessibilityFeatureInfo] = Field(default_factory=list, description="Accessibility support")
    audio_design: list[AudioDesignCue] = Field(default_factory=list, description="Audio design and score highlights")

    @staticmethod
    def get_instructions(additional_info: Sequence[str] | None = None) -> str:
        return compose_instructions(instructions, additional_info)

    @staticmethod
    def get_user_prompt(name: str) -> str:
        return "Provide an RPG leadership brief for '" + name + "', covering setting, factions, classes, companions, branching choices, monetisation, and post-launch narrative plans."

    @staticmethod
    def json_format_instructions() -> str:
        return (
            instructions + "\nOUTPUT FORMAT:\nReturn JSON with keys such as title, game_summary, core_loop, world_setting, timeline_context, protagonist_identity, release_year, "
            "estimated_campaign_hours, build_flexibility, choice_consequence_map, monetisation_model, post_launch_story_plan, developers, publishers, platform_releases, "
            "factions, character_classes, companions, systems, narrative_beats, progression_tracks, live_events, accessibility_features, audio_design."
        )

    def _summary_panel(self) -> tuple[str, Sequence[str], str]:
        title = self.title or self.summary_title_fallback
        lines = [line for line in (self.core_loop, self.game_summary) if isinstance(line, str) and line.strip()]
        if not lines:
            lines.append("(no summary provided)")
        return title, lines, self.summary_panel_style

    def _fact_pairs(self) -> Sequence[tuple[str, str]]:
        return [
            ("Release Year", format_year(self.release_year)),
            ("Campaign Hours", format_number(self.estimated_campaign_hours) if self.estimated_campaign_hours else "-"),
            ("Build Flexibility", self.build_flexibility or "-"),
            ("Choices", self.choice_consequence_map or "-"),
            ("Monetisation", self.monetisation_model or "-"),
        ]

    def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence]]:
        sections: list[tuple[str, List[TableSchema], Sequence]] = []
        if self.developers:
            sections.append(("Developers", StudioProfile.table_schema(), self.developers))
        if self.publishers:
            sections.append(("Publishers", StudioProfile.table_schema(), self.publishers))
        if self.platform_releases:
            sections.append(("Platform Releases", PlatformReleaseInfo.table_schema(), self.platform_releases))
        if self.factions:
            sections.append(("Factions", FactionProfile.table_schema(), self.factions))
        if self.character_classes:
            sections.append(("Character Classes", CharacterClassProfile.table_schema(), self.character_classes))
        if self.companions:
            sections.append(("Companions", CompanionProfile.table_schema(), self.companions))
        if self.systems:
            sections.append(("Systems", GameplayMechanicHighlight.table_schema(), self.systems))
        if self.narrative_beats:
            sections.append(("Narrative Beats", NarrativeBeatInfo.table_schema(), self.narrative_beats))
        if self.progression_tracks:
            sections.append(("Progression", ProgressionTrackInfo.table_schema(), self.progression_tracks))
        if self.live_events:
            sections.append(("Live Ops", LiveServiceEventInfo.table_schema(), self.live_events))
        if self.accessibility_features:
            sections.append(("Accessibility", AccessibilityFeatureInfo.table_schema(), self.accessibility_features))
        if self.audio_design:
            sections.append(("Audio Design", AudioDesignCue.table_schema(), self.audio_design))
        return sections

    def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
        world_lines = []
        if self.world_setting:
            world_lines.append(f"World: {self.world_setting}")
        if self.timeline_context:
            world_lines.append(f"Timeline: {self.timeline_context}")
        if self.post_launch_story_plan:
            world_lines.append(f"Post-Launch: {self.post_launch_story_plan}")
        world_panel = "\n".join(world_lines)

        protagonist_lines = []
        if self.protagonist_identity:
            protagonist_lines.append(f"Protagonist: {self.protagonist_identity}")
        if self.build_flexibility:
            protagonist_lines.append(f"Build Freedom: {self.build_flexibility}")
        protagonist_panel = "\n".join(protagonist_lines)

        return [
            ("Worldbuilding", world_panel, "cyan"),
            ("Player Fantasy", protagonist_panel, "magenta"),
        ]


__all__ = [
    "RolePlayingGameInfo",
    "CharacterClassProfile",
    "CompanionProfile",
    "FactionProfile",
]
