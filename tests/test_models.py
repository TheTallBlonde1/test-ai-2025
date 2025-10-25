import pytest

from aiss.models.movie_model import BoxOfficeInfo, CastMemberInfo, MovieInfo
from aiss.models.movie_model import ProductionCompanyInfo as MovieProd
from aiss.models.shared import TableSchema
from aiss.models.show_model import BroadcastInfo, CharInfoInfo, ProductionCompanyInfo


@pytest.mark.parametrize("cls", [CharInfoInfo, ProductionCompanyInfo, BroadcastInfo])
def test_table_schema_types_show(cls):
    schema = cls.table_schema()
    assert isinstance(schema, list)
    assert all(isinstance(s, TableSchema) for s in schema), f"{cls.__name__} schema items must be TableSchema"


@pytest.mark.parametrize("cls", [CastMemberInfo, MovieProd])
def test_table_schema_types_movie(cls):
    schema = cls.table_schema()
    assert isinstance(schema, list)
    assert all(isinstance(s, TableSchema) for s in schema), f"{cls.__name__} schema items must be TableSchema"


def test_castmember_roundtrip():
    c = CastMemberInfo(character="Neo", actor="Keanu Reeves", role="lead")
    d = c.to_dict()
    c2 = CastMemberInfo.from_dict(d)
    assert c.character == c2.character
    assert c.actor == c2.actor
    assert c.role == c2.role


def test_movieinfo_from_dict(sample_movie):
    m = sample_movie
    d = m.to_dict()
    m2 = MovieInfo.from_dict(d)
    assert m.title == m2.title
    assert isinstance(m2.cast[0], CastMemberInfo)
    assert isinstance(m2.production_companies[0], MovieProd)
    assert isinstance(m2.box_office, BoxOfficeInfo)
