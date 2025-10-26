"""Tests for DocumentaryBiographicalMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    BoxOfficeInfo,
    CastMemberInfo,
    ProductionCompanyInfo,
    SubjectFocusInfo,
)
from aiss.models.movies.documentary_biographical_model import DocumentaryBiographicalMovieInfo


@pytest.fixture
def documentary_movie_full():
    """Create a fully populated documentary movie instance for testing."""
    return DocumentaryBiographicalMovieInfo(
        title="The Climate Reckoning",
        tagline="Our planet. Our choice.",
        synopsis="An investigative look at climate change through the eyes of scientists and affected communities.",
        release_year=2024,
        runtime_minutes=95,
        genres=["Documentary"],
        mpaa_rating="PG",
        directors=["Documentary Filmmaker"],
        writers=["Documentary Writer"],
        producers=["Documentary Producer"],
        original_language="English",
        countries=["USA", "UK"],
        rating=8.5,
        keywords=["climate change", "environment", "science"],
        cast=[
            CastMemberInfo(character="Narrator", actor="Famous Narrator", role="Narrator"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Truth Films",
                founded_year=2010,
                start_year=2022,
                end_year=2024,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=5000000, gross_worldwide=15000000, gross_domestic=6000000),
        awards=["Best Documentary", "Audience Award"],
        soundtrack_highlights=["Original score by Documentary Composer"],
        subjects=[
            SubjectFocusInfo(
                subject="Dr. Jane Climate",
                role_or_significance="Lead Scientist - 30 years climate research",
                time_period="1990-2024",
                perspective="Expert scientific viewpoint",
            ),
            SubjectFocusInfo(
                subject="Pacific Island Communities",
                role_or_significance="Affected populations facing displacement",
                time_period="2000-2024",
                perspective="Human impact of climate change",
            ),
        ],
        narrative_scope="Global investigation with personal stories",
        primary_sources=["IPCC Reports", "NASA Climate Data", "Archived footage from 1980s"],
        interviewees=["Dr. Jane Climate", "Former EPA Director", "Island Community Leaders"],
        historical_accuracy_notes="All data peer-reviewed; some projections debated",
        distribution_platforms=["Netflix", "Theatrical Release", "PBS"],
        call_to_action="Contact representatives to support climate legislation",
    )


def test_documentary_basic_creation():
    """Test basic documentary movie creation."""
    movie = DocumentaryBiographicalMovieInfo(title="Test Documentary")
    assert movie.title == "Test Documentary"
    assert movie.model_name == "DocumentaryBiographicalMovieInfo"


def test_documentary_additional_fact_pairs(documentary_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(documentary_movie_full._additional_fact_pairs())
    assert "Global investigation" in facts["Scope"]
    assert "Contact representatives" in facts["Call to Action"]
    assert "peer-reviewed" in facts["Accuracy"]


def test_documentary_extra_tables(documentary_movie_full):
    """Test extra tables generation."""
    tables = documentary_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Subjects" in titles


def test_documentary_extra_panels(documentary_movie_full):
    """Test extra panels generation."""
    panels = documentary_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "Primary Sources" in panel_titles
    assert "Interviewees" in panel_titles
    assert "Distribution" in panel_titles


def test_documentary_render_includes_content(documentary_movie_full, console):
    """Test render includes all expected content."""
    documentary_movie_full.render(console)
    text = console.export_text()
    assert "The Climate Reckoning" in text
    assert "Our planet. Our choice." in text


def test_documentary_instruction_helpers():
    """Test instruction helper methods."""
    combined = DocumentaryBiographicalMovieInfo.get_instructions(["Focus on accuracy"])
    assert "Additional context" in combined
    assert "Focus on accuracy" in combined

    prompt = DocumentaryBiographicalMovieInfo.get_user_prompt("Test Documentary")
    assert "Test Documentary" in prompt

    formatted = DocumentaryBiographicalMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_documentary_subjects(documentary_movie_full):
    """Test subjects data."""
    assert len(documentary_movie_full.subjects) == 2
    assert documentary_movie_full.subjects[0].subject == "Dr. Jane Climate"
    assert "climate research" in documentary_movie_full.subjects[0].role_or_significance.lower()


def test_documentary_primary_sources(documentary_movie_full):
    """Test primary sources list."""
    assert len(documentary_movie_full.primary_sources) == 3
    assert "IPCC Reports" in documentary_movie_full.primary_sources


def test_documentary_interviewees(documentary_movie_full):
    """Test interviewees list."""
    assert len(documentary_movie_full.interviewees) == 3
    assert "Dr. Jane Climate" in documentary_movie_full.interviewees


def test_documentary_distribution_platforms(documentary_movie_full):
    """Test distribution platforms list."""
    assert len(documentary_movie_full.distribution_platforms) == 3
    assert "Netflix" in documentary_movie_full.distribution_platforms


def test_documentary_empty_optional_fields(console):
    """Test documentary with minimal data."""
    movie = DocumentaryBiographicalMovieInfo(
        title="Minimal Documentary",
        synopsis="Basic documentary",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    assert isinstance(facts, dict)


def test_documentary_roundtrip():
    """Test serialization roundtrip."""
    original = DocumentaryBiographicalMovieInfo(
        title="Roundtrip Documentary",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=90,
        narrative_scope="Test scope",
        call_to_action="Test action",
    )
    data = original.to_dict()
    restored = DocumentaryBiographicalMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.narrative_scope == original.narrative_scope
    assert restored.call_to_action == original.call_to_action


def test_subject_focus_info_table_schema():
    """Test SubjectFocusInfo has table schema."""
    schema = SubjectFocusInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Subject" in headers
