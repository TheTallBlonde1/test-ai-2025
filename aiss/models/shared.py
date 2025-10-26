"""Shared model helpers and typed schema descriptors.

This module contains small, reusable utilities used by the rendering
helpers. The primary exported item is `TableSchema`, a typed descriptor
for a column in a Rich table.

"""

from dataclasses import dataclass
from enum import StrEnum
from functools import lru_cache
from typing import Any, Callable, Optional, Sequence, cast

# Avoid top-level imports of models to prevent circular imports; import lazily
from .protocols import ModelFormatProtocol


def compose_instructions(base: str, additional_info: Optional[Sequence[str]] = None) -> str:
    """Combine base instructions with optional additional context lines."""

    if not additional_info:
        return base

    extras = [line.strip() for line in additional_info if isinstance(line, str) and line.strip()]
    if not extras:
        return base

    joined_extras = "\n".join(f"- {line}" for line in extras)
    base_text = base.rstrip()
    return f"{base_text}\n\nAdditional context:\n{joined_extras}"


class ResultType(StrEnum):
    PARSED = "parsed"
    JSON = "json"
    TEXT = "text"


class ModelType(StrEnum):
    SHOW = "show"
    MOVIE = "movie"
    DRAMA = "drama"
    COMEDY = "comedy"
    THRILLER = "thriller"
    ACTION_ADVENTURE_FANTASY = "action_adventure_fantasy"
    SCIENCE_FICTION = "science_fiction"
    REALITY_COMPETITION_LIFESTYLE = "reality_competition_lifestyle"
    DOCUMENTARY_FACTUAL = "documentary_factual"
    FAMILY_ANIMATION_KIDS = "family_animation_kids"
    NEWS_INFORMATIONAL = "news_informational"
    SPORTS = "sports"
    DRAMA_MOVIE = "drama_movie"
    COMEDY_MOVIE = "comedy_movie"
    ACTION_ADVENTURE_MOVIE = "action_adventure_movie"
    FANTASY_SCIENCE_FICTION_MOVIE = "fantasy_science_fiction_movie"
    THRILLER_MYSTERY_CRIME_MOVIE = "thriller_mystery_crime_movie"
    ROMANCE_MOVIE = "romance_movie"
    HORROR_MOVIE = "horror_movie"
    DOCUMENTARY_BIOGRAPHICAL_MOVIE = "documentary_biographical_movie"
    ACTION_ADVENTURE_GAME = "action_adventure_game"
    SHOOTER_GAME = "shooter_game"
    PUZZLE_STRATEGY_GAME = "puzzle_strategy_game"
    ROLE_PLAYING_GAME = "role_playing_game"
    SIMULATION_SANDBOX_GAME = "simulation_sandbox_game"
    SPORTS_RACING_GAME = "sports_racing_game"
    HORROR_SURVIVAL_GAME = "horror_survival_game"
    MMO_ONLINE_GAME = "mmo_online_game"

    def __str__(self) -> str:
        return self.value

    def get_model_from_name(self) -> type[ModelFormatProtocol]:
        """Return the Pydantic model class associated with this ModelType."""

        from .games import (
            ActionAdventureGameInfo,
            HorrorSurvivalGameInfo,
            MmoOnlineGameInfo,
            PuzzleStrategyGameInfo,
            RolePlayingGameInfo,
            ShooterGameInfo,
            SimulationSandboxGameInfo,
            SportsRacingGameInfo,
        )
        from .movies import (
            DEFAULT_MOVIE_MODEL,
            ActionAdventureMovieInfo,
            ComedyMovieInfo,
            DocumentaryBiographicalMovieInfo,
            DramaMovieInfo,
            FantasyScienceFictionMovieInfo,
            HorrorMovieInfo,
            RomanceMovieInfo,
            ThrillerMysteryCrimeMovieInfo,
        )
        from .shows import (
            DEFAULT_SHOW_MODEL,
            ActionAdventureFantasyShowInfo,
            ComedyShowInfo,
            DocumentaryFactualShowInfo,
            DramaShowInfo,
            FamilyAnimationKidsShowInfo,
            NewsInformationalShowInfo,
            RealityCompetitionLifestyleShowInfo,
            ScienceFictionShowInfo,
            SportsShowInfo,
            ThrillerShowInfo,
        )

        mapping = {
            ModelType.SHOW: DEFAULT_SHOW_MODEL,
            ModelType.MOVIE: DEFAULT_MOVIE_MODEL,
            ModelType.DRAMA: DramaShowInfo,
            ModelType.COMEDY: ComedyShowInfo,
            ModelType.THRILLER: ThrillerShowInfo,
            ModelType.ACTION_ADVENTURE_FANTASY: ActionAdventureFantasyShowInfo,
            ModelType.SCIENCE_FICTION: ScienceFictionShowInfo,
            ModelType.REALITY_COMPETITION_LIFESTYLE: RealityCompetitionLifestyleShowInfo,
            ModelType.DOCUMENTARY_FACTUAL: DocumentaryFactualShowInfo,
            ModelType.FAMILY_ANIMATION_KIDS: FamilyAnimationKidsShowInfo,
            ModelType.NEWS_INFORMATIONAL: NewsInformationalShowInfo,
            ModelType.SPORTS: SportsShowInfo,
            ModelType.DRAMA_MOVIE: DramaMovieInfo,
            ModelType.COMEDY_MOVIE: ComedyMovieInfo,
            ModelType.ACTION_ADVENTURE_MOVIE: ActionAdventureMovieInfo,
            ModelType.FANTASY_SCIENCE_FICTION_MOVIE: FantasyScienceFictionMovieInfo,
            ModelType.THRILLER_MYSTERY_CRIME_MOVIE: ThrillerMysteryCrimeMovieInfo,
            ModelType.ROMANCE_MOVIE: RomanceMovieInfo,
            ModelType.HORROR_MOVIE: HorrorMovieInfo,
            ModelType.DOCUMENTARY_BIOGRAPHICAL_MOVIE: DocumentaryBiographicalMovieInfo,
            ModelType.ACTION_ADVENTURE_GAME: ActionAdventureGameInfo,
            ModelType.SHOOTER_GAME: ShooterGameInfo,
            ModelType.PUZZLE_STRATEGY_GAME: PuzzleStrategyGameInfo,
            ModelType.ROLE_PLAYING_GAME: RolePlayingGameInfo,
            ModelType.SIMULATION_SANDBOX_GAME: SimulationSandboxGameInfo,
            ModelType.SPORTS_RACING_GAME: SportsRacingGameInfo,
            ModelType.HORROR_SURVIVAL_GAME: HorrorSurvivalGameInfo,
            ModelType.MMO_ONLINE_GAME: MmoOnlineGameInfo,
        }

        try:
            return mapping[self]
        except KeyError as exc:
            raise ValueError(f"Unknown ModelType: {self}") from exc

    @classmethod
    @lru_cache(maxsize=1)
    def registry(cls) -> dict[str, type[ModelFormatProtocol]]:
        """Return a cached mapping of model type strings to format classes."""

        mapping: dict[str, type[ModelFormatProtocol]] = {}
        for member in cls:
            try:
                mapping[member.value] = member.get_model_from_name()
            except ValueError:
                continue
        return mapping

    @classmethod
    def formatted_options(cls) -> str:
        """Return a human-readable list of registered model type strings."""

        names = [f"'{name}'" for name in cls.registry().keys()]
        if not names:
            return "''"
        if len(names) == 1:
            return names[0]
        return ", ".join(names[:-1]) + ", or " + names[-1]

    @classmethod
    def instruction_listing(cls) -> str:
        """Return a descriptive multi-line string for instructions/prompts."""

        lines = ["", "Models available:"]
        for model_name, model in cls.registry().items():
            lines.append(f"For model type '{model_name}':")
            lines.append(f"- Description: {model.description}")
            lines.append(f"- Key Trait: {model.key_trait}")

        return "\n".join(lines)

    @property
    def display_label(self) -> str:
        """Human-friendly label for progress output and logging."""

        return self.value.replace("_", " ").title()

    @property
    def get_found_model_name(self) -> str:
        model = self.get_model_from_name()
        if hasattr(model, "model_name"):
            return model.model_name
        raise ValueError(f"Unknown ModelType: {self}")

    @property
    def get_found_model_description(self) -> str:
        model = self.get_model_from_name()
        if hasattr(model, "description"):
            return model.description
        raise ValueError(f"Unknown ModelType: {self}")


