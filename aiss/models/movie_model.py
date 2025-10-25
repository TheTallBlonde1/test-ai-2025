import json
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

from aiss.utils import render_table_from_schema

from .shared import TableSchema

instructions = """Provide a detailed summary of the movie along with the main cast,
their actors, key crew (director(s), producers), production companies, release year,
runtime, genres, and box-office/budget information."""


class CastMemberInfo(BaseModel):
    character: str = Field("", description="Name of character in the movie")
    actor: str = Field("", description="Actor who played the character")
    role: str = Field("", description="Role type (lead/supporting/guest)")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="character", header="Character", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="role", header="Role", style="yellow"),
        ]

    def __repr__(self) -> str:
        return f"CastMemberInfo(character={self.character}, actor={self.actor}, role={self.role})"

    def __str__(self) -> str:
        return f"{self.character} played by {self.actor} ({self.role})"

    def to_dict(self) -> dict[str, str]:
        return {
            "character": self.character,
            "actor": self.actor,
            "role": self.role,
        }

    def to_json(self, json_file_path: Path | str) -> None:
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    @classmethod
    def from_dict(cls, data: dict) -> "CastMemberInfo":
        return cls(
            character=data.get("character", ""),
            actor=data.get("actor", ""),
            role=data.get("role", ""),
        )

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "CastMemberInfo":
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


class ProductionCompanyInfo(BaseModel):
    name: str = Field("", description="Name of the production company")
    founded_year: int = Field(0, description="Year the production company was founded")
    start_year: int = Field(0, description="Year the company started working on the movie")
    end_year: int = Field(0, description="Year the company stopped working on the movie")
    country: str = Field("", description="Country where the production company is based")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(name="founded_year", header="Founded", justify="center", formatter=cls._format_year),
            TableSchema(name="start_year", header="Start", justify="center", formatter=cls._format_year),
            TableSchema(name="end_year", header="End", justify="center", formatter=cls._format_year),
            TableSchema(name="country", header="Country", style="cyan"),
        ]

    @staticmethod
    def _format_year(v) -> str:
        try:
            return str(int(v)) if v else "-"
        except Exception:
            return str(v)

    def __repr__(self) -> str:
        return f"ProductionCompanyInfo(name={self.name!r}, founded_year={self.founded_year!r})"

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "founded_year": self.founded_year,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "country": self.country,
        }

    def to_json(self, json_file_path):
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductionCompanyInfo":
        return cls(
            name=data.get("name", ""),
            founded_year=data.get("founded_year", 0),
            start_year=data.get("start_year", 0),
            end_year=data.get("end_year", 0),
            country=data.get("country", ""),
        )

    @classmethod
    def from_json(cls, json_file_path):
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


class BoxOfficeInfo(BaseModel):
    budget: Optional[int] = Field(None, description="Budget in local currency or smallest unit")
    gross_worldwide: Optional[int] = Field(None, description="Worldwide gross")
    gross_domestic: Optional[int] = Field(None, description="Domestic gross")

    def __repr__(self) -> str:
        return f"BoxOfficeInfo(budget={self.budget!r}, gross_worldwide={self.gross_worldwide!r})"

    def __str__(self) -> str:
        parts = []
        if self.budget is not None:
            parts.append(f"Budget: {self.budget}")
        if self.gross_worldwide is not None:
            parts.append(f"Worldwide: {self.gross_worldwide}")
        return ", ".join(parts) or "(no box office data)"

    def to_dict(self) -> dict:
        return {
            "budget": self.budget,
            "gross_worldwide": self.gross_worldwide,
            "gross_domestic": self.gross_domestic,
        }

    def to_json(self, json_file_path):
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "BoxOfficeInfo":
        return cls(
            budget=data.get("budget"),
            gross_worldwide=data.get("gross_worldwide"),
            gross_domestic=data.get("gross_domestic"),
        )

    @classmethod
    def from_json(cls, json_file_path):
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


