"""Tests for ThrillerMysteryCrimeMovieInfo model."""

import pytest

from aiss.models.movies._base import (
    BoxOfficeInfo,
    CastMemberInfo,
    InvestigationThreadInfo,
    ProductionCompanyInfo,
)
from aiss.models.movies.thriller_mystery_crime_model import ThrillerMysteryCrimeMovieInfo


@pytest.fixture
def thriller_movie_full():
    """Create a fully populated thriller movie instance for testing."""
    return ThrillerMysteryCrimeMovieInfo(
        title="The Silent Witness",
        tagline="The truth will be revealed.",
        synopsis="A detective investigates a series of murders connected to a decades-old conspiracy.",
        release_year=2024,
        runtime_minutes=128,
        genres=["Thriller", "Mystery", "Crime"],
        mpaa_rating="R",
        directors=["Thriller Director"],
        writers=["Mystery Writer"],
        producers=["Crime Producer"],
        original_language="English",
        countries=["USA"],
        rating=8.1,
        keywords=["conspiracy", "detective", "murder"],
        cast=[
            CastMemberInfo(character="Detective Marcus Reid", actor="Leading Actor", role="Lead"),
            CastMemberInfo(character="Officer Sarah Chen", actor="Supporting Actress", role="Supporting"),
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Suspense Studios",
                founded_year=1998,
                start_year=2023,
                end_year=2024,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=35000000, gross_worldwide=180000000, gross_domestic=75000000),
        awards=["Best Thriller", "Best Screenplay"],
        soundtrack_highlights=["Tense score by Suspense Composer"],
        narrative_hook="Serial killer targets witnesses from old trials - detective's own case included",
        investigation_threads=[
            InvestigationThreadInfo(
                thread="The Witness Murders",
                suspect_or_focus="Serial killer targeting witnesses",
                clues=["Matching crime scene signatures", "20-year timeline pattern"],
                status="Active",
            ),
            InvestigationThreadInfo(
                thread="The Corporate Conspiracy",
                suspect_or_focus="Pharmaceutical company executives",
                clues=["Financial records", "Whistleblower testimony"],
                status="Active",
            ),
        ],
        twists=["Reid's partner is compromised", "Victims were willing participants"],
        suspects=["Corrupt politician", "Vengeful ex-convict", "Grieving family member"],
        law_enforcement_agencies=["FBI", "Local Police Department"],
        tension_profile="Dark and cerebral with escalating action sequences",
        evidence_chain=["Crime scene signatures", "Financial records", "Whistleblower testimony"],
    )


def test_thriller_basic_creation():
    """Test basic thriller movie creation."""
    movie = ThrillerMysteryCrimeMovieInfo(title="Test Thriller")
    assert movie.title == "Test Thriller"
    assert movie.model_name == "ThrillerMysteryCrimeMovieInfo"


def test_thriller_additional_fact_pairs(thriller_movie_full):
    """Test additional fact pairs generation."""
    facts = dict(thriller_movie_full._additional_fact_pairs())
    assert "Serial killer" in facts["Hook"]
    assert "cerebral" in facts["Tension"]


def test_thriller_extra_tables(thriller_movie_full):
    """Test extra tables generation."""
    tables = thriller_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Investigation Threads" in titles


def test_thriller_extra_panels(thriller_movie_full):
    """Test extra panels generation."""
    panels = thriller_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert "Twists" in panel_titles
    assert "Suspects" in panel_titles
    assert "Evidence Chain" in panel_titles
    assert "Agencies" in panel_titles


def test_thriller_render_includes_content(thriller_movie_full, console):
    """Test render includes all expected content."""
    thriller_movie_full.render(console)
    text = console.export_text()
    assert "The Silent Witness" in text
    assert "The truth will be revealed." in text


def test_thriller_instruction_helpers():
    """Test instruction helper methods."""
    combined = ThrillerMysteryCrimeMovieInfo.get_instructions(["Build suspense"])
    assert "Additional context" in combined
    assert "Build suspense" in combined

    prompt = ThrillerMysteryCrimeMovieInfo.get_user_prompt("Test Thriller")
    assert "Test Thriller" in prompt

    formatted = ThrillerMysteryCrimeMovieInfo.json_format_instructions()
    assert "JSON" in formatted


def test_thriller_investigation_threads(thriller_movie_full):
    """Test investigation threads data."""
    assert len(thriller_movie_full.investigation_threads) == 2
    assert thriller_movie_full.investigation_threads[0].thread == "The Witness Murders"
    assert "Serial killer" in thriller_movie_full.investigation_threads[0].suspect_or_focus


def test_thriller_red_herrings(thriller_movie_full):
    """Test suspects list."""
    assert len(thriller_movie_full.suspects) == 3
    assert "Corrupt politician" in thriller_movie_full.suspects


def test_thriller_major_twists(thriller_movie_full):
    """Test twists list."""
    assert len(thriller_movie_full.twists) == 2
    assert "partner is compromised" in thriller_movie_full.twists[0]


def test_thriller_procedural_elements(thriller_movie_full):
    """Test evidence chain list."""
    assert len(thriller_movie_full.evidence_chain) == 3
    assert "Financial records" in thriller_movie_full.evidence_chain


def test_thriller_empty_optional_fields(console):
    """Test movie with minimal data."""
    movie = ThrillerMysteryCrimeMovieInfo(
        title="Minimal Thriller",
        synopsis="Basic thriller",
    )
    movie.render(console)
    facts = dict(movie._additional_fact_pairs())
    assert isinstance(facts, dict)


def test_thriller_roundtrip():
    """Test serialization roundtrip."""
    original = ThrillerMysteryCrimeMovieInfo(
        title="Roundtrip Thriller",
        synopsis="Testing serialization",
        release_year=2024,
        runtime_minutes=120,
        narrative_hook="Test hook",
        tension_profile="Test tension",
    )
    data = original.to_dict()
    restored = ThrillerMysteryCrimeMovieInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.narrative_hook == original.narrative_hook
    assert restored.tension_profile == original.tension_profile


def test_investigation_thread_info_table_schema():
    """Test InvestigationThreadInfo has table schema."""
    schema = InvestigationThreadInfo.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Thread" in headers
