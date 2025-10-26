"""Documentary and biographical movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import BaseMovieInfo, SubjectFocusInfo


class DocumentaryBiographicalMovieInfo(BaseMovieInfo):
    """Non-fiction or biographical film representation."""

    model_name: ClassVar[str] = "DocumentaryBiographicalMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for documentary and biographical movies that illuminate real people, issues, and events."
    key_trait: ClassVar[str] = "Fact-driven feature storytelling anchored in real-world insight."
    instructions: ClassVar[str] = "Operate as a documentary film strategist summarizing a documentary or biographical movie. Cover the primary subjects, narrative scope, research rigor, archival materials, interview perspectives, creative liberties, and broader cultural or societal impact."
    label: ClassVar[str] = "documentary/biographical movie"
    user_prompt_template: ClassVar[str] = "Describe the documentary or biographical movie '{title}', focusing on subjects, narrative framing, research depth, and impact."

    subjects: list[SubjectFocusInfo] = Field(
        default_factory=list,
        description="Primary subjects or individuals covered",
    )
    narrative_scope: str = Field(
        "",
        description="Scope of the story (personal journey, historical overview, investigative)",
    )
    primary_sources: list[str] = Field(
        default_factory=list,
        description="Archival materials, documents, or research sources used",
    )
    interviewees: list[str] = Field(
        default_factory=list,
        description="Notable interviewees or commentators",
    )
    historical_accuracy_notes: str = Field(
        "",
        description="Notes on accuracy, creative liberties, or debated points",
    )
    distribution_platforms: list[str] = Field(
        default_factory=list,
        description="Platforms or networks where the documentary premiered",
    )
    call_to_action: str = Field(
        "",
        description="Any advocacy or call-to-action presented by the film",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.narrative_scope:
            facts.append(("Scope", self.narrative_scope))
        if self.call_to_action:
            facts.append(("Call to Action", self.call_to_action))
        if self.historical_accuracy_notes:
            facts.append(("Accuracy", self.historical_accuracy_notes))
        return facts

    def _extra_tables(self):
        tables = []
        if self.subjects:
            tables.append(("Subjects", SubjectFocusInfo.table_schema(), self.subjects))
        return tables

    def _extra_panels(self):
        panels = []
        if self.primary_sources:
            sources = "\n".join(f"- {source}" for source in self.primary_sources)
            panels.append(("Primary Sources", sources))
        if self.interviewees:
            interviews = "\n".join(f"- {person}" for person in self.interviewees)
            panels.append(("Interviewees", interviews))
        if self.distribution_platforms:
            platforms = "\n".join(f"- {platform}" for platform in self.distribution_platforms)
            panels.append(("Distribution", platforms))
        return panels


__all__ = ["DocumentaryBiographicalMovieInfo"]
