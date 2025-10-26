import pytest

from aiss.models.shared import TableSchema
from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.drama_model import (
    DramaAwardRecognition,
    DramaCharacterProfile,
    DramaShowInfo,
    DramaStoryArc,
)


@pytest.fixture
def drama_show_full():
    return DramaShowInfo(
        title="Testing Grounds",
        logline="An elite QA squad protects the multiverse from regressions.",
        show_summary="Each season the team audits a new reality while juggling personal stakes.",
        tone="Moody",
        themes=["Resilience", "Trust"],
        primary_setting="Neo Seattle",
        season_count=3,
        episode_count=24,
        average_runtime_minutes=55,
        age_rating="TV-MA",
        release_start_year=2020,
        release_end_year=2023,
        showrunners=["Pat Lead"],
        head_writers=["Jamie Script"],
        directors=["Sam Vision"],
        composers=["Kelly Keys"],
        characters=[
            DramaCharacterProfile(
                name="Alex",
                actor="Robin Star",
                arc_summary="Learns to delegate",
                driving_conflict="Perfectionism",
                key_relationships=["Jordan"],
                season_introduced=1,
                current_status="Active",
                notable_episodes=["S01E03"],
            )
        ],
        major_story_arcs=[
            DramaStoryArc(
                arc_title="Broken Timeline",
                season_focus=2,
                episode_span="S02E01-S02E08",
                synopsis="Team mends a fragmented timeline",
                primary_themes=["Forgiveness"],
                resolution_status="Resolved",
                key_turning_point="Alex sacrifices timeline",
            )
        ],
        awards=[
            DramaAwardRecognition(
                award_body="Emmys",
                category="Best Drama",
                year=2022,
                recipient="Testing Grounds",
                result="Winner",
                notes="Season two finale",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="TV Weekly",
                reviewer="Casey Critic",
                score=9.1,
                summary="Inventive and heartfelt",
                quote="A rare blend of head and heart.",
                publication_date="2022-09-15",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Adults 25-34",
                average_viewers=2500000,
                share=4.2,
                engagement_notes="Streaming surge after finale",
            )
        ],
        production_companies=[
            ProductionCompanyInfo(
                name="Fixture Studios",
                founded_year=2005,
                start_year=2019,
                end_year=2023,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="StreamGrid",
                country="USA",
                start_year=2020,
                end_year=2023,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="Global Syndication",
                territory="Worldwide",
                release_type="Streaming",
                start_year=2020,
                end_year=0,
                revenue=150000000,
            )
        ],
    )


def test_drama_show_render_outputs_key_details(drama_show_full, console):
    drama_show_full.render(console)
    output = console.export_text()
    assert "Moody" in output
    assert "Resilience" in output
    assert "StreamGrid" in output


def test_drama_show_fact_pairs_contains_run_window(drama_show_full):
    facts = dict(drama_show_full._fact_pairs())
    assert facts["Run"] == "2020 - 2023"
    assert facts["Tone"] == "Moody"


def test_drama_show_table_sections_use_table_schema(drama_show_full):
    sections = drama_show_full._table_sections()
    assert sections
    for _, schema, rows in sections:
        assert schema
        assert rows
        assert all(isinstance(column, TableSchema) for column in schema)


def test_drama_show_instructions_include_context_block():
    text = DramaShowInfo.get_instructions(["Emphasise international roll-out"])
    assert "Additional context" in text
    assert "- Emphasise international roll-out" in text


def test_drama_show_json_format_mentions_expected_keys():
    formatted = DramaShowInfo.json_format_instructions()
    assert "OUTPUT FORMAT" in formatted
    assert "major_story_arcs" in formatted
