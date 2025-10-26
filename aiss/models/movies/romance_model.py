"""Romance movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import BaseMovieInfo, RomanticBeatInfo


class RomanceMovieInfo(BaseMovieInfo):
    """Romantic film representation."""

    model_name: ClassVar[str] = "RomanceMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for romance movies centered on intimacy, emotional risk, and relational growth."
    key_trait: ClassVar[str] = "Feature-length love stories built around relationship dynamics and vulnerability."
    instructions: ClassVar[str] = "Act as a romance development executive summarizing a romance movie. Detail the relationship arcs, emotional beats, conflicts, supporting ensemble, chemistry observations, and ultimate resolution."
    label: ClassVar[str] = "romance movie"
    user_prompt_template: ClassVar[str] = "Describe the romance movie '{title}', focusing on relationship dynamics, key romantic beats, conflicts, and resolution."

    relationship_dynamics: list[str] = Field(
        default_factory=list,
        description="Key dynamics between romantic leads",
    )
    meet_cute_description: str = Field(
        "",
        description="Description of how the leads meet or reconnect",
    )
    romantic_beats: list[RomanticBeatInfo] = Field(
        default_factory=list,
        description="Major romantic beats throughout the narrative",
    )
    conflict_obstacles: list[str] = Field(
        default_factory=list,
        description="Obstacles preventing the relationship from succeeding",
    )
    ending_type: str = Field("", description="Resolution type (happy, bittersweet, ambiguous)")
    chemistry_notes: str = Field(
        "",
        description="Observations about on-screen chemistry or performance interplay",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.meet_cute_description:
            facts.append(("Meet-Cute", self.meet_cute_description))
        if self.ending_type:
            facts.append(("Ending", self.ending_type))
        return facts

    def _extra_tables(self):
        tables = []
        if self.romantic_beats:
            tables.append(("Romantic Beats", RomanticBeatInfo.table_schema(), self.romantic_beats))
        return tables

    def _extra_panels(self):
        panels = []
        if self.relationship_dynamics:
            dynamics = "\n".join(f"- {item}" for item in self.relationship_dynamics)
            panels.append(("Relationship Dynamics", dynamics))
        if self.conflict_obstacles:
            conflicts = "\n".join(f"- {item}" for item in self.conflict_obstacles)
            panels.append(("Conflicts", conflicts))
        if self.chemistry_notes:
            panels.append(("Chemistry", self.chemistry_notes))
        return panels


__all__ = ["RomanceMovieInfo"]
