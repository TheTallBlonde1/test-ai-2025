"""Determine which registered format best matches the input text.

This helper queries the OpenAI responses.parse endpoint using the
`FindModelRequest` Pydantic model and returns the matching format class
(one of the movie formats or genre-specific `*ShowInfo` formats) for
downstream parsing/rendering.
"""

from typing import TYPE_CHECKING, Optional

from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console

# Progress UI is managed by the caller (run_queries); no progress imports here.
from aiss.claude_direct._common import MAX_TOKENS, check_refusal, get_model_name
from aiss.models import FindModelRequest, ModelType, ModelTypeInput

if TYPE_CHECKING:
    from openai.types.responses.parsed_response import ParsedResponse

load_dotenv()


# MARK: Model Finder
def find_model_from_input(
    input_text: str,
    client: OpenAI,
    console: Console,
) -> ModelTypeInput:
    """

    Query the model and return a JSON representation of the show info.

    :param input_text: Input text to analyze for model type
    :type input_text: str
    :param client: OpenAI client instance
    :type client: OpenAI
    :param console: Rich Console to render output to
    :type console: Console

    :return : The determined model type class
    :rtype : ModelType

    """

    options, instructions = _classification_prompt()

    response: ParsedResponse[FindModelRequest] = client.responses.parse(
        model="gpt-5-mini",
        input=f"Find whether the following text is about a {options}:\n\n`{input_text}`",
        instructions=instructions,
        text_format=FindModelRequest,
        timeout=Timeout(4000, connect=6.0),
    )

    find_model_response: FindModelRequest = response.output_parsed
    if find_model_response is None:
        console.print("[red]Failed to parse model type from input[/red]")
        return

    return _to_model_type_input(find_model_response, console)


# MARK: Claude Model Finder
def find_model_from_input_claude(
    input_text: str,
    client: Anthropic,
    console: Console,
) -> Optional[ModelTypeInput]:
    """
    Classify the input text using Claude's messages.parse (structured outputs).

    :param input_text: Input text to analyze for model type
    :type input_text: str
    :param client: Anthropic client instance
    :type client: Anthropic
    :param console: Rich Console to render output to
    :type console: Console

    :return: The determined model type input, or None on failure
    :rtype: Optional[ModelTypeInput]
    """

    options, instructions = _classification_prompt()

    response = client.messages.parse(
        model=get_model_name(),
        max_tokens=MAX_TOKENS,
        system=instructions,
        messages=[{"role": "user", "content": f"Find whether the following text is about a {options}:\n\n`{input_text}`"}],
        output_format=FindModelRequest,
    )

    if check_refusal(response, console, input_text):
        return None

    find_model_response: Optional[FindModelRequest] = getattr(response, "parsed_output", None)
    if find_model_response is None:
        console.print("[red]Failed to parse model type from input[/red]")
        return None

    return _to_model_type_input(find_model_response, console)


def _classification_prompt() -> tuple[str, str]:
    options = ModelType.formatted_options()
    instructions = f"""You are an expert at classifying entertainment descriptions.
        Select the most appropriate format from {options} and respond using the FindModelRequest schema.
        {ModelType.instruction_listing()}"""
    return options, instructions


def _to_model_type_input(find_model_response: FindModelRequest, console: Console) -> ModelTypeInput:
    console.rule(f"[bold cyan]Model Type: {find_model_response.find_model}")
    console.print("\n")

    return ModelTypeInput(
        model_type=ModelType(find_model_response.find_model),
        description=find_model_response.description,
        formatted_name=find_model_response.formatted_name,
        additional_info=find_model_response.additional_info,
    )
