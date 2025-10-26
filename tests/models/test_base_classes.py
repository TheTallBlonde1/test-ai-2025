"""Tests for base class functionality across all model types."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from aiss.models.games._base import GameFormatBase
from aiss.models.shows._base import ShowFormatBase, _dump


@pytest.fixture
def console():
    """Provide a console for rendering tests."""
    from rich.console import Console

    return Console(record=True, force_terminal=False, width=80, legacy_windows=False)


class TestDumpFunction:
    """Test _dump utility function."""

    def test_dump_with_model_dump(self):
        """Test _dump with Pydantic v2 model_dump method."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str
            value: int

        instance = TestModel(name="test", value=42)
        result = _dump(instance)
        assert result == {"name": "test", "value": 42}

    def test_dump_with_legacy_dict(self):
        """Test _dump fallback to legacy dict() method."""
        # Create a mock object that only has dict() method
        mock_obj = Mock()
        mock_obj.model_dump = None
        mock_obj.dict = Mock(return_value={"legacy": "data"})

        result = _dump(mock_obj)
        assert result == {"legacy": "data"}
        mock_obj.dict.assert_called_once()

    def test_dump_with_no_methods_raises(self):
        """Test _dump raises TypeError when neither method exists."""
        mock_obj = Mock()
        mock_obj.model_dump = None
        mock_obj.dict = None

        with pytest.raises(TypeError, match="does not support model_dump/dict"):
            _dump(mock_obj)


