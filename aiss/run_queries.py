from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

from .check_model import find_model_from_input
from .models.shared import ResultType
from .openai_direct import get_json_response, get_parsed_response, get_text_response
from .pydantic_ai.pydantic_ai_agents import run_agents_parsed

load_dotenv()


# MARK: Runner
def run_the_query(
    input_text: str,
    result_type: ResultType | str | None = ResultType.PARSED,
    api: str | None = "openai",
):
    """
    Run the chosen query mode against a set of test shows (or a single show).

    :param input_text: Name of the show to query
    :type input_text: str

    :param result_type: One of 'parsed', 'json', or 'text' to select the helper flow
    :type result_type: ResultType | str | None

    :return: None
    :rtype: None
    """
    console = Console()

    input_text = input_text.strip()
    input_text = input_text if input_text else None
    if input_text is None:
        console.print("[bold red]Error:[/bold red] Input text must be provided")
        return

    # Normalize backend selection
    api = (api or "openai").strip().lower()
    is_pydantic = api in {"pydantic", "pydantic ai", "pydantic_ai", "pydantic-ai"}

    # Delegate progress handling to sub-functions
    if is_pydantic:
        run_agents_parsed(input_text, console)
        return

    if not result_type:
        result_type = ResultType.PARSED
    if isinstance(result_type, str):
        result_type = ResultType(result_type.lower())
    if result_type not in (ResultType.PARSED, ResultType.JSON, ResultType.TEXT):
        console.print(f"[bold red]Error:[/bold red] Unknown mode '{result_type}'. Choose from 'parsed', 'json', or 'text'.")
        return

    client = OpenAI()
    model_type_result = find_model_from_input(input_text, client, console)
    if model_type_result is None:
        console.print(f"[red]Failed to determine model type for input '{input_text}'[/red]")
        return
    if result_type == ResultType.PARSED:
        get_parsed_response(model_type_result, client, console)
    elif result_type == ResultType.JSON:
        get_json_response(model_type_result, client, console)
    elif result_type == ResultType.TEXT:
        get_text_response(model_type_result, client, console)
