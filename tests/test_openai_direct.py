import json
from unittest.mock import Mock

from aiss.openai_direct.openai_json import show_information_json
from aiss.openai_direct.openai_parsed import show_information_parsed
from aiss.openai_direct.openai_text import show_information_text


def test_show_information_parsed_returns_renderable(sample_show, console, fake_client_factory):
    client = fake_client_factory(sample_show)
    # use a single show name
    show_information_parsed(["Test Show"], client, console)
    out = console.export_text()
    assert "Summary here" in out
    assert "Test Character" in out


def test_show_information_text_renders_plain_text(console):
    client = Mock()
    client.responses = Mock()
    client.responses.create.return_value = Mock(output_text="Plain summary text for the show")
    show_information_text(["Any Show"], client, console)
    out = console.export_text()
    assert "Plain summary text for the show" in out


def test_show_information_json_parses_and_renders(console):
    client = Mock()
    client.responses = Mock()
    data = {
        "show_summary": "JSON summary",
        "characters": [{"character": "C1", "actor": "A1", "relationship": "Friend", "description": "Desc", "year_joined": 2010}],
        "broadcast_info": [{"network": "Net", "country": "US", "start_year": 2010, "end_year": 2015}],
        "production_companies": [{"name": "Studio", "founded_year": 1990, "start_year": 2000, "end_year": 2005, "country": "USA"}],
    }
    # return a text payload with JSON
    client.responses.create.return_value = Mock(output_text=json.dumps(data))
    show_information_json(["Any Show"], client, console)
    out = console.export_text()
    assert "JSON summary" in out
    assert "C1" in out
    assert "Studio" in out