class MovieInfo(BaseModel):
    title: str = Field("", description="Movie title")
    synopsis: str = Field("", description="Short synopsis of the movie")
    release_year: int = Field(0, description="Year the movie was released")
    runtime_minutes: int = Field(0, description="Runtime in minutes")
    genres: list[str] = Field([], description="List of genres")
    directors: list[str] = Field([], description="List of directors")
    cast: list[CastMemberInfo] = Field([], description="Main cast members")
    production_companies: list[ProductionCompanyInfo] = Field([], description="Production companies involved")
    box_office: Optional[BoxOfficeInfo] = Field(None, description="Box office / budget info")

    def render(self, console: Console) -> None:
        """Render this MovieInfo to the provided Rich Console using the
        centralized render_table_from_schema helper and Panel for the synopsis
        and summary facts."""
        # Title + synopsis
        title_text = f"{self.title} ({self.release_year})" if self.title else "(untitled)"
        synopsis_text = self.synopsis or "(no synopsis returned)"
        console.print(Panel(synopsis_text, title=title_text, expand=False, style="green"))

        # Basic facts
        facts = []
        facts.append({"header": "Runtime", "value": f"{self.runtime_minutes} min" if self.runtime_minutes else "-"})
        facts.append({"header": "Genres", "value": ", ".join(self.genres) if self.genres else "-"})
        facts.append({"header": "Directors", "value": ", ".join(self.directors) if self.directors else "-"})

        # Render facts as a small table
        # Use a simple panel for compact facts
        facts_text = ", ".join(f"{f['header']}: {f['value']}" for f in facts)
        console.print(Panel(facts_text, title="Facts", expand=False, style="blue"))

        # Cast
        if self.cast:
            render_table_from_schema("Cast", CastMemberInfo.table_schema(), self.cast, console)
        else:
            console.print("[yellow]No cast info returned.[/yellow]")

        # Production companies
        if self.production_companies:
            render_table_from_schema("Production Companies", ProductionCompanyInfo.table_schema(), self.production_companies, console)

        # Box office
        if self.box_office:
            bo = self.box_office
            bo_lines = []
            if bo.budget is not None:
                bo_lines.append(f"Budget: {bo.budget}")
            if bo.gross_domestic is not None:
                bo_lines.append(f"Gross (domestic): {bo.gross_domestic}")
            if bo.gross_worldwide is not None:
                bo_lines.append(f"Gross (worldwide): {bo.gross_worldwide}")

            if bo_lines:
                console.print(Panel("\n".join(bo_lines), title="Box Office", expand=False, style="magenta"))

    def __repr__(self) -> str:
        return f"MovieInfo(title={self.title!r}, release_year={self.release_year!r})"

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "synopsis": self.synopsis,
            "release_year": self.release_year,
            "runtime_minutes": self.runtime_minutes,
            "genres": list(self.genres),
            "directors": list(self.directors),
            "cast": [c.to_dict() if hasattr(c, "to_dict") else c for c in self.cast],
            "production_companies": [p.to_dict() if hasattr(p, "to_dict") else p for p in self.production_companies],
            "box_office": self.box_office.to_dict() if (self.box_office and hasattr(self.box_office, "to_dict")) else (self.box_office or None),
        }

    def to_json(self, json_file_path):
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "MovieInfo":
        cast = [CastMemberInfo.from_dict(c) if isinstance(c, dict) else c for c in (data.get("cast") or [])]
        prods = [ProductionCompanyInfo.from_dict(p) if isinstance(p, dict) else p for p in (data.get("production_companies") or [])]
        bo = data.get("box_office")
        bo_obj = BoxOfficeInfo.from_dict(bo) if isinstance(bo, dict) else None
        return cls(
            title=data.get("title", ""),
            synopsis=data.get("synopsis", ""),
            release_year=data.get("release_year", 0),
            runtime_minutes=data.get("runtime_minutes", 0),
            genres=data.get("genres", []),
            directors=data.get("directors", []),
            cast=cast,
            production_companies=prods,
            box_office=bo_obj,
        )

    @classmethod
    def from_json(cls, json_file_path):
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @staticmethod
    def get_instructions() -> str:
        return instructions

    @staticmethod
    def get_user_prompt(movie_title: str) -> str:
        return f"Tell me about the movie '{movie_title}', including cast, crew, production companies, release year, runtime, genres and box office information."

    @staticmethod
    def json_format_instructions() -> str:
        # Avoid f-strings with braces; return the general instructions plus a JSON schema example
        return (
            MovieInfo.get_instructions()
            + "\nOUTPUT FORMAT:\nFormat the response as a JSON object with the following structure:\n"
            + '```json\n{\n  "title": "string",\n  "synopsis": "string",\n  "release_year": "integer",\n  "runtime_minutes": "integer",\n  "genres": ["string"],\n  "directors": ["string"],\n  "cast": [\n    {\n      "character": "string",\n      "actor": "string",\n      "role": "string"\n    }\n  ],\n  "production_companies": [\n    {\n      "name": "string",\n      "founded_year": "integer",\n      "start_year": "integer",\n      "end_year": "integer",\n      "country": "string"\n    }\n  ],\n  "box_office": {\n    "budget": "integer?",\n    "gross_worldwide": "integer?",\n    "gross_domestic": "integer?"\n  }\n}\n```'
        )
