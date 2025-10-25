from typing import TYPE_CHECKING, Type, TypeVar

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console
from rich.panel import Panel
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

if TYPE_CHECKING:
    from openai.types.responses.response import Response


load_dotenv()

# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_text_response(
    items: list[str],
    client: OpenAI,
    console: Console,
    local_model: str = "show",
    text_format: Type[T] | None = None,
):
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
                instructions=text_format.get_instructions(),
                input=text_format.get_user_prompt(item_name),
                timeout=Timeout(4000, connect=6.0),
            )

            # render output
            console.rule(f"[bold cyan]{item_name}")

            json_text = response.output_text
            console.print(Panel(json_text, title="Show Information (JSON)", expand=False, style="green"))

            progress.update(task, advance=1)


def show_information_text(shows: list[str], client: OpenAI, console: Console):
    """Query the model and return a text representation of the show info.

    This uses the Pydantic `ShowInfo` model to parse the response and
    render it via the model's `render` method.

    :param shows: List of show names to query
    :type shows: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console

    """
    get_text_response(shows, client, console, local_model="shows", text_format=ShowInfo)


def movie_information_text(movies: list[str], client: OpenAI, console: Console):
    """Query the model and return a text representation of the movie info.

    This uses the Pydantic `ShowInfo` model to parse the response and
    render it via the model's `render` method.

    :param movies: List of movie names to query
    :type movies: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console

    """
    get_text_response(movies, client, console, local_model="movies", text_format=MovieInfo)
