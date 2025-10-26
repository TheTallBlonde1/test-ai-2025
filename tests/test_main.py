"""Tests for main module entry point."""

import unittest


class FakeResponse:
    """
    Mock response object for testing.

    :param parsed: The parsed output data
    :type parsed: Any
    """

    def __init__(self, parsed):
        """
        Initialize fake response with parsed data.

        :param parsed: The parsed output to store
        :type parsed: Any
        """
        self.output_parsed = parsed


if __name__ == "__main__":
    unittest.main()
