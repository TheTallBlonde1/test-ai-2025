import json
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

from aiss.utils import render_table_from_schema

from .shared import TableSchema

instructions = """Provide a detailed summary of the show along with a list of main characters including their actor, relationship to other characters, description, and year joined. 
    Include information about what network the show was broadcasted on, including the network name, country, start year, and end year.
    Also include information about the production companies involved in the show, including their name, founded year, year started working on the show, year ended working on the show, and country."""


class CharInfoInfo(BaseModel):
    character: str = Field("", description="Name of character from the show")
    actor: str = Field("", description="Actor / Voice actor of the character")
    relationship: str = Field("", description="Relationship to other characters")
    description: str = Field("", description="Short description of the character")
    year_joined: int = Field(0, description="Year the character joined the show")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="character", header="Name", style="magenta", no_wrap=True),
            TableSchema(name="actor", header="Actor", style="cyan"),
            TableSchema(name="relationship", header="Relationship", style="yellow"),
            TableSchema(name="year_joined", header="Year Joined", justify="center", formatter=cls._format_year),
            TableSchema(name="description", header="Description"),
        ]

    @staticmethod
    def _format_year(v) -> str:
        try:
            return str(int(v)) if v else "-"
        except Exception:
            return str(v)

    def __repr__(self) -> str:
        return f"CharInfoInfo(character={self.character!r}, actor={self.actor!r}, relationship={self.relationship!r}, year_joined={self.year_joined!r})"

    def __str__(self) -> str:
        return f"{self.character} ({self.actor})"

    def to_dict(self) -> dict:
        return {
            "character": self.character,
            "actor": self.actor,
            "relationship": self.relationship,
            "description": self.description,
            "year_joined": self.year_joined,
        }

    def to_json(self, json_file_path):
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "CharInfoInfo":
        return cls(
            character=data.get("character", ""),
            actor=data.get("actor", ""),
            relationship=data.get("relationship", ""),
            description=data.get("description", ""),
            year_joined=data.get("year_joined", 0),
        )

    @classmethod
    def from_json(cls, json_file_path):
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


class ProductionCompanyInfo(BaseModel):
    name: str = Field("", description="Name of the production company")
    founded_year: int = Field(0, description="Year the production company was founded")
    start_year: int = Field(0, description="Year the company started working on the show")
    end_year: int = Field(0, description="Year the company stopped working on the show")
    country: str = Field("", description="Country where the production company is based")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="name", header="Name", style="magenta"),
            TableSchema(name="founded_year", header="Founded Year", justify="center", formatter=cls._format_year),
            TableSchema(name="start_year", header="Start Year", justify="center", formatter=cls._format_year),
            TableSchema(name="end_year", header="End Year", justify="center", formatter=cls._format_year),
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


