"""Base helpers and shared show format data models.

Provides lightweight mixins shared across TV show format modules along
with the reusable data classes that were historically defined in
``show_model``. Consolidating them here keeps the imports local to the
``shows`` package while allowing other modules (tests, OpenAI helpers)
to access the same abstractions from a single place.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ClassVar, List, Optional, Sequence, TypeVar

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

from aiss.utils import (
    format_decimal,
    format_money,
    format_number,
    format_percentage,
    format_year,
    render_table_from_schema,
)

from ..protocols import ModelFormatProtocol
from ..shared import TableSchema


def _dump(obj: BaseModel) -> dict[str, Any]:
    """Return a plain dict for any Pydantic model, supporting v1/v2 APIs."""

    model_dump: Callable[[], dict[str, Any]] | None = getattr(obj, "model_dump", None)  # type: ignore[assignment]
    if callable(model_dump):
        return model_dump()
    legacy_dump: Callable[[], dict[str, Any]] | None = getattr(obj, "dict", None)
    if callable(legacy_dump):
        return legacy_dump()
    raise TypeError(f"Object {obj!r} does not support model_dump/dict")


T = TypeVar("T", bound="JsonModel")


class JsonModel(BaseModel):
    """Extend Pydantic's BaseModel with convenient JSON helpers."""

    def to_dict(self) -> dict[str, Any]:
        return _dump(self)

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        return cls(**data)

    @classmethod
    def from_json(cls: type[T], json_file_path: Path | str) -> T:
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)


if TYPE_CHECKING:

    class ShowFormatBase(JsonModel, ModelFormatProtocol):
        """Type-checking helper ensuring show formats satisfy the protocol."""

        wikipedia_summary: str

        def render_wikipedia_summary(self, console: Console) -> None: ...

        summary_title_fallback: ClassVar[str]
        summary_panel_style: ClassVar[str]
        summary_attributes: ClassVar[Sequence[str]]
        facts_panel_title: ClassVar[str]
        facts_panel_style: ClassVar[str]

        def _summary_panel(self) -> tuple[str, Sequence[str], str]: ...

        def _fact_pairs(self) -> Sequence[tuple[str, str]]: ...

        def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence[JsonModel]]]: ...

        def _extra_panels(self) -> Sequence[tuple[str, str, str]]: ...

        def render(self, console: Console) -> None: ...


else:

    class ShowFormatBase(JsonModel):
        """Runtime base for show format models that provide rendering helpers."""

        summary_title_fallback: ClassVar[str] = "Television Series"
        summary_panel_style: ClassVar[str] = "green"
        summary_attributes: ClassVar[Sequence[str]] = ("tagline", "show_summary")
        facts_panel_title: ClassVar[str] = "Quick Facts"
        facts_panel_style: ClassVar[str] = "blue"

        wikipedia_summary: str = Field(
            "",
            exclude=True,
            description="Runtime-only hint populated after parsing for richer rendering.",
        )

        def render_wikipedia_summary(self, console: Console) -> None:
            hint_text = self.wikipedia_summary.strip()
            if not hint_text:
                return
            console.print(Panel(hint_text, title="Context", expand=False, style="yellow"))

        # Rendering hook methods ---------------------------------------------------------
        def _summary_panel(self) -> tuple[str, Sequence[str], str]:
            title_value = getattr(self, "title", "") or self.summary_title_fallback
            lines: list[str] = []
            for attribute in self.summary_attributes:
                value = getattr(self, attribute, None)
                if isinstance(value, str) and value.strip():
                    lines.append(value.strip())
            if not lines:
                fallback = getattr(self, "show_summary", None)
                if isinstance(fallback, str) and fallback.strip():
                    lines.append(fallback.strip())
            if not lines:
                lines.append("(no summary provided)")
            return title_value, lines, self.summary_panel_style

        def _fact_pairs(self) -> Sequence[tuple[str, str]]:
            return []

        def _table_sections(self) -> Sequence[tuple[str, List[TableSchema], Sequence[JsonModel]]]:
            return []

        def _extra_panels(self) -> Sequence[tuple[str, str, str]]:
            return []

        # MARK: Render -------------------------------------------------------------------
        def render(self, console: Console) -> None:
            summary_title, summary_lines, summary_style = self._summary_panel()
            summary_body = "\n\n".join(line for line in summary_lines if line.strip())
            if not summary_body.strip():
                summary_body = "(no summary provided)"
            console.print(Panel(summary_body, title=summary_title, expand=False, style=summary_style))

            self.render_wikipedia_summary(console)

            fact_pairs = list(self._fact_pairs())
            if fact_pairs:
                facts_text = ", ".join(f"{label}: {value}" for label, value in fact_pairs)
                console.print(Panel(facts_text, title=self.facts_panel_title, expand=False, style=self.facts_panel_style))

            for title, schema, rows in self._table_sections():
                if rows:
                    render_table_from_schema(title, schema, rows, console)

            for panel_title, body, style in self._extra_panels():
                if body:
                    console.print(Panel(body, title=panel_title, expand=False, style=style or "cyan"))


class CriticalResponse(JsonModel):
    """Structured representation of a critical review snippet."""

    outlet: str = Field("", description="Publication or platform name")
    reviewer: str = Field("", description="Reviewer or critic name")
    score: float | None = Field(None, description="Numeric score or rating if provided")
    summary: str = Field("", description="Condensed takeaway from the review")
    quote: str = Field("", description="Representative quote from the review")
    publication_date: str = Field("", description="Release date of the review in ISO format")

    @classmethod
    def table_schema(cls) -> list[TableSchema]:
        return [
            TableSchema(name="outlet", header="Outlet", style="magenta"),
            TableSchema(name="reviewer", header="Reviewer", style="cyan"),
            TableSchema(name="score", header="Score", justify="center", formatter=format_decimal),
            TableSchema(name="summary", header="Summary"),
        ]


