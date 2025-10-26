"""Thriller, mystery, and crime movie format definitions."""

from typing import ClassVar

from pydantic import Field

from ._base import BaseMovieInfo, InvestigationThreadInfo


class ThrillerMysteryCrimeMovieInfo(BaseMovieInfo):
    """Suspenseful thriller/mystery/crime film representation."""

    model_name: ClassVar[str] = "ThrillerMysteryCrimeMovieInfo"
    description: ClassVar[str] = "Cinematic intelligence model for thriller, mystery, and crime movies driven by investigations, deception, and psychological stakes."
    key_trait: ClassVar[str] = "Feature-length suspense narratives built on investigations, twists, and escalating tension."
    instructions: ClassVar[str] = "Adopt the vantage of a thriller acquisitions executive crafting a suspense brief on a thriller, mystery, or crime movie. Detail the central mystery, investigative threads, suspects, reveals, mood, production atmosphere choices, and audience payoff."
    label: ClassVar[str] = "thriller/mystery/crime movie"
    user_prompt_template: ClassVar[str] = "Summarize the thriller, mystery, or crime movie '{title}', focusing on investigative structure, suspects, twists, and tonal mood."

    narrative_hook: str = Field("", description="Opening hook or inciting incident of the mystery")
    investigation_threads: list[InvestigationThreadInfo] = Field(
        default_factory=list,
        description="Active investigation threads tracked throughout the story",
    )
    twists: list[str] = Field(default_factory=list, description="Major twists or reveals")
    suspects: list[str] = Field(default_factory=list, description="List of suspects or persons of interest")
    law_enforcement_agencies: list[str] = Field(
        default_factory=list,
        description="Agencies or teams involved in the investigation",
    )
    tension_profile: str = Field("", description="Description of pacing/tension progression")
    evidence_chain: list[str] = Field(
        default_factory=list,
        description="Sequence of critical evidence that drives the case",
    )

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        if self.narrative_hook:
            facts.append(("Hook", self.narrative_hook))
        if self.tension_profile:
            facts.append(("Tension", self.tension_profile))
        return facts

    def _extra_tables(self):
        tables = []
        if self.investigation_threads:
            tables.append(("Investigation Threads", InvestigationThreadInfo.table_schema(), self.investigation_threads))
        return tables

    def _extra_panels(self):
        panels = []
        if self.twists:
            twist_body = "\n".join(f"- {twist}" for twist in self.twists)
            panels.append(("Twists", twist_body))
        if self.suspects:
            suspect_body = "\n".join(f"- {suspect}" for suspect in self.suspects)
            panels.append(("Suspects", suspect_body))
        if self.evidence_chain:
            evidence_body = "\n".join(f"- {item}" for item in self.evidence_chain)
            panels.append(("Evidence Chain", evidence_body))
        if self.law_enforcement_agencies:
            agencies_body = "\n".join(f"- {agency}" for agency in self.law_enforcement_agencies)
            panels.append(("Agencies", agencies_body))
        return panels


__all__ = ["ThrillerMysteryCrimeMovieInfo"]
