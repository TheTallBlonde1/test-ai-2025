"""Fantasy and science-fiction movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import ActionSetPieceInfo, BaseMovieInfo


class FantasyScienceFictionMovieInfo(BaseMovieInfo):
    """Speculative fiction film representation."""

    model_name: ClassVar[str] = "FantasyScienceFictionMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for fantasy and science fiction movies that construct imaginative worlds, technology frontiers, or supernatural systems."
    key_trait: ClassVar[str] = "Feature-length speculative storytelling anchored in layered world-building."
    instructions: ClassVar[str] = "Adopt the voice of a speculative film curator delivering an in-depth brief on a fantasy or science-fiction movie. Cover world-building pillars, technology or magic systems, major factions, mythology, visual effects collaborators, allegorical themes, and spectacle moments."
    label: ClassVar[str] = "fantasy/science-fiction movie"
    user_prompt_template: ClassVar[str] = "Outline the fantasy or science-fiction movie '{title}', emphasizing lore, technology or magic frameworks, key factions, and signature spectacle sequences."

    world_building_elements: list[str] = Field(
        default_factory=list,
        description="Key elements that define the world or universe",
    )
    technology_or_magic: list[str] = Field(
        default_factory=list,
        description="Notable technology, magic systems, or powers",
    )
    factions: list[str] = Field(
        default_factory=list,
        description="Factions, species, or cultures featured in the narrative",
    )
    mythology_notes: str = Field("", description="Important lore or mythology underpinning the story")
    timeline: str = Field("", description="Setting timeline or era relevant to the narrative")
    visual_effects_partners: list[str] = Field(
        default_factory=list,
        description="Studios or partners responsible for VFX or creature work",
    )
    signature_set_pieces: list[ActionSetPieceInfo] = Field(
        default_factory=list,
        description="Spectacle-driven sequences or battles",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.timeline:
            facts.append(("Timeline", self.timeline))
        if self.mythology_notes:
            facts.append(("Mythology", self.mythology_notes))
        return facts

    def _extra_tables(self):
        tables = []
        if self.signature_set_pieces:
            tables.append(("Signature Set Pieces", ActionSetPieceInfo.table_schema(), self.signature_set_pieces))
        return tables

    def _extra_panels(self):
        panels = []
        if self.world_building_elements:
            body = "\n".join(f"- {item}" for item in self.world_building_elements)
            panels.append(("World Building", body))
        if self.technology_or_magic:
            tech_body = "\n".join(f"- {item}" for item in self.technology_or_magic)
            panels.append(("Technology / Magic", tech_body))
        if self.factions:
            faction_body = "\n".join(f"- {faction}" for faction in self.factions)
            panels.append(("Factions", faction_body))
        if self.visual_effects_partners:
            vfx_body = "\n".join(f"- {partner}" for partner in self.visual_effects_partners)
            panels.append(("VFX Partners", vfx_body))
        return panels


__all__ = ["FantasyScienceFictionMovieInfo"]