class AudienceEngagement(JsonModel):
    """Metrics describing how viewers engage with a show."""

    region: str = Field("", description="Region or platform for the statistic")
    demographic: str = Field("", description="Key demographic segment")
    average_viewers: int | None = Field(None, description="Average viewers for the period")
    share: float | None = Field(None, description="Audience share percentage if available")
    engagement_notes: str = Field("", description="Contextual notes about the metric")

    @classmethod
    def table_schema(cls) -> list[TableSchema]:
        return [
            TableSchema(name="region", header="Region", style="magenta"),
            TableSchema(name="demographic", header="Demographic", style="cyan"),
            TableSchema(name="average_viewers", header="Avg Viewers", justify="right", formatter=format_number),
            TableSchema(name="share", header="Share %", justify="right", formatter=format_percentage),
            TableSchema(name="engagement_notes", header="Notes"),
        ]


# MARK: Character Info
class CharInfoInfo(JsonModel):
    character: str = Field("", description="Name of character from the show")
    actor: str = Field("", description="Actor / Voice actor of the character")
    relationship: str = Field("", description="Relationship to other characters")
    description: str = Field("", description="Short description of the character")
    year_joined: int = Field(0, description="Year the character joined the show")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        """
        Return a TableSchema list describing columns for character tables.

        :return: List of TableSchema describing the character table columns
        :rtype: List[TableSchema]
        """
        return [
            TableSchema(name="character", header="Name", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="relationship", header="Relationship", style="yellow"),
            TableSchema(name="year_joined", header="Year Joined", justify="center", formatter=format_year),
            TableSchema(name="description", header="Description"),
        ]

    # year formatting is handled by shared utils.format_year

    def __repr__(self) -> str:
        return f"CharInfoInfo(character={self.character!r}, actor={self.actor!r}, relationship={self.relationship!r}, year_joined={self.year_joined!r})"

    def __str__(self) -> str:
        return f"{self.character} ({self.actor})"


# MARK: Production Company
class ProductionCompanyInfo(JsonModel):
    name: str = Field("", description="Name of the production company")
    founded_year: int = Field(0, description="Year the production company was founded")
    start_year: int = Field(0, description="Year the company started working on the show")
    end_year: int = Field(0, description="Year the company stopped working on the show")
    country: str = Field("", description="Country where the production company is based")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        """
        Return a TableSchema list describing production company columns.

        :return: List of TableSchema for production companies
        :rtype: List[TableSchema]
        """
        return [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(name="founded_year", header="Founded Year", justify="center", formatter=format_year),
            TableSchema(name="start_year", header="Start Year", justify="center", formatter=format_year),
            TableSchema(name="end_year", header="End Year", justify="center", formatter=format_year),
            TableSchema(name="country", header="Country", style="cyan"),
        ]

    # Use shared format_year from utils

    def __repr__(self) -> str:
        return f"ProductionCompanyInfo(name={self.name!r}, founded_year={self.founded_year!r})"

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"


# MARK: Broadcast Info
class BroadcastInfo(JsonModel):
    network: str = Field("", description="Name of the broadcast network")
    country: str = Field("", description="Country where the show is broadcasted")
    start_year: int = Field(0, description="Year the show started broadcasting on this network")
    end_year: int = Field(0, description="Year the show ended broadcasting on this network")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        """
        Return TableSchema for broadcast info columns.

        :return: List[TableSchema] for broadcast columns
        :rtype: List[TableSchema]
        """
        return [
            TableSchema(name="network", header="Network", style="magenta"),
            TableSchema(name="country", header="Country", style="cyan"),
            TableSchema(name="start_year", header="Start Year", justify="center", formatter=format_year),
            TableSchema(name="end_year", header="End Year", justify="center", formatter=format_year),
        ]

    # year formatting is provided by aiss.utils.format_year

    def __repr__(self) -> str:
        return f"BroadcastInfo(network={self.network!r}, country={self.country!r})"

    def __str__(self) -> str:
        return f"{self.network} ({self.country})"


# MARK: Distribution Info
class DistributionInfo(JsonModel):
    """Information about worldwide distribution for a show.

    This model captures the distributor, territory, release window and an
    optional revenue figure when available.
    """

    distributor: str = Field("", description="Name of the distributor")
    territory: str = Field("", description="Territory / country of distribution")
    release_type: str = Field("", description="Type of release (theatrical, streaming, tv, etc.)")
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

    def __repr__(self) -> str:
        return f"DistributionInfo(distributor={self.distributor!r}, territory={self.territory!r})"

    def __str__(self) -> str:
        return f"{self.distributor} — {self.territory} ({self.release_type})"


# MARK: Box Office
class BoxOfficeInfo(JsonModel):
    budget: Optional[int] = Field(None, description="Budget in smallest currency unit or local currency")
    gross_worldwide: Optional[int] = Field(None, description="Worldwide gross")
    gross_domestic: Optional[int] = Field(None, description="Domestic gross")

    def __repr__(self) -> str:
        return f"BoxOfficeInfo(budget={self.budget!r}, gross_worldwide={self.gross_worldwide!r})"

    def __str__(self) -> str:
        return f"Budget: {format_money(self.budget)} | Worldwide: {format_money(self.gross_worldwide)}"

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="budget", header="Budget", style="magenta", justify="right", formatter=format_money),
            TableSchema(name="gross_worldwide", header="Gross (WW)", style="cyan", justify="right", formatter=format_money),
            TableSchema(name="gross_domestic", header="Gross (Domestic)", style="yellow", justify="right", formatter=format_money),
        ]
