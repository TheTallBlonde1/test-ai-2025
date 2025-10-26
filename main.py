"""Command-line entrypoint and convenience runner for demo queries.

This module provides a tiny CLI used during development to exercise the
OpenAI helpers. It is intentionally minimal and demonstrates how to call
the parsed/json/text helper flows.
"""

import argparse

from aiss import ResultType, run_the_query

__all__ = ["main"]


# MARK: Main
def main(input_text: str | None = None, mode: ResultType | str | None = ResultType.PARSED) -> None:
    """
    Small main function used by the CLI to initialize the client and console.

    :param input_text: Input text to run (default: None)
    :type input_text: str

    :param mode: Mode to run ('parsed' | 'json' | 'text')
    :type mode: ResultType | str | None

    :return: None
    :rtype: None
    """

    run_the_query(input_text, mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query show info via OpenAI responses.parse and print pretty output")

    parser.add_argument("input_text", nargs="?", help="First (default) input to query (positional)", default="Match of the Day shown on Saturdays on BBC One in the UK")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["parsed", "json", "text"],
        default="parsed",
        help="Mode of querying show information",
    )
    args = parser.parse_args()
    main(args.input_text, ResultType(args.mode))
