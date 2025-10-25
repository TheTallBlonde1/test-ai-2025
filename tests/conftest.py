from unittest.mock import Mock

import pytest
from rich.console import Console

from aiss.models.movie_model import BoxOfficeInfo, CastMemberInfo, MovieInfo
from aiss.models.movie_model import ProductionCompanyInfo as MovieProd
from aiss.models.show_model import BroadcastInfo, CharInfoInfo, ProductionCompanyInfo, ShowInfo


@pytest.fixture
def console() -> Console:
    """Rich Console configured for tests (record=True)."""
    return Console(record=True)


@pytest.fixture
def fake_client_factory():
    """Return a factory that produces a fake OpenAI-like client whose
    responses.parse returns an object with .output_parsed set to the
    provided parsed value.
    Usage: client = fake_client_factory(parsed_obj)
    """

    def _make(parsed):
        m = Mock()
        m.responses = Mock()
        m.responses.parse.return_value = Mock(output_parsed=parsed)
        return m

    return _make


@pytest.fixture
def sample_show() -> ShowInfo:
    fake_char = CharInfoInfo(
        character="Test Character",
        actor="Actor Name",
        relationship="Friend",
        description="A brave test character",
        year_joined=2001,
    )
    prod = ProductionCompanyInfo(name="Studio", founded_year=1990, start_year=2000, end_year=2005, country="USA")
    brod = BroadcastInfo(network="Net", country="US", start_year=2000, end_year=2004)
    s = ShowInfo(characters=[fake_char], show_summary="Summary here", production_companies=[prod], broadcast_info=[brod])
    return s


@pytest.fixture
def sample_movie() -> MovieInfo:
    cast = CastMemberInfo(character="Lead", actor="Actor", role="lead")
    prod = MovieProd(name="BigStudio", founded_year=1980, start_year=2019, end_year=2020, country="USA")
    bo = BoxOfficeInfo(budget=1000000, gross_worldwide=5000000, gross_domestic=2000000)
    m = MovieInfo(
        title="Example",
        synopsis="An example movie",
        release_year=2020,
        runtime_minutes=120,
        genres=["Drama"],
        directors=["Someone"],
        cast=[cast],
        production_companies=[prod],
        box_office=bo,
    )
    return m
