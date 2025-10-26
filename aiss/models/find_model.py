"""Small Pydantic model used to classify input into a registered format.

This module contains the `FindModelRequest` model used by the
`aiss.find_model` helper to instruct the LLM to return one of the
available `ModelType` values (show, movie, drama, comedy, etc.).
"""

from pydantic import BaseModel, Field

from .shared import ModelType


# MARK: FindModelRequest
class FindModelRequest(BaseModel):
    """
    Pydantic request model that captures the LLM's classification result.

    :param find_model: One of the values enumerated in :class:`ModelType`
    :type find_model: str
    """

    find_model: str = Field(
        ModelType.SHOW.value,
        description="The type of model to find. Valid options: " + ", ".join(f"'{model.value}'" for model in ModelType) + ".",
    )
    formatted_name: str = Field("", description="The name of the show, movie or game found formatted in the correct way as it was branded by the studio.")
    description: str = Field(
        "",
        description="A brief description of why this model was chosen based on the input text (less than 30 characters).",
    )
    additional_info: list[str] = Field(
        default_factory=list,
        description="Any additional information about the found model that may be useful to identify it from the input text or found about it.",
    )
