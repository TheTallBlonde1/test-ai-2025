"""Tests for FamilyAnimationKidsShowInfo model."""

import pytest

from aiss.models.shows._base import (
    AudienceEngagement,
    BroadcastInfo,
    CriticalResponse,
    DistributionInfo,
    ProductionCompanyInfo,
)
from aiss.models.shows.family_kids_model import (
    EducationalSegment,
    FamilyAnimationKidsShowInfo,
    FamilyCharacterProfile,
    ParentGuideNote,
)


@pytest.fixture
def family_kids_show_full():
    """Create a fully populated family/kids show instance for testing."""
    return FamilyAnimationKidsShowInfo(
        title="Learn and Grow",
        premise="Educational adventures with animated friends",
        show_summary="Animated series teaching social-emotional skills to preschoolers.",
        target_age_range="3-6 years",
        developmental_goals=["Emotional intelligence", "Problem solving", "Friendship"],
        tone="Warm and encouraging",
        primary_setting="Colorful neighborhood",
        season_count=5,
        episode_count=100,
        episode_length_minutes=12,
        release_start_year=2015,
        release_end_year=2020,
        age_rating="TV-Y",
        animation_style="2D bright colors",
        music_integration="Original songs in each episode",
        characters=[
            FamilyCharacterProfile(
                name="Buddy Bear",
                voice_actor="Voice Actor A",
                role="Protagonist",
                species_or_type="Bear",
                personality_traits=["Curious", "Kind", "Helpful"],
                lesson_focus="Sharing and cooperation",
                catchphrases=["Let's work together!"],
            )
        ],
        educational_segments=[
            EducationalSegment(
                episode="The Sharing Tree",
                topic="Sharing",
                skills_targeted=["Cooperation", "Empathy"],
                teaching_approach="Storytelling with music",
                takeaway="Sharing makes everyone happy",
            )
        ],
        parent_guides=[
            ParentGuideNote(
                topic="Sharing",
                conversation_starters=["What did you share today?"],
                emotional_notes="Children may need reassurance",
                reinforcement_ideas=["Practice sharing toys"],
            )
        ],
        critical_reception=[
            CriticalResponse(
                outlet="Common Sense Media",
                reviewer="Parents Team",
                score=9.0,
                summary="Excellent educational content",
                quote="Perfect for preschool learning",
                publication_date="2015-09-01",
            )
        ],
        audience_metrics=[
            AudienceEngagement(
                region="US",
                demographic="Children 3-6",
                average_viewers=2000000,
                share=5.0,
                engagement_notes="High repeat viewing",
            )
        ],
        creators=["Creator Name"],
        animators=["Animation Studio"],
        voice_directors=["Voice Director"],
        production_companies=[
            ProductionCompanyInfo(
                name="Kids Animation Studio",
                founded_year=2010,
                start_year=2014,
                end_year=2020,
                country="USA",
            )
        ],
        broadcast_info=[
            BroadcastInfo(
                network="PBS Kids",
                country="USA",
                start_year=2015,
                end_year=2020,
            )
        ],
        distribution_info=[
            DistributionInfo(
                distributor="PBS Distribution",
                territory="US",
                release_type="Broadcast",
                start_year=2015,
                end_year=0,
                revenue=50000000,
            )
        ],
    )


def test_family_kids_basic_creation():
    """Test basic show creation."""
    show = FamilyAnimationKidsShowInfo(title="Test Kids Show")
    assert show.title == "Test Kids Show"
    assert show.model_name == "FamilyAnimationKidsShowInfo"


def test_family_kids_fact_pairs(family_kids_show_full):
    """Test fact pairs generation."""
    facts = dict(family_kids_show_full._fact_pairs())
    assert "3-6 years" == facts["Target Age"]
    assert "2015 - 2020" == facts["Run"]


def test_family_kids_table_sections(family_kids_show_full):
    """Test table sections generation."""
    sections = family_kids_show_full._table_sections()
    assert sections
    titles = {title for title, _, _ in sections}
    assert "Characters" in titles or "Educational Segments" in titles


def test_family_kids_render_includes_content(family_kids_show_full, console):
    """Test render includes all expected content."""
    family_kids_show_full.render(console)
    text = console.export_text()
    assert "Learn and Grow" in text


def test_family_kids_instruction_helpers():
    """Test instruction helper methods."""
    combined = FamilyAnimationKidsShowInfo.get_instructions(["Focus on education"])
    assert "Additional context" in combined

    prompt = FamilyAnimationKidsShowInfo.get_user_prompt("Test Show")
    assert "Test Show" in prompt

    formatted = FamilyAnimationKidsShowInfo.json_format_instructions()
    assert "JSON" in formatted


def test_family_kids_characters(family_kids_show_full):
    """Test characters data."""
    assert len(family_kids_show_full.characters) == 1
    assert family_kids_show_full.characters[0].name == "Buddy Bear"


def test_family_kids_educational_segments(family_kids_show_full):
    """Test educational segments data."""
    assert len(family_kids_show_full.educational_segments) == 1
    assert family_kids_show_full.educational_segments[0].topic == "Sharing"


def test_family_kids_parent_guides(family_kids_show_full):
    """Test parent guides data."""
    assert len(family_kids_show_full.parent_guides) == 1
    assert family_kids_show_full.parent_guides[0].topic == "Sharing"


def test_family_kids_empty_optional_fields(console):
    """Test show with minimal data."""
    show = FamilyAnimationKidsShowInfo(
        title="Minimal Kids Show",
        premise="Basic premise",
    )
    show.render(console)
    facts = dict(show._fact_pairs())
    assert isinstance(facts, dict)


def test_family_kids_roundtrip():
    """Test serialization roundtrip."""
    original = FamilyAnimationKidsShowInfo(
        title="Roundtrip Kids Show",
        premise="Testing serialization",
        season_count=3,
        episode_count=30,
        target_age_range="3-7",
    )
    data = original.to_dict()
    restored = FamilyAnimationKidsShowInfo.from_dict(data)

    assert restored.title == original.title
    assert restored.target_age_range == original.target_age_range


def test_family_character_profile_table_schema():
    """Test FamilyCharacterProfile has table schema."""
    schema = FamilyCharacterProfile.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Character" in headers


def test_educational_segment_table_schema():
    """Test EducationalSegment has table schema."""
    schema = EducationalSegment.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Episode" in headers


def test_parent_guide_note_table_schema():
    """Test ParentGuideNote has table schema."""
    schema = ParentGuideNote.table_schema()
    assert len(schema) > 0
    headers = {s.header for s in schema}
    assert "Topic" in headers
