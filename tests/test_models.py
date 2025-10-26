"""Tests for model base functionality and serialization."""

import pytest

from aiss.models.movies import (
    BoxOfficeInfo,
    CastMemberInfo,
    DramaMovieInfo,
)
from aiss.models.movies import (
    ProductionCompanyInfo as MovieProductionCompanyInfo,
)
from aiss.models.shared import TableSchema
from aiss.models.shows._base import BroadcastInfo, CharInfoInfo, ProductionCompanyInfo


@pytest.mark.parametrize("cls", [CharInfoInfo, ProductionCompanyInfo, BroadcastInfo])
def test_table_schema_types_show(cls):
    """
    Test that show model table_schema methods return valid TableSchema lists.

    :param cls: The show model class to test
    :type cls: type
    """
    schema = cls.table_schema()
    assert isinstance(schema, list)
    assert all(isinstance(s, TableSchema) for s in schema), f"{cls.__name__} schema items must be TableSchema"


@pytest.mark.parametrize("cls", [CastMemberInfo, MovieProductionCompanyInfo])
def test_table_schema_types_movie(cls):
    """
    Test that movie model table_schema methods return valid TableSchema lists.

    :param cls: The movie model class to test
    :type cls: type
    """
    schema = cls.table_schema()
    assert isinstance(schema, list)
    assert all(isinstance(s, TableSchema) for s in schema), f"{cls.__name__} schema items must be TableSchema"


def test_castmember_roundtrip():
    """
    Test CastMemberInfo serialization and deserialization roundtrip.

    Ensures that converting to dict and back preserves all data.
    """
    c = CastMemberInfo(character="Neo", actor="Keanu Reeves", role="lead")
    d = c.to_dict()
    c2 = CastMemberInfo.from_dict(d)
    assert c.character == c2.character
    assert c.actor == c2.actor
    assert c.role == c2.role


def test_drama_movie_from_dict(sample_movie):
    """
    Test DramaMovieInfo deserialization from dictionary.

    Verifies that complex nested structures like cast and production companies
    are correctly restored with proper types.

    :param sample_movie: Fixture providing a sample DramaMovieInfo instance
    :type sample_movie: DramaMovieInfo
    """
    m = sample_movie
    d = m.to_dict()
    m2 = DramaMovieInfo.from_dict(d)
    assert m.title == m2.title
    assert isinstance(m2.cast[0], CastMemberInfo)
    assert isinstance(m2.production_companies[0], MovieProductionCompanyInfo)
    assert isinstance(m2.box_office, BoxOfficeInfo)
