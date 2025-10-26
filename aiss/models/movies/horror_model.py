"""Horror movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import BaseMovieInfo, FearMomentInfo


class HorrorMovieInfo(BaseMovieInfo):
    """Horror film representation."""

    model_name: ClassVar[str] = "HorrorMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for horror movies engineered to provoke dread through atmosphere, threat design, and psychological unease."
    key_trait: ClassVar[str] = "Feature-length horror storytelling orchestrating fear, tension, and survival stakes."
    instructions: ClassVar[str] = "Operate as a genre programming executive delivering a definitive horror movie dossier. Detail the subgenre, threat entities, scare construction, survival trajectories, thematic undercurrents, and production craft that amplify dread."
    label: ClassVar[str] = "horror movie"
    user_prompt_template: ClassVar[str] = "Deliver an in-depth horror movie breakdown for '{title}', emphasizing threat design, scare tactics, survivors, and thematic commentary."

    subgenre: str = Field("", description="Specific horror subgenre (psychological, slasher, etc.)")
    threat_entities: list[str] = Field(
        default_factory=list,
        description="Primary antagonistic entities or forces",
    )
    fear_moments: list[FearMomentInfo] = Field(
        default_factory=list,
        description="Major scare or dread moments",
    )
    gore_level: str = Field("", description="Description of gore intensity")
    atmosphere: str = Field("", description="Tone or atmosphere (claustrophobic, surreal, etc.)")
    final_survivors: list[str] = Field(
        default_factory=list,
        description="Characters that survive or their final fates",
    )
    thematic_notes: list[str] = Field(
        default_factory=list,
        description="Underlying societal or psychological themes",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.subgenre:
            facts.append(("Subgenre", self.subgenre))
        if self.gore_level:
            facts.append(("Gore", self.gore_level))
        if self.atmosphere:
            facts.append(("Atmosphere", self.atmosphere))
        return facts

    def _extra_tables(self):
        tables = []
        if self.fear_moments:
            tables.append(("Fear Moments", FearMomentInfo.table_schema(), self.fear_moments))
        return tables

    def _extra_panels(self):
        panels = []
        if self.threat_entities:
            threats = "\n".join(f"- {entity}" for entity in self.threat_entities)
            panels.append(("Threat Entities", threats))
        if self.final_survivors:
            survivors = "\n".join(f"- {survivor}" for survivor in self.final_survivors)
            panels.append(("Final Survivors", survivors))
        if self.thematic_notes:
            themes = "\n".join(f"- {note}" for note in self.thematic_notes)
            panels.append(("Themes", themes))
        return panels


__all__ = ["HorrorMovieInfo"]