class BroadcastInfo(BaseModel):
    network: str = Field("", description="Name of the broadcast network")
    country: str = Field("", description="Country where the show is broadcasted")
    start_year: int = Field(0, description="Year the show started broadcasting on this network")
    end_year: int = Field(0, description="Year the show ended broadcasting on this network")

    @classmethod
    def table_schema(cls) -> List[TableSchema]:
        return [
            TableSchema(name="network", header="Network", style="magenta"),
            TableSchema(name="country", header="Country", style="cyan"),
            TableSchema(name="start_year", header="Start Year", justify="center", formatter=cls._format_year),
            TableSchema(name="end_year", header="End Year", justify="center", formatter=cls._format_year),
        ]

    @staticmethod
    def _format_year(v) -> str:
        try:
            return str(int(v)) if v else "-"
        except Exception:
            return str(v)

    def __repr__(self) -> str:
        return f"BroadcastInfo(network={self.network!r}, country={self.country!r})"

    def __str__(self) -> str:
        return f"{self.network} ({self.country})"

    def to_dict(self) -> dict:
        return {
            "network": self.network,
            "country": self.country,
            "start_year": self.start_year,
            "end_year": self.end_year,
        }

    def to_json(self, json_file_path):
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "BroadcastInfo":
        return cls(
            network=data.get("network", ""),
            country=data.get("country", ""),
            start_year=data.get("start_year", 0),
            end_year=data.get("end_year", 0),
        )

    @classmethod
    def from_json(cls, json_file_path):
        path = Path(json_file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


class ShowInfo(BaseModel):
    characters: list[CharInfoInfo] = Field([], description="List of characters and their info from the show")
    show_summary: str = Field("", description="Overall summary of the show")
    production_companies: list[ProductionCompanyInfo] = Field([], description="List of production companies involved in the show")
    broadcast_info: list[BroadcastInfo] = Field([], description="Broadcast information of the show")

    def render(self, console: Console) -> None:
        """Render this ShowInfo to the provided Rich Console using the
        centralized render_table_from_schema helper and Panel for summary."""
        # Summary
        summary_text = self.show_summary or "(no summary returned)"
        console.print(Panel(summary_text, title="Summary", expand=False, style="green"))

        # Characters
        if self.characters:
            render_table_from_schema("Characters", CharInfoInfo.table_schema(), self.characters, console)
        else:
            console.print("[yellow]No character info returned.[/yellow]")

        # Broadcast
        if self.broadcast_info:
            render_table_from_schema("Broadcast Info", BroadcastInfo.table_schema(), self.broadcast_info, console)

        # Production companies
        if self.production_companies:
            render_table_from_schema("Production Companies", ProductionCompanyInfo.table_schema(), self.production_companies, console)

    def __repr__(self) -> str:
        return f"ShowInfo(characters={len(self.characters)}, production_companies={len(self.production_companies)})"

    def __str__(self) -> str:
        return f"Show with {len(self.characters)} characters"

    def to_dict(self) -> dict:
        return {
            "show_summary": self.show_summary,
            "characters": [c.to_dict() if hasattr(c, "to_dict") else c for c in self.characters],
            "production_companies": [p.to_dict() if hasattr(p, "to_dict") else p for p in self.production_companies],
            "broadcast_info": [b.to_dict() if hasattr(b, "to_dict") else b for b in self.broadcast_info],
        }

    def to_json(self, json_file_path):
        path = Path(json_file_path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "ShowInfo":
        chars = [CharInfoInfo.from_dict(c) if isinstance(c, dict) else c for c in (data.get("characters") or [])]
        prods = [ProductionCompanyInfo.from_dict(p) if isinstance(p, dict) else p for p in (data.get("production_companies") or [])]
        brod = [BroadcastInfo.from_dict(b) if isinstance(b, dict) else b for b in (data.get("broadcast_info") or [])]
        return cls(characters=chars, show_summary=data.get("show_summary", ""), production_companies=prods, broadcast_info=brod)

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
    def get_user_prompt(show_name: str) -> str:
        return f"Tell me about the show '{show_name}', including its characters, production companies, and broadcast information."

    @staticmethod
    def json_format_instructions() -> str:
        # Avoid f-string here because the JSON example contains braces which
        # would be interpreted as format specifiers. Concatenate the general
        # instructions with the JSON schema literal.
        return (
            ShowInfo.get_instructions()
            + "\nOUTPUT FORMAT:\nFormat the response as a JSON object with the following structure:\n"
            + '```json\n{\n    "show_summary": "string",\n    "characters": [\n        {\n            "character": "string",\n            "actor": "string",\n            "relationship": "string",\n            "description": "string",\n            "year_joined": "integer"\n        }\n    ],\n    "broadcast_info": [\n        {\n            "network": "string",\n            "country": "string",\n            "start_year": "integer",\n            "end_year": "integer"\n        }\n    ],\n    "production_companies": [\n        {\n            "name": "string",\n            "founded_year": "integer",\n            "start_year": "integer",\n            "end_year": "integer",\n            "country": "string"\n        }\n    ]\n}\n```'
        )
