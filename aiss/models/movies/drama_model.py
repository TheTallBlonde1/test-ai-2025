"""Drama movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import BaseMovieInfo, CharacterArcInfo


class DramaMovieInfo(BaseMovieInfo):
    """Emotionally driven drama film representation."""

    model_name: ClassVar[str] = "DramaMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for drama movies that explore nuanced character journeys, social dilemmas, and emotional catharsis."
    key_trait: ClassVar[str] = "Feature-length character storytelling grounded in emotional stakes."
    instructions: ClassVar[str] = "Serve as a prestige drama analyst compiling a character-driven profile of a drama movie. Illuminate the emotional stakes, moral conflicts, transformative performances, production context, awards trajectory, and cultural impact."
    label: ClassVar[str] = "drama movie"
    user_prompt_template: ClassVar[str] = "Provide a layered breakdown of the drama movie '{title}', highlighting emotional arcs, character growth, and production insights."

    themes: list[str] = Field(default_factory=list, description="Core thematic ideas explored by the drama")
    central_conflict: str = Field(
        "",
        description="The primary emotional or moral conflict propelling the story",
    )
    character_arcs: list[CharacterArcInfo] = Field(
        default_factory=list,
        description="Detailed arcs for principal characters",
    )
    tone: str = Field("", description="Overall tone or mood of the drama")
    pivotal_moments: list[str] = Field(
        default_factory=list,
        description="Key dramatic moments that reshape characters or conflict",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.central_conflict:
            facts.append(("Conflict", self.central_conflict))
        if self.tone:
            facts.append(("Tone", self.tone))
        return facts

    def _extra_tables(self):
        tables = []
        if self.character_arcs:
            tables.append(("Character Arcs", CharacterArcInfo.table_schema(), self.character_arcs))
        return tables

    def _extra_panels(self):
        panels = []
        if self.themes:
            themes_body = "\n".join(f"- {theme}" for theme in self.themes)
            panels.append(("Themes", themes_body))
        if self.pivotal_moments:
            pivotal_body = "\n".join(f"- {moment}" for moment in self.pivotal_moments)
            panels.append(("Pivotal Moments", pivotal_body))
        return panels


__all__ = ["DramaMovieInfo"]
