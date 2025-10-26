import json

import pytest

from aiss.models.movies._base import (
    BoxOfficeInfo,
    CastMemberInfo,
    CharacterArcInfo,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.movies.drama_model import DramaMovieInfo


@pytest.fixture
def drama_movie_full():
    return DramaMovieInfo(
        title="Echoes of QA",
        tagline="Perfection has a cost.",
        synopsis="A tight-knit team battles time to deliver a flawless build.",
        release_year=2024,
        runtime_minutes=132,
        genres=["Drama", "Thriller"],
        mpaa_rating="PG-13",
        directors=["A. Director"],
        writers=["B. Writer"],
        producers=["C. Producer"],
        original_language="English",
        countries=["USA"],
        rating=8.7,
        keywords=["quality", "sacrifice"],
        cast=[CastMemberInfo(character="Jordan", actor="R. Star", role="Lead")],
        production_companies=[
            ProductionCompanyInfo(
                name="Fixture Films",
                founded_year=2010,
                start_year=2022,
                end_year=2023,
                country="USA",
            )
        ],
        box_office=BoxOfficeInfo(budget=20000000, gross_worldwide=125000000, gross_domestic=45000000),
        distribution_info=[
            DistributionInfo(
                distributor="StreamGrid",
                territory="Worldwide",
                release_type="Streaming",
                start_year=2024,
                end_year=0,
                revenue=85000000,
            )
        ],
        awards=["Best Ensemble"],
        soundtrack_highlights=["Final Push"],
        themes=["Ambition", "Teamwork"],
        central_conflict="Delivering on impossible expectations",
        character_arcs=[
            CharacterArcInfo(
                name="Jordan",
                portrayed_by="R. Star",
                arc_summary="Learns to trust the team",
                motivation="Protect product vision",
                turning_points=["Shares roadmap", "Delegates critical task"],
                resolution_status="Empowered",
            )
        ],
        tone="Intimate",
        pivotal_moments=["Team rewrites the core module", "Public launch succeeds"],
    )


def test_drama_movie_additional_fact_pairs(drama_movie_full):
    facts = dict(drama_movie_full._additional_fact_pairs())
    assert facts["Conflict"] == "Delivering on impossible expectations"
    assert facts["Tone"] == "Intimate"


def test_drama_movie_extra_tables_and_panels(drama_movie_full):
    tables = drama_movie_full._extra_tables()
    assert tables
    titles = {title for title, _, _ in tables}
    assert "Character Arcs" in titles
    panels = drama_movie_full._extra_panels()
    assert panels
    panel_titles = {title for title, _ in panels}
    assert {"Themes", "Pivotal Moments"}.issubset(panel_titles)


def test_drama_movie_render_includes_lists(drama_movie_full, console):
    drama_movie_full.render(console)
    text = console.export_text()
    assert "Perfection has a cost." in text
    assert "Ambition" in text
    assert "StreamGrid" in text


def test_drama_movie_instruction_helpers():
    combined = DramaMovieInfo.get_instructions(["Stress awards potential"])
    assert "Additional context" in combined
    assert "- Stress awards potential" in combined
    prompt = DramaMovieInfo.get_user_prompt("Echoes of QA")
    assert "Echoes of QA" in prompt
    formatted = DramaMovieInfo.json_format_instructions()
    assert "Respond with JSON" in formatted
    start = formatted.find("{")
    end = formatted.rfind("}")
    assert start != -1 and end != -1 and end > start
    parsed = json.loads(formatted[start : end + 1])
    assert "properties" in parsed
