"""Shared movie model base classes and helpers.

This module houses the reusable building blocks shared across all movie
formats. Each concrete movie format (drama, comedy, etc.) extends
:class:`BaseMovieInfo` and reuses the nested helper models defined here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar, Iterable, List, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

from aiss.utils import format_decimal, format_money, format_runtime_minutes, format_year, render_table_from_schema

from ..shared import TableSchema, compose_instructions

# Reusable helper type for BaseModel factories
T = TypeVar("T", bound=BaseModel)


def _model_dump(instance: BaseModel) -> dict[str, Any]:  # pragma: no cover - trivial helper
    try:
        return instance.model_dump(mode="python")  # type: ignore[attr-defined]
    except AttributeError:
        return instance.dict()  # type: ignore[call-arg]


def _model_validate(cls: Type[T], data: Any) -> T:  # pragma: no cover - trivial helper
    try:
        return cls.model_validate(data)  # type: ignore[attr-defined]
    except AttributeError:
        return cls.parse_obj(data)  # type: ignore[call-arg]


# MARK: Cast and Crew Helpers
class CastMemberInfo(BaseModel):
    """Principal cast member information."""

    character: str = Field("", description="Name of character in the movie")
    actor: str = Field("", description="Actor who played the character")
    role: str = Field("", description="Role type (lead/supporting/guest)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        """Return the table schema for rendering cast information."""

        return [
            TableSchema(name="character", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="role", header="Role", style="yellow"),
        ]

    def to_dict(self) -> dict[str, Any]:
        return _model_dump(self)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CastMemberInfo":
        return _model_validate(cls, data)

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "CastMemberInfo":
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


class CrewMemberInfo(BaseModel):
    """Notable crew member information beyond directors/producers."""

    name: str = Field("", description="Crew member name")
    role: str = Field("", description="Primary contribution (editor, DP, etc.)")
    notable_work: str = Field("", description="Past notable credits or accolades")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(name="role", header="Role", style="cyan"),
            TableSchema(name="notable_work", header="Notable Work", style="yellow"),
        ]

    def to_dict(self) -> dict[str, Any]:
        return _model_dump(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrewMemberInfo":
        return _model_validate(cls, data)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "CrewMemberInfo":
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


class ProductionCompanyInfo(BaseModel):
    """Production company involvement details."""

    name: str = Field("", description="Name of the production company")
    founded_year: int = Field(0, description="Year the production company was founded")
    start_year: int = Field(0, description="Year the company started working on the movie")
    end_year: int = Field(0, description="Year the company stopped working on the movie")
    country: str = Field("", description="Country where the production company is based")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(
                name="founded_year",
                header="Founded",
                justify="center",
                formatter=format_year,
            ),
            TableSchema(
                name="start_year",
                header="Start",
                justify="center",
                formatter=format_year,
            ),
            TableSchema(
                name="end_year",
                header="End",
                justify="center",
                formatter=format_year,
            ),
            TableSchema(name="country", header="Country", style="cyan"),
        ]

    def to_dict(self) -> dict[str, Any]:
        return _model_dump(self)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProductionCompanyInfo":
        return _model_validate(cls, data)

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "ProductionCompanyInfo":
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


class BoxOfficeInfo(BaseModel):
    """Aggregated box office and budget information."""

    budget: Optional[int] = Field(None, description="Budget in local currency or smallest unit")
    gross_worldwide: Optional[int] = Field(None, description="Worldwide gross")
    gross_domestic: Optional[int] = Field(None, description="Domestic gross")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(
                name="budget",
                header="Budget",
                style="magenta",
                justify="right",
                formatter=format_money,
            ),
            TableSchema(
                name="gross_worldwide",
                header="Gross (WW)",
                style="cyan",
                justify="right",
                formatter=format_money,
            ),
            TableSchema(
                name="gross_domestic",
                header="Gross (Domestic)",
                style="yellow",
                justify="right",
                formatter=format_money,
            ),
        ]

    def to_dict(self) -> dict[str, Any]:
        return _model_dump(self)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BoxOfficeInfo":
        return _model_validate(cls, data)

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "BoxOfficeInfo":
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


class DistributionInfo(BaseModel):
    """Distribution details for a movie (territory-specific releases)."""

    distributor: str = Field("", description="Name of the distributor")
    territory: str = Field("", description="Territory / country of distribution")
    release_type: str = Field("", description="Type of release (theatrical, streaming, etc.)")
    start_year: int = Field(0, description="Year distribution started in the territory")
    end_year: int = Field(0, description="Year distribution ended in the territory, if applicable")
    revenue: Optional[int] = Field(None, description="Reported revenue for this territory (if available)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="distributor", header="Distributor", style="magenta", no_wrap=True),
            TableSchema(name="territory", header="Territory", style="cyan"),
            TableSchema(name="release_type", header="Type", style="yellow"),
            TableSchema(name="start_year", header="Start", justify="center", formatter=format_year),
            TableSchema(name="end_year", header="End", justify="center", formatter=format_year),
            TableSchema(name="revenue", header="Revenue", justify="right", formatter=format_money),
        ]

    def to_dict(self) -> dict[str, Any]:
        return _model_dump(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DistributionInfo":
        return _model_validate(cls, data)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "DistributionInfo":
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


# MARK: Genre-Specific Helper Models
class CharacterArcInfo(BaseModel):
    """Detailed character journey information used in character-driven movies."""

    name: str = Field("", description="Character name")
    portrayed_by: str = Field("", description="Actor portraying the character")
    arc_summary: str = Field("", description="Summary of the character's emotional journey")
    motivation: str = Field("", description="Primary driving motivation")
    turning_points: list[str] = Field(
        default_factory=list,
        description="Key turning points that reshape the character",
    )
    resolution_status: str = Field(
        "",
        description="Where the character ends the story (resolved, tragic, ambiguous, etc.)",
    )

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="portrayed_by", header="Actor", style="cyan"),
            TableSchema(name="motivation", header="Motivation", style="yellow"),
            TableSchema(name="resolution_status", header="Resolution", style="green"),
        ]


class ActionSetPieceInfo(BaseModel):
    """Set piece information for action or spectacle-driven movies."""

    name: str = Field("", description="Name or description of the set piece")
    act: str = Field("", description="Act or placement in the film structure")
    location: str = Field("", description="Primary location of the sequence")
    stakes: str = Field("", description="Immediate stakes or goals during the sequence")
    practical_effects: str = Field("", description="Notable stunts, VFX, or practical work")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Set Piece", style="magenta", no_wrap=True),
            TableSchema(name="act", header="Act", justify="center"),
            TableSchema(name="location", header="Location", style="cyan"),
            TableSchema(name="stakes", header="Stakes", style="yellow"),
            TableSchema(name="practical_effects", header="Execution", style="green"),
        ]


class HumorBeatInfo(BaseModel):
    """Major comedic beats tracked for comedy movies."""

    situation: str = Field("", description="Setup for the comedic beat")
    punchline: str = Field("", description="Primary comedic payoff")
    characters_involved: list[str] = Field(
        default_factory=list,
        description="Characters delivering or affected by the beat",
    )
    comedic_style: str = Field("", description="Type of humor (satire, slapstick, deadpan, etc.)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="situation", header="Situation", style="magenta"),
            TableSchema(name="punchline", header="Payoff", style="cyan"),
            TableSchema(name="comedic_style", header="Style", style="yellow"),
        ]


class InvestigationThreadInfo(BaseModel):
    """Used for thriller/mystery plots to track investigative threads."""

    thread: str = Field("", description="Name or short description of the investigation thread")
    suspect_or_focus: str = Field("", description="Primary suspect, victim, or focus of this thread")
    clues: list[str] = Field(default_factory=list, description="Key clues uncovered in this thread")
    status: str = Field("", description="Current status (active, resolved, red herring)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="thread", header="Thread", style="magenta"),
            TableSchema(name="suspect_or_focus", header="Focus", style="cyan"),
            TableSchema(name="status", header="Status", style="yellow"),
        ]


class RomanticBeatInfo(BaseModel):
    """Romantic beat tracking for romance-driven stories."""

    beat_name: str = Field("", description="Name of the romantic beat")
    description: str = Field("", description="What happens during this beat")
    emotional_shift: str = Field("", description="How the relationship evolves")
    setting: str = Field("", description="Where the beat occurs")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="beat_name", header="Beat", style="magenta"),
            TableSchema(name="emotional_shift", header="Emotional Shift", style="cyan"),
            TableSchema(name="setting", header="Setting", style="yellow"),
        ]


class FearMomentInfo(BaseModel):
    """Major scare or tension moments for horror movies."""

    moment_name: str = Field("", description="Identifier for the scare or tension beat")
    type_of_fear: str = Field("", description="Fear driver (jump scare, dread, body horror, etc.)")
    setup: str = Field("", description="Lead-in that builds tension")
    payoff: str = Field("", description="Resulting scare or twist")
    survivors_involved: list[str] = Field(
        default_factory=list,
        description="Characters involved or affected",
    )

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="moment_name", header="Moment", style="magenta"),
            TableSchema(name="type_of_fear", header="Fear Type", style="cyan"),
            TableSchema(name="payoff", header="Payoff", style="yellow"),
        ]


class SubjectFocusInfo(BaseModel):
    """Subject focus details for documentaries or biographical films."""

    subject: str = Field("", description="Primary subject or individual")
    role_or_significance: str = Field("", description="Why the subject is important")
    time_period: str = Field("", description="Time period covered for this subject")
    perspective: str = Field("", description="Narrative perspective or framing")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="subject", header="Subject", style="magenta"),
            TableSchema(name="role_or_significance", header="Significance", style="cyan"),
            TableSchema(name="time_period", header="Time Period", style="yellow"),
            TableSchema(name="perspective", header="Perspective", style="green"),
        ]


# MARK: Base Movie Format
class BaseMovieInfo(BaseModel):
    """Base class shared by all movie formats implementing the protocol."""

    model_name: ClassVar[str]
    description: ClassVar[str]
    key_trait: ClassVar[str]
    instructions: ClassVar[str]
    label: ClassVar[str] = "movie"
    user_prompt_template: ClassVar[str] = "Tell me about the {label} '{title}' in depth."

    title: str = Field("", description="Movie title")
    tagline: str = Field("", description="Marketing tagline or hook")
    synopsis: str = Field("", description="Short synopsis of the movie")
    release_year: int = Field(0, description="Year the movie was released")
    runtime_minutes: int = Field(0, description="Runtime in minutes")
    genres: list[str] = Field(default_factory=list, description="List of genres")
    mpaa_rating: str = Field("", description="Content rating (e.g., PG-13)")
    directors: list[str] = Field(default_factory=list, description="List of directors")
    writers: list[str] = Field(default_factory=list, description="List of writers")
    producers: list[str] = Field(default_factory=list, description="List of producers")
    original_language: str = Field("", description="Original spoken language")
    countries: list[str] = Field(default_factory=list, description="Countries of production")
    rating: Optional[float] = Field(None, description="Average critic or audience rating")
    keywords: list[str] = Field(default_factory=list, description="Key thematic keywords")
    cast: list[CastMemberInfo] = Field(default_factory=list, description="Main cast members")
    notable_crew: list[CrewMemberInfo] = Field(default_factory=list, description="Notable crew beyond the core team")
    production_companies: list[ProductionCompanyInfo] = Field(
        default_factory=list,
        description="Production companies involved",
    )
    box_office: Optional[BoxOfficeInfo] = Field(None, description="Box office / budget info")
    distribution_info: list[DistributionInfo] = Field(
        default_factory=list,
        description="Distribution entries for the movie",
    )
    awards: list[str] = Field(default_factory=list, description="Awards and nominations")
    soundtrack_highlights: list[str] = Field(
        default_factory=list,
        description="Notable soundtrack cues, songs, or composers",
    )
    wikipedia_summary: str = Field(
        "",
        exclude=True,
        description="Runtime-only hint populated after parsing for richer rendering.",
    )

    # Generic protocol compliance helpers -------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        """Serialize the movie info to a plain dictionary suitable for JSON."""

        return _model_dump(self)

    def to_json(self, json_file_path: Path | str) -> None:
        """Persist the movie info as JSON on disk."""

        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        """Construct the movie format from a mapping of values."""

        return _model_validate(cls, data)

    @classmethod
    def from_json(cls: Type[T], json_file_path: Path | str) -> T:
        """Load the movie format from a JSON file."""

        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)

    @classmethod
    def get_instructions(cls, additional_info: Sequence[str] | None = None) -> str:  # pragma: no cover - simple delegation
        return compose_instructions(cls.instructions, additional_info)

    @classmethod
    def get_user_prompt(cls, movie_title: str) -> str:  # pragma: no cover - simple delegation
        return cls.user_prompt_template.format(title=movie_title, label=cls.label)

    @classmethod
    def _json_schema(cls) -> str:
        try:
            schema = cls.model_json_schema()  # type: ignore[attr-defined]
        except AttributeError:
            schema = cls.schema()  # type: ignore[attr-defined]
        return json.dumps(schema, ensure_ascii=False, indent=2)

    @classmethod
    def json_format_instructions(cls) -> str:
        """Return instructions that include an explicit JSON schema example."""

        schema_text = cls._json_schema()
        return f"{cls.get_instructions()}\nRespond with JSON that adheres to the following schema:\n```json\n{schema_text}\n```"

    # Rendering helpers -------------------------------------------------------------------
    def _base_fact_pairs(self) -> list[tuple[str, str]]:
        facts: list[tuple[str, str]] = []
        release_display = format_year(self.release_year)
        facts.append(("Release", release_display))
        facts.append(("Runtime", format_runtime_minutes(self.runtime_minutes)))
        facts.append(("Genres", ", ".join(self.genres) if self.genres else "-"))
        facts.append(("MPAA", self.mpaa_rating or "-"))
        facts.append(("Directors", ", ".join(self.directors) if self.directors else "-"))
        facts.append(("Producers", ", ".join(self.producers) if self.producers else "-"))
        facts.append(("Writers", ", ".join(self.writers) if self.writers else "-"))
        facts.append(("Language", self.original_language or "-"))
        facts.append(("Countries", ", ".join(self.countries) if self.countries else "-"))
        facts.append(("Rating", format_decimal(self.rating) if self.rating is not None else "-"))
        return facts

    def _additional_fact_pairs(self) -> list[tuple[str, str]]:
        return []

    def _extra_tables(self) -> list[tuple[str, List[TableSchema], Sequence[BaseModel]]]:
        return []

    def _extra_panels(self) -> list[tuple[str, str]]:
        return []

    def _render_list_panel(self, title: str, items: Iterable[str], console: Console) -> None:
        data = list(items)
        if not data:
            return
        body = "\n".join(f"- {item}" for item in data)
        console.print(Panel(body, title=title, expand=False, style="blue"))

    def _render_wikipedia_summary(self, console: Console) -> None:
        hint_text = self.wikipedia_summary.strip()
        if not hint_text:
            return
        console.print(Panel(hint_text, title="Context", expand=False, style="yellow"))

    def render(self, console: Console) -> None:
        """Render the movie information using Rich primitives."""

        release_display = format_year(self.release_year)
        if self.title:
            if release_display and release_display != "-":
                title_text = f"{self.title} ({release_display})"
            else:
                title_text = self.title
        else:
            title_text = "(untitled)"
            if release_display and release_display != "-":
                title_text = f"{title_text} ({release_display})"
        synopsis_text = self.synopsis or "(no synopsis provided)"
        if self.tagline:
            synopsis_text = f"{self.tagline}\n\n{synopsis_text}".strip()
        console.print(Panel(synopsis_text, title=title_text, expand=False, style="green"))
        self._render_wikipedia_summary(console)

        facts = self._base_fact_pairs() + self._additional_fact_pairs()
        facts_text = ", ".join(f"{header}: {value}" for header, value in facts)
        console.print(Panel(facts_text, title="Facts", expand=False, style="magenta"))

        if self.keywords:
            self._render_list_panel("Keywords", self.keywords, console)
        if self.awards:
            self._render_list_panel("Awards", self.awards, console)
        if self.soundtrack_highlights:
            self._render_list_panel("Soundtrack", self.soundtrack_highlights, console)

        if self.cast:
            render_table_from_schema("Cast", CastMemberInfo.table_schema(), self.cast, console)
        if self.notable_crew:
            render_table_from_schema("Key Crew", CrewMemberInfo.table_schema(), self.notable_crew, console)
        if self.production_companies:
            render_table_from_schema(
                "Production Companies",
                ProductionCompanyInfo.table_schema(),
                self.production_companies,
                console,
            )
        if self.box_office:
            render_table_from_schema("Box Office", BoxOfficeInfo.table_schema(), [self.box_office], console)
        if self.distribution_info:
            render_table_from_schema(
                "Distribution",
                DistributionInfo.table_schema(),
                self.distribution_info,
                console,
            )

        for title, schema, rows in self._extra_tables():
            if rows:
                render_table_from_schema(title, schema, rows, console)

        for title, body in self._extra_panels():
            console.print(Panel(body, title=title, expand=False, style="cyan"))


__all__ = [
    "BaseMovieInfo",
    "CastMemberInfo",
    "CrewMemberInfo",
    "ProductionCompanyInfo",
    "BoxOfficeInfo",
    "DistributionInfo",
    "CharacterArcInfo",
    "ActionSetPieceInfo",
    "HumorBeatInfo",
    "InvestigationThreadInfo",
    "RomanticBeatInfo",
    "FearMomentInfo",
    "SubjectFocusInfo",
]
