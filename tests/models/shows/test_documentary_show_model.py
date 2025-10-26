"""Tests for DocumentaryFactualShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.documentary_model import (
    ArchiveMaterial,
    DocumentaryEpisode,
    DocumentaryFactualShowInfo,
    InterviewSubject,
)


@pytest.fixture
def documentary_show_full():
    """Create a fully populated documentary show instance for testing."""
    return DocumentaryFactualShowInfo(
        title="Planet Earth: The Complete Story",
        premise="Comprehensive exploration of Earth's ecosystems",
        show_summary="Groundbreaking documentary series exploring diverse habitats and wildlife.",
        series_type="Nature Documentary",
        narrative_approach="Observational with expert narration",
        educational_focus=["Conservation", "Ecology", "Wildlife behavior"],
        tone="Awe-inspiring and educational",
        primary_setting="Global locations",
        season_count=3,
        episode_count=30,
        average_episode_length_minutes=50,
        release_start_year=2006,
        release_end_year=2016,
        age_rating="TV-G",
        production_techniques=["4K cinematography", "Aerial drones", "Time-lapse"],
        episodes=[
            DocumentaryEpisode(
                title="From Pole to Pole",
                focus="Journey from Arctic to Antarctic",
                runtime_minutes=50,
                key_subjects=["Polar bears", "Penguins"],
                narrative_devices=["Time-lapse", "Aerial footage"],
            ),
            DocumentaryEpisode(
                title="Mountains",
                focus="Life in mountain environments",
                runtime_minutes=50,
                key_subjects=["Snow leopards", "Golden eagles"],
                narrative_devices=["Slow motion", "Tracking shots"],
            ),
        ],
        interview_subjects=[
            InterviewSubject(
                name="Dr. Jane Goodall",
                expertise="Primatology",
                affiliation="Jane Goodall Institute",
                role_in_story="Expert commentary on conservation",
                standout_quote="We have a window of time to make a difference",
            )
        ],
        archive_materials=[
            ArchiveMaterial(
                material_type="Archival footage",
                description="Historical conservation efforts",
                source="BBC Archives",
                year=1960,
                usage="Contrast past and present",
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="The Guardian",
                reviewer="David Attenborough",
                score=10.0,
                summary="Revolutionary nature filmmaking",
                quote="The most ambitious natural history series ever",
                publication_date="2006-03-05",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="UK",
                demographic="All ages",
                average_viewers=10000000,
                share=6.5,
                engagement_notes="Highest rated documentary series",
            )
        ],
        narrators=["David Attenborough"],
        directors=["Alastair Fothergill"],
        production_companies=[
            ProductionCompanyInfo(
                name="BBC Natural History Unit",
                founded_year=1957,
                start_year=2003,
                end_year=2016,
                country="UK",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="BBC One",
                country="UK",
                start_year=2006,
                end_year=2016,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="BBC Worldwide",
                territory="Global",
                release_type="Broadcast + Streaming",
                start_year=2006,
                end_year=0,
                revenue=300000000,
            )
        ],
    )


def test_documentary_basic_creation():
    """Test basic show creation."""
    show = DocumentaryFactualShowInfo(title="Test Documentary")
    assert show.title == "Test Documentary"
    assert show.model_name == "DocumentaryFactualShowInfo"


def test_documentary_fact_pairs(documentary_show_full):
    """Test fact pairs generation."""
    facts = dict(documentary_show_full._fact_pairs())
    assert "2006 - 2016" == facts["Run"]
    assert facts["Rating"] == "TV-G"


def test_documentary_table_sections(documentary_show_full):
    """Test table sections generation."""
    sections = documentary_show_full._table_sections()
    assert sections
    titles = {title for title, _, _ in sections}
    assert "Episodes" in titles or "Interview Subjects" in titles


def test_documentary_render_includes_content(documentary_show_full, console):
    """Test render includes all expected content."""
    documentary_show_full.render(console)
    text = console.export_text()
    assert "Planet Earth" in text


def test_documentary_instruction_helpers():
    """Test instruction helper methods."""
    combined = DocumentaryFactualShowInfo.get_instructions(["Focus on conservation"])
    assert "Additional context" in combined

    prompt = DocumentaryFactualShowInfo.get_user_prompt("Test Doc")
    assert "Test Doc" in prompt

    formatted = DocumentaryFactualShowInfo.json_format_instructions()
    assert "JSON" in formatted


def test_documentary_episodes(documentary_show_full):
    """Test episodes data."""
    assert len(documentary_show_full.episodes) == 2
    assert documentary_show_full.episodes[0].title == "From Pole to Pole"


def test_documentary_interview_subjects(documentary_show_full):
    """Test interview subjects data."""
    assert len(documentary_show_full.interview_subjects) == 1
    assert documentary_show_full.interview_subjects[0].name == "Dr. Jane Goodall"


def test_documentary_archive_materials(documentary_show_full):
    """Test archive materials data."""
    assert len(documentary_show_full.archive_materials) == 1
    assert documentary_show_full.archive_materials[0].year == 1960


def test_documentary_empty_optional_fields(console):
    """Test show with minimal data."""
    show = DocumentaryFactualShowInfo(
        title="Minimal Documentary",
        premise="Basic premise",
    )
    show.render(console)
    facts = dict(show._fact_pairs())
    assert isinstance(facts, dict)


def test_documentary_roundtrip():
    """Test serialization roundtrip."""
    original = DocumentaryFactualShowInfo(
        title="Roundtrip Documentary",
        show_summary="Testing serialization",
        season_count=2,
        episode_count=20,
        narrative_style="Observational",
    )
    data = original.to_dict()
    restored = DocumentaryFactualShowInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.narrative_style == original.narrative_style


def test_documentary_episode_table_schema():
    """Test DocumentaryEpisode has table schema."""
    schema = DocumentaryEpisode.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Episode" in headers


def test_interview_subject_table_schema():
    """Test InterviewSubject has table schema."""
    schema = InterviewSubject.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Subject" in headers


def test_archive_material_table_schema():
    """Test ArchiveMaterial has table schema."""
    schema = ArchiveMaterial.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Material" in headers
