"""Additional tests for model rendering and JSON deserialization."""

import json

from aiss.utils import render_from_json


def test_drama_show_render_output(sample_show, console):
    """
    Test drama show rendering includes key content.

    :param sample_show: Fixture providing a sample DramaShowInfo instance
    :type sample_show: DramaShowInfo

    :param console: Fixture providing a Rich Console for rendering
    :type console: Console
    """
    sample_show.render(console)
    out = console.export_text()
    assert "Summary here" in out
    assert "Test Character" in out
    assert "Studio" in out


def test_drama_movie_render_output(sample_movie, console):
    """
    Test drama movie rendering includes key content.

    :param sample_movie: Fixture providing a sample DramaMovieInfo instance
    :type sample_movie: DramaMovieInfo

    :param console: Fixture providing a Rich Console for rendering
    :type console: Console
    """
    sample_movie.render(console)
    out = console.export_text()
    assert "Example" in out
    assert "Lead" in out
    assert "BigStudio" in out


def test_render_from_json_basic(console):
    """
    Test rendering show data from JSON string.

    Verifies that render_from_json can parse JSON and render it correctly,
    including nested structures like characters, broadcast info, and
    production companies.

    :param console: Fixture providing a Rich Console for rendering
    :type console: Console
    """
    data = {
        "show_summary": "JSON summary",
        "characters": [{"character": "C1", "actor": "A1", "relationship": "Friend", "description": "Desc", "year_joined": 2010}],
        "broadcast_info": [{"network": "Net", "country": "US", "start_year": 2010, "end_year": 2015}],
        "production_companies": [{"name": "Studio", "founded_year": 1990, "start_year": 2000, "end_year": 2005, "country": "USA"}],
    }
    render_from_json(json.dumps(data), console)
    out = console.export_text()
    assert "JSON summary" in out
    assert "C1" in out
    assert "Studio" in out
