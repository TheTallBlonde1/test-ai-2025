"""Comedy movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import BaseMovieInfo, HumorBeatInfo


class ComedyMovieInfo(BaseMovieInfo):
    """Light-hearted comedy film representation."""

    model_name: ClassVar[str] = "ComedyMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for comedy movies, balancing comedic voice, ensemble dynamics, and cultural resonance."
    key_trait: ClassVar[str] = "Feature-length comedy storytelling driven by rhythmic humour beats and character chemistry."
    instructions: ClassVar[str] = "Serve as a comedy development executive producing a definitive profile of a comedy movie. Highlight the humour styles at play, ensemble dynamics, hallmark set pieces, improvisational flair, standout comedic beats, and audience appeal alongside release positioning."
    label: ClassVar[str] = "comedy movie"
    user_prompt_template: ClassVar[str] = "Develop a detailed comedy movie breakdown for '{title}', covering humour styles, standout moments, ensemble chemistry, and production context."

    humor_styles: list[str] = Field(
        default_factory=list,
        description="Humor approaches used (satire, slapstick, situational, etc.)",
    )
    comedic_beats: list[HumorBeatInfo] = Field(
        default_factory=list,
        description="Signature comedic beats within the film",
    )
    running_gags: list[str] = Field(
        default_factory=list,
        description="Recurring jokes or comedic motifs",
    )
    improv_notes: str = Field(
        "",
        description="Notable improvisational moments or performers known for improv",
    )
    tone: str = Field("", description="Overall comedic tone (raucous, heartfelt, satirical, etc.)")
    cameo_appearances: list[str] = Field(
        default_factory=list,
        description="Notable cameo appearances that add comedic surprise",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.tone:
            facts.append(("Tone", self.tone))
        if self.improv_notes:
            facts.append(("Improv", self.improv_notes))
        return facts

    def _extra_tables(self):
        tables = []
        if self.comedic_beats:
            tables.append(("Comedic Beats", HumorBeatInfo.table_schema(), self.comedic_beats))
        return tables

    def _extra_panels(self):
        panels = []
        if self.humor_styles:
            body = "\n".join(f"- {style}" for style in self.humor_styles)
            panels.append(("Humor Styles", body))
        if self.running_gags:
            gags = "\n".join(f"- {gag}" for gag in self.running_gags)
            panels.append(("Running Gags", gags))
        if self.cameo_appearances:
            cameos = "\n".join(f"- {cameo}" for cameo in self.cameo_appearances)
            panels.append(("Cameos", cameos))
        return panels


__all__ = ["ComedyMovieInfo"]
