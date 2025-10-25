import argparse

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

from aiss import show_information_json, show_information_parsed, show_information_text

load_dotenv()


def run_show_queries(show: str | None, client: OpenAI, console: Console, mode: str = "parsed"):
    if not mode:
        mode = "parsed"
    if mode not in ("parsed", "json", "text"):
        console.print(f"[bold red]Error:[/bold red] Unknown mode '{mode}'. Choose from 'parsed', 'json', or 'text'.")
        return

    if mode == "parsed":
        console.print("[bold green]Running Parsed Show Information Queries[/bold green]")

        test_shows = [
            "Peppa Pig",
            "SpongeBob SquarePants",
            "Avatar: The Last Airbender",
        ]
        shows = [show] if show else test_shows
        show_information_parsed(shows, client, console)

    elif mode == "json":
        console.print("[bold green]Running JSON Show Information Queries[/bold green]")
        test_shows = [
            "The Office",
            "Friends",
            "Breaking Bad",
        ]
        shows = [show] if show else test_shows
        show_information_json(shows, client, console)

    elif mode == "text":
        console.print("[bold green]Running Text Show Information Queries[/bold green]")
        test_shows = [
            "Game of Thrones",
            "Stranger Things",
            "The Crown",
        ]
        shows = [show] if show else test_shows
        show_information_text(shows, client, console)


def main(show: str | None = None, mode: str = "parsed"):
    client: OpenAI = OpenAI()
    console = Console()
    run_show_queries(show, client, console, mode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query show info via OpenAI responses.parse and print pretty output")
    parser.add_argument(
        "--show",
        "-s",
        help="Single show name to query (if omitted, runs the test list)",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["parsed", "json", "text"],
        default="parsed",
        help="Mode of querying show information",
    )
    args = parser.parse_args()

    show = args.show if args.show else None

    main(show, args.mode)
