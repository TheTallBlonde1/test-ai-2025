"""Shared pytest fixtures for all test modules."""

from unittest.mock import Mock

import pytest
from rich.console import Console

from aiss.models.movies import (
    BoxOfficeInfo,
    CastMemberInfo,
    DramaMovieInfo,
)
from aiss.models.movies import (
    ProductionCompanyInfo as MovieProductionCompanyInfo,
)
from aiss.models.shows._base import BroadcastInfo, ProductionCompanyInfo
from aiss.models.shows.drama_model import DramaCharacterProfile, DramaShowInfo


@pytest.fixture
def console() -> Console:
    """
    Rich Console configured for tests with recording enabled.

    :return: A Console instance with record=True for capturing output
    :rtype: Console
    """
    return Console(record=True)


@pytest.fixture
def fake_client_factory():
    """
    Return a factory that produces a fake OpenAI-like client.

    The client's responses.parse returns an object with .output_parsed
    set to the provided parsed value.

    Usage:
        client = fake_client_factory(parsed_obj)

    :return: Factory function that creates mock clients
    :rtype: Callable
    """

    def _make(parsed):
        m = Mock()
        m.responses = Mock()
        m.responses.parse.return_value = Mock(output_parsed=parsed)
        return m

    return _make


@pytest.fixture
def sample_show() -> DramaShowInfo:
    """
    Create a sample DramaShowInfo instance for testing.

    :return: A populated DramaShowInfo instance with character, production, and broadcast data
    :rtype: DramaShowInfo
    """
    fake_char = DramaCharacterProfile(
        name="Test Character",
        actor="Actor Name",
        arc_summary="Arc summary",
        driving_conflict="Conflict",
        key_relationships=["Friend"],
        season_introduced=1,
        current_status="Active",
    )
    prod = ProductionCompanyInfo(name="Studio", founded_year=1990, start_year=2000, end_year=2005, country="USA")
    brod = BroadcastInfo(network="Net", country="US", start_year=2000, end_year=2004)
    s = DramaShowInfo(
        title="Sample Show",
        logline="Sample logline",
        characters=[fake_char],
        show_summary="Summary here",
        production_companies=[prod],
        broadcast_info=[brod],
    )
    return s


@pytest.fixture
def sample_movie() -> DramaMovieInfo:
    """
    Create a sample DramaMovieInfo instance for testing.

    :return: A populated DramaMovieInfo instance with cast, production, and box office data
    :rtype: DramaMovieInfo
    """
    cast = CastMemberInfo(character="Lead", actor="Actor", role="lead")
    prod = MovieProductionCompanyInfo(
        name="BigStudio",
        founded_year=1980,
        start_year=2019,
        end_year=2020,
        country="USA",
    )
    bo = BoxOfficeInfo(budget=1000000, gross_worldwide=5000000, gross_domestic=2000000)
    m = DramaMovieInfo(
        title="Example",
        synopsis="An example movie",
        release_year=2020,
        runtime_minutes=120,
        genres=["Drama"],
        directors=["Someone"],
        cast=[cast],
        production_companies=[prod],
        box_office=bo,
        central_conflict="Lead must choose between ambition and loyalty.",
        themes=["Ambition", "Friendship"],
        pivotal_moments=["Lead confronts mentor"],
    )
    return m
