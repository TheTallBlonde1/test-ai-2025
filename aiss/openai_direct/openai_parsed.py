from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console
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
    from openai.types.responses.parsed_response import ParsedResponse


load_dotenv()

# generic type variable for parsed response model
# generic type variable for parsed response model bound to the ModelFormatProtocol
T = TypeVar("T", bound=ModelFormatProtocol)


def get_parsed_response(
    items: List[str],
    client: OpenAI,
    console: Console,
    local_model: str = "show",
    text_format: Type[T] | None = None,
) -> None:
    """

    Query the model and return a parsed ShowInfo representation.

    :param items: List of show names to query
    :type items: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console
    :param local_model: Local model name for progress display
    :type local_model: str

    """
    # default to ShowInfo when no explicit text_format is provided
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
            # Use the responses.parse endpoint to get structured ShowInfo back
            response: ParsedResponse[T] = client.responses.parse(
                model="gpt-5-mini",
                instructions=text_format.get_instructions(),
                input=text_format.get_user_prompt(item_name),
                text_format=text_format,
                timeout=Timeout(4000, connect=6.0),
            )
            item_info: Optional[T] = getattr(response, "output_parsed", None)
            if item_info is None:
                console.print(f"[red]Failed to parse info for '{item_name}'[/red]")
                progress.update(task, advance=1)
                continue

            # render output (delegate to model's render method)
            console.rule(f"[bold cyan]{item_name}")
            item_info.render(console)
            console.print("\n")
            progress.update(task, advance=1)


def movie_information_parsed(movies: List[str], client: OpenAI, console: Console):
    """

    Query the model and return a parsed MovieInfo representation.

    :param movies: List of movie names to query
    :type movies: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console

    """
    get_parsed_response(movies, client, console, local_model="movies", text_format=MovieInfo)


def show_information_parsed(shows: List[str], client: OpenAI, console: Console):
    """

    Query the model and return a parsed ShowInfo representation.

    :param shows: List of show names to query
    :type shows: list[str]
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console

    """
    get_parsed_response(shows, client, console, local_model="shows", text_format=ShowInfo)
