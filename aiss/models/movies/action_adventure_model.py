"""Action and adventure movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import ActionSetPieceInfo, BaseMovieInfo


class ActionAdventureMovieInfo(BaseMovieInfo):
    """High-energy action or adventure film representation."""

    model_name: ClassVar[str] = "ActionAdventureMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for high-octane action and adventure movies, spotlighting spectacle, heroism, and global stakes."
    key_trait: ClassVar[str] = "Feature-length action narratives built around escalating set pieces and dynamic locales."
    instructions: ClassVar[str] = "Act as a theatrical action analyst delivering a definitive breakdown of an action-adventure movie. Cover the hero's mission, antagonistic forces, marquee set pieces, stunt choreography, tactical gear, and global stakes alongside production scale and release positioning."
    label: ClassVar[str] = "action-adventure movie"
    user_prompt_template: ClassVar[str] = "Create an action-adventure movie breakdown for '{title}', highlighting hero motivation, villains, signature set pieces, stunt craftsmanship, and production scale."

    hero_motivation: str = Field("", description="Driving motivation or mission for the hero")
    primary_locales: list[str] = Field(
        default_factory=list,
        description="Key locations or regions visited during the film",
    )
    antagonists: list[str] = Field(
        default_factory=list,
        description="Primary antagonists or opposing forces",
    )
    gear_and_tech: list[str] = Field(
        default_factory=list,
        description="Signature weapons, vehicles, gadgets, or technology featured",
    )
    stunt_team: list[str] = Field(
        default_factory=list,
        description="Notable stunt coordinators or second-unit directors",
    )
    set_pieces: list[ActionSetPieceInfo] = Field(
        default_factory=list,
        description="Major action set pieces structured throughout the film",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.hero_motivation:
            facts.append(("Hero Motivation", self.hero_motivation))
        if self.primary_locales:
            locales = ", ".join(self.primary_locales)
            facts.append(("Locales", locales))
        return facts

    def _extra_tables(self):
        tables = []
        if self.set_pieces:
            tables.append(("Set Pieces", ActionSetPieceInfo.table_schema(), self.set_pieces))
        return tables

    def _extra_panels(self):
        panels = []
        if self.antagonists:
            body = "\n".join(f"- {antagonist}" for antagonist in self.antagonists)
            panels.append(("Antagonists", body))
        if self.gear_and_tech:
            gear_body = "\n".join(f"- {item}" for item in self.gear_and_tech)
            panels.append(("Gear & Tech", gear_body))
        if self.stunt_team:
            stunt_body = "\n".join(f"- {name}" for name in self.stunt_team)
            panels.append(("Stunt Team", stunt_body))
        return panels


__all__ = ["ActionAdventureMovieInfo"]