class TestJsonModel:
    """Test JsonModel base functionality."""

    def test_json_model_to_dict(self):
        """Test to_dict works on JsonModel subclass."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        data = instance.to_dict()
        assert isinstance(data, dict)
        assert "title" in data

    def test_json_model_from_dict(self):
        """Test from_dict works on JsonModel subclass."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        data = {"title": "Test Show", "show_summary": "Test"}
        instance = ActionAdventureFantasyShowInfo.from_dict(data)
        assert instance.title == "Test Show"

    def test_json_model_to_json_file(self):
        """Test to_json writes to file."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            instance.to_json(temp_path)
            assert Path(temp_path).exists()

            with open(temp_path, "r") as f:
                data = json.load(f)
            assert data["title"] == "Test"
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_json_model_from_json_file(self):
        """Test from_json reads from file."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"title": "File Test", "show_summary": "Test"}, f)
            temp_path = f.name

        try:
            instance = ActionAdventureFantasyShowInfo.from_json(temp_path)
            assert instance.title == "File Test"
        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestShowFormatBase:
    """Test ShowFormatBase functionality."""

    def test_show_format_base_class_variables(self):
        """Test ShowFormatBase has required class variables."""
        assert hasattr(ShowFormatBase, "summary_title_fallback")
        assert hasattr(ShowFormatBase, "summary_panel_style")
        assert hasattr(ShowFormatBase, "summary_attributes")
        assert hasattr(ShowFormatBase, "facts_panel_title")
        assert hasattr(ShowFormatBase, "facts_panel_style")

    def test_show_format_render_wikipedia_summary_empty(self, console):
        """Test render_wikipedia_summary with empty string."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        instance.wikipedia_summary = ""
        instance.render_wikipedia_summary(console)
        # Should not crash and should not add anything
        output = console.export_text()
        assert "Context" not in output

    def test_show_format_render_wikipedia_summary_with_content(self, console):
        """Test render_wikipedia_summary with content."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        instance.wikipedia_summary = "This is context from Wikipedia."
        instance.render_wikipedia_summary(console)
        output = console.export_text()
        assert "Context" in output
        assert "Wikipedia" in output

    def test_show_format_summary_panel_with_tagline(self):
        """Test _summary_panel with tagline."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test Show", tagline="Amazing tagline", show_summary="Summary text")
        title, lines, style = instance._summary_panel()
        assert title == "Test Show"
        assert "Amazing tagline" in lines
        assert isinstance(style, str)

    def test_show_format_summary_panel_no_attributes(self):
        """Test _summary_panel with no summary attributes."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        title, lines, style = instance._summary_panel()
        assert title == "Test"
        assert len(lines) > 0

    def test_show_format_summary_panel_fallback_to_show_summary(self):
        """Test _summary_panel falls back to show_summary when attributes are empty."""
        from aiss.models.shows import DramaShowInfo

        # Create instance with empty tagline but with show_summary
        instance = DramaShowInfo(title="Test", tagline="", show_summary="Fallback summary")
        title, lines, style = instance._summary_panel()
        assert "Fallback summary" in lines or "Fallback summary" in str(lines)

    def test_show_format_summary_panel_no_summary_at_all(self):
        """Test _summary_panel with no summary whatsoever."""
        from aiss.models.shows import DramaShowInfo

        instance = DramaShowInfo(title="Test", tagline="", show_summary="")
        title, lines, style = instance._summary_panel()
        assert "(no summary provided)" in lines or "(no summary provided)" in str(lines)

    def test_show_format_fact_pairs_default(self):
        """Test _fact_pairs returns empty sequence by default."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        # The default implementation returns empty
        # But child classes override it
        facts = instance._fact_pairs()
        assert isinstance(facts, (list, tuple))

    def test_show_format_table_sections_default(self):
        """Test _table_sections returns empty sequence by default."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        sections = instance._table_sections()
        assert isinstance(sections, (list, tuple))

    def test_show_format_extra_panels_default(self):
        """Test _extra_panels returns empty sequence by default."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test")
        panels = instance._extra_panels()
        assert isinstance(panels, (list, tuple))

    def test_show_format_render_with_fact_pairs(self, console):
        """Test render with fact pairs."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test Show", show_summary="Test summary", season_count=3, episode_count=30)
        instance.render(console)
        output = console.export_text()
        assert "Test Show" in output

    def test_show_format_render_with_tables(self, console):
        """Test render with table sections."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo, HeroProfile

        instance = ActionAdventureFantasyShowInfo(title="Test Show", show_summary="Test summary", heroes=[HeroProfile(name="Hero", archetype="Warrior", power_set="Strength", arc="Growth")])
        instance.render(console)
        output = console.export_text()
        assert "Test Show" in output

    def test_show_format_render_with_extra_panels(self, console):
        """Test render with extra panels."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        instance = ActionAdventureFantasyShowInfo(title="Test Show", show_summary="Test summary", mythology_notes="Ancient myths and legends")
        instance.render(console)
        output = console.export_text()
        assert "Test Show" in output

    def test_show_format_render_all_empty(self, console):
        """Test render when all content is empty."""
        from aiss.models.shows import DramaShowInfo

        instance = DramaShowInfo(title="Minimal", tagline="", show_summary="")
        instance.render(console)
        output = console.export_text()
        assert "Minimal" in output
        assert "(no summary provided)" in output

    def test_show_format_render_with_empty_fact_pairs(self, console):
        """Test render with empty fact pairs list."""
        from aiss.models.shows import DramaShowInfo

        instance = DramaShowInfo(title="Test", show_summary="Summary")
        # Most show models return empty fact_pairs by default
        instance.render(console)
        output = console.export_text()
        assert "Test" in output

    def test_show_format_render_with_empty_table_sections(self, console):
        """Test render with empty table sections."""
        from aiss.models.shows import ComedyShowInfo

        instance = ComedyShowInfo(title="Test", show_summary="Summary")
        instance.render(console)
        output = console.export_text()
        assert "Test" in output

    def test_show_format_render_with_empty_panel_body(self, console):
        """Test _extra_panels with empty body (should be skipped)."""
        from aiss.models.shows.action_fantasy_model import ActionAdventureFantasyShowInfo

        # Set mythology_notes to empty to trigger skip logic
        instance = ActionAdventureFantasyShowInfo(title="Test", show_summary="Summary", mythology_notes="")
        instance.render(console)
        output = console.export_text()
        assert "Test" in output
        # Empty panels shouldn't appear

    def test_show_format_render_with_character_info(self, console):
        """Test render with character info tables."""
        from aiss.models.shows.drama_model import DramaCharacterProfile, DramaShowInfo

        instance = DramaShowInfo(
            title="Test Show",
            show_summary="Test summary",
            characters=[
                DramaCharacterProfile(
                    name="Main Character",
                    actor="John Doe",
                    arc="Hero's journey",
                    significance="Protagonist",
                )
            ],
        )
        instance.render(console)
        output = console.export_text()
        assert "Test Show" in output
        assert "Main Character" in output or "John Doe" in output

    def test_show_format_render_with_critical_response(self, console):
        """Test render with critical response."""
        from aiss.models.shows._base import CriticalResponse
        from aiss.models.shows.drama_model import DramaShowInfo

        instance = DramaShowInfo(
            title="Test Show",
            show_summary="Test summary",
            critical_reception=[
                CriticalResponse(
                    outlet="Test Magazine",
                    reviewer="Jane Smith",
                    score=8.5,
                    summary="Great show",
                    quote="Fantastic",
                    publication_date="2020-01-01",
                )
            ],
        )
        instance.render(console)
        output = console.export_text()
        assert "Test Show" in output

    def test_show_format_render_with_audience_data(self, console):
        """Test render with audience data."""
        from aiss.models.shows._base import AudienceEngagement
        from aiss.models.shows.drama_model import DramaShowInfo

        instance = DramaShowInfo(
            title="Test Show",
            show_summary="Test summary",
            audience_metrics=[
                AudienceEngagement(
                    region="US",
                    demographic="18-49",
                    average_viewers=5000000,
                    share=25.5,
                    engagement_notes="Strong performance",
                )
            ],
        )
        instance.render(console)
        output = console.export_text()
        assert "Test Show" in output

    def test_game_format_render_with_empty_summary_attributes(self, console):
        """Test render fallback to game_summary when summary_attributes are empty."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(
            title="Test Game",
            game_summary="Fallback summary text",
        )
        # Clear any summary attributes to force fallback
        for attr in instance.summary_attributes:
            if hasattr(instance, attr):
                setattr(instance, attr, "")

        instance.render(console)
        output = console.export_text()
        assert "Fallback summary" in output or "Test Game" in output

    def test_game_format_render_with_no_summary(self, console):
        """Test render fallback to '(no summary provided)' when all summaries empty."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(
            title="Test Game",
            game_summary="",
        )
        # Clear all summary attributes
        for attr in instance.summary_attributes:
            if hasattr(instance, attr):
                setattr(instance, attr, "")

        instance.render(console)
        output = console.export_text()
        assert "(no summary provided)" in output or "Test Game" in output

    def test_show_format_render_with_empty_summary_attributes(self, console):
        """Test show render fallback to show_summary when summary_attributes are empty."""
        from aiss.models.shows.drama_model import DramaShowInfo

        instance = DramaShowInfo(
            title="Test Show",
            show_summary="Fallback summary for show",
        )
        # Clear any summary attributes to force fallback
        for attr in instance.summary_attributes:
            if hasattr(instance, attr):
                setattr(instance, attr, "")

        instance.render(console)
        output = console.export_text()
        assert "Fallback summary" in output or "Test Show" in output

    def test_show_format_render_with_no_summary(self, console):
        """Test show render fallback to '(no summary provided)' when all summaries empty."""
        from aiss.models.shows.drama_model import DramaShowInfo

        instance = DramaShowInfo(
            title="Test Show",
            show_summary="",
        )
        # Clear all summary attributes
        for attr in instance.summary_attributes:
            if hasattr(instance, attr):
                setattr(instance, attr, "")

        instance.render(console)
        output = console.export_text()
        assert "(no summary provided)" in output or "Test Show" in output

    def test_crew_member_info_serialization(self):
        """Test CrewMemberInfo to_dict/from_dict/to_json/from_json."""
        import tempfile

        from aiss.models.movies._base import CrewMemberInfo

        instance = CrewMemberInfo(
            name="Test Crew",
            role="Director",
            department="Production",
            notable_work="Test Work",
        )

        # Test to_dict/from_dict
        data = instance.to_dict()
        assert data["name"] == "Test Crew"
        recreated = CrewMemberInfo.from_dict(data)
        assert recreated.name == "Test Crew"

        # Test to_json/from_json
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name
        try:
            instance.to_json(temp_path)
            loaded = CrewMemberInfo.from_json(temp_path)
            assert loaded.name == "Test Crew"
        finally:
            import os

            os.unlink(temp_path)

    def test_production_company_info_table_schema(self):
        """Test ProductionCompanyInfo table_schema."""
        from aiss.models.movies._base import ProductionCompanyInfo

        schema = ProductionCompanyInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "name" for s in schema)

    def test_production_company_info_serialization(self):
        """Test ProductionCompanyInfo to_dict/from_dict/to_json/from_json."""
        import tempfile

        from aiss.models.movies._base import ProductionCompanyInfo

        instance = ProductionCompanyInfo(
            name="Test Production",
            founded_year=2000,
            start_year=2020,
            end_year=2022,
            country="US",
        )

        # Test to_dict/from_dict
        data = instance.to_dict()
        assert data["name"] == "Test Production"
        recreated = ProductionCompanyInfo.from_dict(data)
        assert recreated.name == "Test Production"

        # Test to_json/from_json
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name
        try:
            instance.to_json(temp_path)
            loaded = ProductionCompanyInfo.from_json(temp_path)
            assert loaded.name == "Test Production"
        finally:
            import os

            os.unlink(temp_path)

    def test_box_office_info_table_schema(self):
        """Test BoxOfficeInfo table_schema."""
        from aiss.models.movies._base import BoxOfficeInfo

        schema = BoxOfficeInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "budget" for s in schema)

    def test_char_info_str_repr(self):
        """Test CharInfoInfo __str__ and __repr__."""
        from aiss.models.shows._base import CharInfoInfo

        instance = CharInfoInfo(
            character="Test Char",
            actor="Test Actor",
            relationship="Friend",
            year_joined=2020,
        )

        str_repr = str(instance)
        assert "Test Char" in str_repr
        assert "Test Actor" in str_repr

        repr_str = repr(instance)
        assert "CharInfoInfo" in repr_str
        assert "Test Char" in repr_str

    def test_show_production_company_info_table_schema(self):
        """Test shows ProductionCompanyInfo table_schema."""
        from aiss.models.shows._base import ProductionCompanyInfo

        schema = ProductionCompanyInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "name" for s in schema)

    def test_box_office_info_serialization(self):
        """Test BoxOfficeInfo to_dict/from_dict/to_json/from_json."""
        import tempfile

        from aiss.models.movies._base import BoxOfficeInfo

        instance = BoxOfficeInfo(
            budget=10000000,
            gross_worldwide=50000000,
            gross_domestic=20000000,
        )

        # Test to_dict/from_dict
        data = instance.to_dict()
        assert data["budget"] == 10000000
        recreated = BoxOfficeInfo.from_dict(data)
        assert recreated.budget == 10000000

        # Test to_json/from_json
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name
        try:
            instance.to_json(temp_path)
            loaded = BoxOfficeInfo.from_json(temp_path)
            assert loaded.budget == 10000000
        finally:
            import os

            os.unlink(temp_path)

    def test_distribution_info_table_schema(self):
        """Test DistributionInfo table_schema."""
        from aiss.models.movies._base import DistributionInfo

        schema = DistributionInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "distributor" for s in schema)

    def test_distribution_info_serialization(self):
        """Test DistributionInfo to_dict/from_dict/to_json/from_json."""
        import tempfile

        from aiss.models.movies._base import DistributionInfo

        instance = DistributionInfo(
            distributor="Test Distributor",
            territory="US",
            release_type="theatrical",
            start_year=2020,
            end_year=2022,
            revenue=5000000,
        )

        # Test to_dict/from_dict
        data = instance.to_dict()
        assert data["distributor"] == "Test Distributor"
        recreated = DistributionInfo.from_dict(data)
        assert recreated.distributor == "Test Distributor"

        # Test to_json/from_json
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name
        try:
            instance.to_json(temp_path)
            loaded = DistributionInfo.from_json(temp_path)
            assert loaded.distributor == "Test Distributor"
        finally:
            import os

            os.unlink(temp_path)

    def test_show_production_company_str_repr(self):
        """Test shows ProductionCompanyInfo __str__ and __repr__."""
        from aiss.models.shows._base import ProductionCompanyInfo

        instance = ProductionCompanyInfo(
            name="Test Production",
            founded_year=2000,
            start_year=2020,
            end_year=2022,
            country="US",
        )

        str_repr = str(instance)
        assert "Test Production" in str_repr
        assert "US" in str_repr

        repr_str = repr(instance)
        assert "ProductionCompanyInfo" in repr_str
        assert "Test Production" in repr_str

    def test_broadcast_info_table_schema(self):
        """Test BroadcastInfo table_schema."""
        from aiss.models.shows._base import BroadcastInfo

        schema = BroadcastInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "network" for s in schema)

    def test_broadcast_info_str_repr(self):
        """Test BroadcastInfo __str__ and __repr__."""
        from aiss.models.shows._base import BroadcastInfo

        instance = BroadcastInfo(
            network="Test Network",
            country="US",
            start_year=2020,
            end_year=2022,
        )

        str_repr = str(instance)
        assert "Test Network" in str_repr
        assert "US" in str_repr

        repr_str = repr(instance)
        assert "BroadcastInfo" in repr_str
        assert "Test Network" in repr_str

    def test_show_distribution_info_table_schema(self):
        """Test shows DistributionInfo table_schema."""
        from aiss.models.shows._base import DistributionInfo

        schema = DistributionInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "distributor" for s in schema)

    def test_show_distribution_info_str_repr(self):
        """Test shows DistributionInfo __str__ and __repr__."""
        from aiss.models.shows._base import DistributionInfo

        instance = DistributionInfo(
            distributor="Test Distributor",
            territory="US",
            release_type="streaming",
            start_year=2020,
            end_year=2022,
            revenue=5000000,
        )

        str_repr = str(instance)
        assert "Test Distributor" in str_repr
        assert "US" in str_repr

        repr_str = repr(instance)
        assert "DistributionInfo" in repr_str
        assert "Test Distributor" in repr_str

    def test_show_box_office_info_str_repr(self):
        """Test shows BoxOfficeInfo __str__ and __repr__."""
        from aiss.models.shows._base import BoxOfficeInfo

        instance = BoxOfficeInfo(
            budget=10000000,
            gross_worldwide=50000000,
            gross_domestic=20000000,
        )

        str_repr = str(instance)
        assert str_repr  # Just check it doesn't error

        repr_str = repr(instance)
        assert "BoxOfficeInfo" in repr_str

    def test_base_movie_info_json_format_instructions(self):
        """Test BaseMovieInfo json_format_instructions method."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instructions = DramaMovieInfo.json_format_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 0
        assert "JSON" in instructions or "json" in instructions

    def test_base_movie_info_base_fact_pairs(self):
        """Test BaseMovieInfo _base_fact_pairs with various data."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test Movie",
            movie_summary="Test summary",
            release_year=2020,
            runtime_minutes=120,
            genres=["Drama", "Thriller"],
            mpaa_rating="PG-13",
            directors=["Director 1", "Director 2"],
            producers=["Producer 1"],
            writers=["Writer 1"],
            original_language="English",
            countries=["US", "UK"],
            rating=8.5,
        )

        facts = instance._base_fact_pairs()
        assert len(facts) > 0
        assert any("Release" in f[0] for f in facts)
        assert any("Runtime" in f[0] for f in facts)

    def test_base_movie_info_additional_fact_pairs(self):
        """Test BaseMovieInfo _additional_fact_pairs returns empty list."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(title="Test", movie_summary="Test")
        facts = instance._additional_fact_pairs()
        assert isinstance(facts, list)

    def test_base_movie_info_extra_tables(self):
        """Test BaseMovieInfo _extra_tables returns empty list."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(title="Test", movie_summary="Test")
        tables = instance._extra_tables()
        assert isinstance(tables, list)

    def test_base_movie_info_extra_panels(self):
        """Test BaseMovieInfo _extra_panels returns empty list."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(title="Test", movie_summary="Test")
        panels = instance._extra_panels()
        assert isinstance(panels, list)

    def test_base_movie_info_render_list_panel(self, console):
        """Test BaseMovieInfo _render_list_panel with items."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(title="Test", movie_summary="Test")
        instance._render_list_panel("Test Items", ["Item 1", "Item 2"], console)
        output = console.export_text()
        assert "Item 1" in output or "Test Items" in output

    def test_base_movie_info_render_list_panel_empty(self, console):
        """Test BaseMovieInfo _render_list_panel with no items."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(title="Test", movie_summary="Test")
        instance._render_list_panel("Test Items", [], console)
        output = console.export_text()
        # Should be empty or minimal
        assert len(output) < 50

    def test_base_movie_info_render_wikipedia_summary(self, console):
        """Test BaseMovieInfo _render_wikipedia_summary with content."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Test",
            wikipedia_summary="This is a Wikipedia summary",
        )
        instance._render_wikipedia_summary(console)
        output = console.export_text()
        assert "Wikipedia" in output or "Context" in output

    def test_base_movie_info_render_wikipedia_summary_empty(self, console):
        """Test BaseMovieInfo _render_wikipedia_summary with empty content."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Test",
            wikipedia_summary="",
        )
        instance._render_wikipedia_summary(console)
        output = console.export_text()
        # Should be empty
        assert len(output) < 20

    def test_base_movie_info_render_with_title_and_year(self, console):
        """Test BaseMovieInfo render formats title with year."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test Movie",
            movie_summary="Test summary",
            release_year=2020,
        )
        instance.render(console)
        output = console.export_text()
        assert "Test Movie" in output
        assert "2020" in output or "20" in output

    def test_show_box_office_info_table_schema(self):
        """Test shows BoxOfficeInfo table_schema."""
        from aiss.models.shows._base import BoxOfficeInfo

        schema = BoxOfficeInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "budget" for s in schema)

    def test_base_movie_info_render_no_title(self, console):
        """Test BaseMovieInfo render with no title (untitled)."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="",
            movie_summary="Test summary",
            release_year=2020,
        )
        instance.render(console)
        output = console.export_text()
        assert "untitled" in output.lower() or "2020" in output

    def test_base_movie_info_render_with_tagline(self, console):
        """Test BaseMovieInfo render includes tagline."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Synopsis text",
            tagline="Amazing tagline",
        )
        instance.render(console)
        output = console.export_text()
        assert "Amazing tagline" in output

    def test_base_movie_info_render_with_keywords(self, console):
        """Test BaseMovieInfo render shows keywords."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Synopsis",
            keywords=["thriller", "action", "mystery"],
        )
        instance.render(console)
        output = console.export_text()
        assert "Keywords" in output or "thriller" in output

    def test_base_movie_info_render_with_awards(self, console):
        """Test BaseMovieInfo render shows awards."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Synopsis",
            awards=["Oscar Best Picture", "Golden Globe"],
        )
        instance.render(console)
        output = console.export_text()
        assert "Awards" in output or "Oscar" in output

    def test_base_movie_info_render_with_soundtrack(self, console):
        """Test BaseMovieInfo render shows soundtrack."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Synopsis",
            soundtrack_highlights=["Song 1", "Song 2"],
        )
        instance.render(console)
        output = console.export_text()
        assert "Soundtrack" in output or "Song" in output

    def test_base_movie_info_render_with_notable_crew(self, console):
        """Test BaseMovieInfo render shows notable crew."""
        from aiss.models.movies._base import CrewMemberInfo
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Synopsis",
            notable_crew=[
                CrewMemberInfo(
                    name="Test Crew",
                    role="Cinematographer",
                    department="Camera",
                )
            ],
        )
        instance.render(console)
        output = console.export_text()
        assert "Crew" in output or "Test Crew" in output

    def test_base_movie_info_render_with_distribution(self, console):
        """Test BaseMovieInfo render shows distribution info."""
        from aiss.models.movies._base import DistributionInfo
        from aiss.models.movies.drama_model import DramaMovieInfo

        instance = DramaMovieInfo(
            title="Test",
            movie_summary="Synopsis",
            distribution_info=[
                DistributionInfo(
                    distributor="Test Dist",
                    territory="US",
                    release_type="theatrical",
                )
            ],
        )
        instance.render(console)
        output = console.export_text()
        assert "Distribution" in output or "Test Dist" in output


class TestShowDataModels:
    """Test show data model classes."""

    def test_critical_response_table_schema(self):
        """Test CriticalResponse table_schema method."""
        from aiss.models.shows._base import CriticalResponse

        schema = CriticalResponse.table_schema()
        assert len(schema) > 0
        assert any(s.name == "outlet" for s in schema)
        assert any(s.name == "reviewer" for s in schema)

    def test_audience_engagement_table_schema(self):
        """Test AudienceEngagement table_schema method."""
        from aiss.models.shows._base import AudienceEngagement

        schema = AudienceEngagement.table_schema()
        assert len(schema) > 0
        assert any(s.name == "region" for s in schema)
        assert any(s.name == "demographic" for s in schema)

    def test_char_info_table_schema(self):
        """Test CharInfoInfo table_schema method."""
        from aiss.models.shows._base import CharInfoInfo

        schema = CharInfoInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "character" for s in schema)
        assert any(s.name == "actor" for s in schema)


class TestMovieBaseInfo:
    """Test BaseMovieInfo functionality."""

    def test_base_movie_render_wikipedia_summary(self, console):
        """Test _render_wikipedia_summary method."""
        from aiss.models.movies.action_adventure_model import ActionAdventureMovieInfo

        instance = ActionAdventureMovieInfo(title="Test")
        instance.wikipedia_summary = "Movie context from Wikipedia."
        instance._render_wikipedia_summary(console)
        output = console.export_text()
        assert "Context" in output

    def test_base_movie_render_wikipedia_summary_empty(self, console):
        """Test _render_wikipedia_summary with empty string."""
        from aiss.models.movies.action_adventure_model import ActionAdventureMovieInfo

        instance = ActionAdventureMovieInfo(title="Test")
        instance.wikipedia_summary = ""
        instance._render_wikipedia_summary(console)
        output = console.export_text()
        assert output == "" or "Context" not in output

    def test_movie_data_models_table_schema(self):
        """Test table_schema for movie data models."""
        from aiss.models.movies._base import (
            ActionSetPieceInfo,
            BoxOfficeInfo,
            CastMemberInfo,
            CharacterArcInfo,
            CrewMemberInfo,
            DistributionInfo,
            FearMomentInfo,
            HumorBeatInfo,
            InvestigationThreadInfo,
            ProductionCompanyInfo,
            RomanticBeatInfo,
            SubjectFocusInfo,
        )

        schema = CastMemberInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "character" for s in schema)

        schema = CrewMemberInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "name" for s in schema)

        schema = ProductionCompanyInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "name" for s in schema)

        schema = BoxOfficeInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "budget" for s in schema)

        schema = DistributionInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "distributor" for s in schema)

        schema = CharacterArcInfo.table_schema()
        assert len(schema) > 0

        schema = ActionSetPieceInfo.table_schema()
        assert len(schema) > 0

        schema = HumorBeatInfo.table_schema()
        assert len(schema) > 0

        schema = InvestigationThreadInfo.table_schema()
        assert len(schema) > 0

        schema = RomanticBeatInfo.table_schema()
        assert len(schema) > 0

        schema = FearMomentInfo.table_schema()
        assert len(schema) > 0

        schema = SubjectFocusInfo.table_schema()
        assert len(schema) > 0

    def test_movie_data_models_serialization(self, tmp_path):
        """Test to_dict, to_json, from_dict, from_json for movie data models."""
        from aiss.models.movies._base import CastMemberInfo

        cast = CastMemberInfo(character="Hero", actor="John Doe", role="lead")

        # Test to_dict
        data = cast.to_dict()
        assert data["character"] == "Hero"
        assert data["actor"] == "John Doe"

        # Test from_dict
        cast2 = CastMemberInfo.from_dict(data)
        assert cast2.character == "Hero"

        # Test to_json
        json_path = tmp_path / "cast.json"
        cast.to_json(json_path)
        assert json_path.exists()

        # Test from_json
        cast3 = CastMemberInfo.from_json(json_path)
        assert cast3.character == "Hero"
        assert cast3.actor == "John Doe"

    def test_base_movie_info_serialization(self, tmp_path):
        """Test BaseMovieInfo to_dict, to_json, from_dict, from_json."""
        from aiss.models.movies.drama_model import DramaMovieInfo

        movie = DramaMovieInfo(
            title="Test Movie",
            tagline="A test tagline",
            synopsis="A test synopsis",
            release_year=2020,
            runtime_minutes=120,
        )

        # Test to_dict
        data = movie.to_dict()
        assert data["title"] == "Test Movie"
        assert data["release_year"] == 2020

        # Test from_dict
        movie2 = DramaMovieInfo.from_dict(data)
        assert movie2.title == "Test Movie"
        assert movie2.runtime_minutes == 120

        # Test to_json
        json_path = tmp_path / "movie.json"
        movie.to_json(json_path)
        assert json_path.exists()

        # Test from_json
        movie3 = DramaMovieInfo.from_json(json_path)
        assert movie3.title == "Test Movie"
        assert movie3.tagline == "A test tagline"

    def test_base_movie_info_render_with_cast(self, console):
        """Test BaseMovieInfo render with cast members."""
        from aiss.models.movies._base import CastMemberInfo
        from aiss.models.movies.drama_model import DramaMovieInfo

        movie = DramaMovieInfo(
            title="Test Movie",
            synopsis="A test synopsis",
            cast=[
                CastMemberInfo(character="Hero", actor="John Doe", role="lead"),
                CastMemberInfo(character="Villain", actor="Jane Smith", role="supporting"),
            ],
        )
        movie.render(console)
        output = console.export_text()
        assert "Test Movie" in output
        assert "Hero" in output or "John Doe" in output

    def test_base_movie_info_render_with_production_companies(self, console):
        """Test BaseMovieInfo render with production companies."""
        from aiss.models.movies._base import ProductionCompanyInfo
        from aiss.models.movies.drama_model import DramaMovieInfo

        movie = DramaMovieInfo(
            title="Test Movie",
            synopsis="A test synopsis",
            production_companies=[
                ProductionCompanyInfo(
                    name="Test Studios",
                    role="Production",
                    founded_year=2000,
                    headquarters="Hollywood",
                ),
            ],
        )
        movie.render(console)
        output = console.export_text()
        assert "Test Movie" in output

    def test_base_movie_info_render_with_box_office(self, console):
        """Test BaseMovieInfo render with box office info."""
        from aiss.models.movies._base import BoxOfficeInfo
        from aiss.models.movies.drama_model import DramaMovieInfo

        movie = DramaMovieInfo(
            title="Test Movie",
            synopsis="A test synopsis",
            box_office=BoxOfficeInfo(
                budget=50000000,
                gross_worldwide=150000000,
                gross_domestic=75000000,
            ),
        )
        movie.render(console)
        output = console.export_text()
        assert "Test Movie" in output


class TestGameFormatBase:
    """Test GameFormatBase functionality."""

    def test_game_format_base_class_variables(self):
        """Test GameFormatBase has required class variables."""
        assert hasattr(GameFormatBase, "summary_title_fallback")
        assert hasattr(GameFormatBase, "summary_attributes")

    def test_game_format_render_wikipedia_summary_empty(self, console):
        """Test render_wikipedia_summary with empty string."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test")
        instance.wikipedia_summary = ""
        instance.render_wikipedia_summary(console)
        output = console.export_text()
        assert output == "" or "Context" not in output

    def test_game_format_render_wikipedia_summary_with_content(self, console):
        """Test render_wikipedia_summary with content."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test")
        instance.wikipedia_summary = "Game context from Wikipedia."
        instance.render_wikipedia_summary(console)
        output = console.export_text()
        assert "Context" in output
        assert "Wikipedia" in output

    def test_game_format_summary_panel(self):
        """Test _summary_panel method."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test Game", game_summary="Test summary")
        title, lines, style = instance._summary_panel()
        assert title == "Test Game"
        assert len(lines) > 0
        assert isinstance(style, str)

    def test_game_format_fact_pairs(self):
        """Test _fact_pairs method."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test")
        facts = instance._fact_pairs()
        assert isinstance(facts, (list, tuple))

    def test_game_format_table_sections(self):
        """Test _table_sections method."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test")
        sections = instance._table_sections()
        assert isinstance(sections, (list, tuple))

    def test_game_format_extra_panels(self):
        """Test _extra_panels method."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test")
        panels = instance._extra_panels()
        assert isinstance(panels, (list, tuple))

    def test_game_format_summary_panel_no_attributes(self):
        """Test _summary_panel with no summary attributes."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test")
        title, lines, style = instance._summary_panel()
        assert title == "Test"
        assert len(lines) > 0

    def test_game_format_summary_panel_fallback_to_game_summary(self):
        """Test _summary_panel falls back to game_summary when attributes are empty."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        # Create instance with empty tagline but with game_summary
        instance = ActionAdventureGameInfo(title="Test", tagline="", game_summary="Fallback summary")
        title, lines, style = instance._summary_panel()
        assert "Fallback summary" in lines or "Fallback summary" in str(lines)

    def test_game_format_summary_panel_no_summary_at_all(self):
        """Test _summary_panel with no summary whatsoever."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Test", tagline="", game_summary="")
        title, lines, style = instance._summary_panel()
        assert "(no summary provided)" in lines or "(no summary provided)" in str(lines)

    def test_game_format_render_all_empty(self, console):
        """Test render when all content is empty."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(title="Minimal", tagline="", game_summary="")
        instance.render(console)
        output = console.export_text()
        assert "Minimal" in output
        assert "(no summary provided)" in output

    def test_game_format_render_with_fact_pairs(self, console):
        """Test render with fact pairs."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(
            title="Test Game",
            game_summary="Test summary",
            release_year=2020,
            platform="PC",
        )
        instance.render(console)
        output = console.export_text()
        assert "Test Game" in output

    def test_game_format_render_with_tables(self, console):
        """Test render with table sections."""
        from aiss.models.games._base import StudioProfile
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        instance = ActionAdventureGameInfo(
            title="Test Game",
            game_summary="Test summary",
            developers=[
                StudioProfile(
                    name="Test Studio",
                    role="Developer",
                    headquarters="Seattle",
                    team_size=100,
                    notable_credits=["Game 1"],
                    technology_stack=["Unity"],
                )
            ],
        )
        instance.render(console)
        output = console.export_text()
        assert "Test Game" in output

    def test_game_format_render_with_empty_panel_body(self, console):
        """Test _extra_panels with empty body (should be skipped)."""
        from aiss.models.games.action_adventure_model import ActionAdventureGameInfo

        # Set design_notes to empty to trigger skip logic
        instance = ActionAdventureGameInfo(title="Test", game_summary="Summary", design_notes="")
        instance.render(console)
        output = console.export_text()
        assert "Test" in output
        # Empty panels shouldn't appear

    def test_game_data_models_table_schema(self):
        """Test table_schema methods for game data models."""
        from aiss.models.games._base import (
            AccessibilityFeatureInfo,
            AudioDesignCue,
            GameplayMechanicHighlight,
            LiveServiceEventInfo,
            MultiplayerModeInfo,
            NarrativeBeatInfo,
            PlatformReleaseInfo,
            ProgressionTrackInfo,
            StudioProfile,
            TechnicalBenchmarkInfo,
        )

        # Test each model's table_schema method
        schema = StudioProfile.table_schema()
        assert len(schema) > 0
        assert any(s.name == "name" for s in schema)

        schema = PlatformReleaseInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "platform" for s in schema)

        schema = GameplayMechanicHighlight.table_schema()
        assert len(schema) > 0
        assert any(s.name == "mechanic" for s in schema)

        schema = MultiplayerModeInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "mode_name" for s in schema)

        schema = LiveServiceEventInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "event_name" for s in schema)

        schema = AccessibilityFeatureInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "feature" for s in schema)

        schema = TechnicalBenchmarkInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "scenario" for s in schema)

        schema = AudioDesignCue.table_schema()
        assert len(schema) > 0
        assert any(s.name == "cue_name" for s in schema)

        schema = ProgressionTrackInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "track_name" for s in schema)

        schema = NarrativeBeatInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "beat_name" for s in schema)

    def test_game_additional_data_models_table_schema(self):
        """Test table_schema for additional game data models."""
        from aiss.models.games._base import (
            EconomyLoopInfo,
            EconomyModelInfo,
            EsportsEventInfo,
            SessionProfileInfo,
        )

        schema = EconomyModelInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "currency" for s in schema)

        schema = EconomyLoopInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "loop_name" for s in schema)

        schema = EsportsEventInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "event_name" for s in schema)

        schema = SessionProfileInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "activity" for s in schema)

        # Test SocialFeatureInfo
        from aiss.models.games._base import SocialFeatureInfo

        schema = SocialFeatureInfo.table_schema()
        assert len(schema) > 0
        assert any(s.name == "feature_name" for s in schema)

    def test_game_json_model_serialization(self, tmp_path):
        """Test GameJsonModel to_dict, to_json, from_dict, from_json."""
        from aiss.models.games._base import StudioProfile

        studio = StudioProfile(
            name="Test Studio",
            role="Developer",
            headquarters="Seattle",
            team_size=100,
            notable_credits=["Game 1", "Game 2"],
            technology_stack=["Unity", "C#"],
        )

        # Test to_dict
        data = studio.to_dict()
        assert data["name"] == "Test Studio"
        assert data["team_size"] == 100

        # Test from_dict
        studio2 = StudioProfile.from_dict(data)
        assert studio2.name == "Test Studio"
        assert studio2.team_size == 100

        # Test to_json
        json_path = tmp_path / "studio.json"
        studio.to_json(json_path)
        assert json_path.exists()

        # Test from_json
        studio3 = StudioProfile.from_json(json_path)
        assert studio3.name == "Test Studio"
        assert studio3.headquarters == "Seattle"
