import json
import re
from typing import TYPE_CHECKING, Type, TypeVar

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console

# Panel is not required in this helper (rendering delegated to utils)
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from aiss.models.movie_model import MovieInfo
from aiss.models.protocols import ModelFormatProtocol
from aiss.models.show_model import ShowInfo
from aiss.utils import render_from_json

if TYPE_CHECKING:
    from openai.types.responses.response import Response

load_dotenv()

# generic type variable for parsed response model
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def _extract_text_from_response(response) -> str:
    # Safely extract plain text from common SDK response shapes.
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    try:
        parts = []
        for item in getattr(response, "output", []) or []:
            content = item.get("content") if isinstance(item, dict) else None
            if content:
                for c in content:
                    if isinstance(c, dict):
                        t = c.get("text") or c.get("content")
                        if t:
                            parts.append(t)
                    elif isinstance(c, str):
                        parts.append(c)
        return "\n".join(parts)
    except Exception:
        return ""


def get_json_response(items: list[str], client: OpenAI, console: Console, local_model: str = "show", text_format: Type[T] | None = None):
    """

    Query the model and return a JSON representation of the show info.

    :param items: List of show names to query
    :type items: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console
    :param local_model: Local model name for progress display
    :type local_model: str

    """
    if text_format is None:
        text_format = ShowInfo
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"Querying {local_model}", total=len(items))

        for item_name in items:
            # Use the completions endpoint to get raw text back
            response: Response = client.responses.create(
                model="gpt-5-mini",
                input=[
                    {"role": "system", "content": text_format.json_format_instructions()},
                    {"role": "user", "content": text_format.get_user_prompt(item_name)},
                ],
                timeout=Timeout(4000, connect=6.0),
            )

            raw = _extract_text_from_response(response)

            data = None
            if raw:
                try:
                    data = json.loads(raw)
                except Exception:
                    m = re.search(r"(\{(?:.|\n)*\}|\[(?:.|\n)*\])", raw)
                    if m:
                        try:
                            data = json.loads(m.group(1))
                        except Exception:
                            data = None

            if data is None:
                console.print(f"[red]Failed to parse JSON output for '{item_name}'[/red]")
                progress.update(task, advance=1)
                continue

            console.rule(f"[bold cyan]{item_name}")
            try:
                render_from_json(data, console)
            except Exception as exc:
                console.print(f"[red]Rendering JSON failed: {exc}[/red]")

            console.print("\n")
            progress.update(task, advance=1)


def show_information_json(shows: list[str], client: OpenAI, console: Console):
    """Query the model and return a JSON representation of the show info.

    This intentionally does NOT use the Pydantic `ShowInfo` model; it asks the
    model to emit JSON and then parses/render that JSON via
    `aiss.utils.render_from_json`.

    :param shows: List of show names to query
    :type shows: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console
    """
    get_json_response(shows, client, console, local_model="shows", text_format=ShowInfo)


def movie_information_json(movies: list[str], client: OpenAI, console: Console):
    """Query the model and return a JSON representation of the movie info.

    This intentionally does NOT use the Pydantic `MovieInfo` model; it asks the
    model to emit JSON and then parses/render that JSON via
    `aiss.utils.render_from_json`.

    :param movies: List of movie names to query
    :type movies: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console
    """
    get_json_response(movies, client, console, local_model="movies", text_format=MovieInfo)
