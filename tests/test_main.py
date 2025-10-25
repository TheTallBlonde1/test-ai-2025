import unittest
from unittest.mock import Mock

from rich.console import Console

from aiss.models.show_model import CharInfoInfo, ShowInfo
from main import run_show_queries


class FakeResponse:
    def __init__(self, parsed):
        self.output_parsed = parsed


class TestRunQueries(unittest.TestCase):
    def test_run_queries_offline(self):
        # Build a fake ShowInfo
        fake_char = CharInfoInfo(
            character="Test Character",
            actor="Actor Name",
            relationship="Friend",
            description="A brave test character",
            year_joined=2001,
        )

        fake_show = ShowInfo(
            characters=[fake_char],
            show_summary="This is a summary for testing.",
            production_companies=[],
            broadcast_info=[],
        )

        # Mock client so responses.parse returns our fake response
        fake_client = Mock()
        fake_client.responses.parse.return_value = FakeResponse(fake_show)

        console = Console(record=True)

        # Run the queries with our fake client
        run_show_queries(["Test Show"], fake_client, console)

        output = console.export_text()
        # Basic assertions that the rendered output contains expected strings
        self.assertIn("Test Show", output)
        self.assertIn("This is a summary for testing.", output)
        self.assertIn("Test Character", output)


if __name__ == "__main__":
    unittest.main()