@dataclass
class ModelTypeResult:
    model_type: ModelType
    description: str
    formatted_name: str
    additional_info: Optional[list[str]] = None

    def __str__(self) -> str:
        """
        String representation of the model type result.
        console.print(f"[bold green]Running `{formatted_name}` using `{model_name}`: `{model_description}` ({result_type.value.capitalize()})[/bold green]")

        :return: String describing the model type and formatted name
        :rtype: str
        """
        return f"`{self.formatted_name}` using `{self.model_type.get_found_model_name}`: `{self.model_type.get_found_model_description}` ({self.model_type.display_label})"

    def __repr__(self) -> str:
        return f"ModelTypeResult(model_type={self.model_type}, formatted_name='{self.formatted_name}', additional_info={self.additional_info})"


# MARK: Table Schema
@dataclass
class TableSchema:
    """Schema descriptor for a table column.

    This small dataclass centralizes how table columns are described. It is
    intended to replace older dict-shaped schemas and provides clearer
    typing for renderers.

    :param name: Attribute name on the item to read
    :type name: str
    :param header: Column header text shown in the table
    :type header: str
    :param style: Optional Rich style string for the column
    :type style: Optional[str]
    :param no_wrap: If True, the column will not wrap
    :type no_wrap: bool
    :param justify: Optional justification (e.g., 'center')
    :type justify: Optional[str]
    :param formatter: Optional callable used to format individual cell values
    :type formatter: Optional[Callable[[Any], str]]

    :return: dataclass instance representing a column schema
    :rtype: TableSchema
    """

    name: str
    header: str
    style: Optional[str] = None
    no_wrap: bool = False
    justify: Optional[str] = None
    formatter: Optional[Callable[[Any], str]] = None


# Default show model fallback used when no specific show type is provided
DEFAULT_SHOW_MODEL = cast(type[ModelFormatProtocol], ModelType.SHOW.get_model_from_name())
