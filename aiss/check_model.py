"""Determine which registered format best matches the input text.

This helper queries the OpenAI responses.parse endpoint using the
`FindModelRequest` Pydantic model and returns the matching format class
(one of the movie formats or genre-specific `*ShowInfo` formats) for
downstream parsing/rendering.
"""

from typing import TYPE_CHECKING

from dotenv import load_dotenv
from openai import OpenAI, Timeout
from rich.console import Console

# Progress UI is managed by the caller (run_queries); no progress imports here.
from aiss.models import FindModelRequest, ModelType, ModelTypeResult

if TYPE_CHECKING:
    from openai.types.responses.parsed_response import ParsedResponse

load_dotenv()


# MARK: Model Finder
def find_model_from_input(
    input_text: str,
    client: OpenAI,
    console: Console,
) -> ModelTypeResult:
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

    options = ModelType.formatted_options()
    instructions = f"""You are an expert at classifying entertainment descriptions. 
        Select the most appropriate format from {options} and respond using the FindModelRequest schema.
        {ModelType.instruction_listing()}"""

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

    console.rule(f"[bold cyan]Model Type: {find_model_response.find_model}")
    console.print("\n")

    return ModelTypeResult(
        model_type=ModelType(find_model_response.find_model),
        description=find_model_response.description,
        formatted_name=find_model_response.formatted_name,
        additional_info=find_model_response.additional_info,
    )
