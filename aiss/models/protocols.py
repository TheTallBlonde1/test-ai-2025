"""Model format protocol

Provides a lightweight Protocol that describes the three class-level
methods our helpers expect from a "text format" class (for example
`DramaShowInfo` or a movie format). We keep this as a Protocol so static type
checkers (mypy/pyright) can verify structural compatibility without
requiring runtime inheritance.

"""

from pathlib import Path
from typing import Protocol, Sequence

from rich.console import Console


# MARK: ModelFormat Protocol
class ModelFormatProtocol(Protocol):
    """Protocol describing the minimal 'text format' API used by the
    various helper modules (openai_json/openai_parsed/etc).

    Implementations are expected to be classes (typically Pydantic models)
    with class/staticmethods that provide instruction text and user prompts.
    """

    # Class-level metadata required on formats (use simple str annotations
    # so static checkers can verify presence without importing typing.ClassVar
    model_name: str
    description: str
    key_trait: str

    @classmethod
    def get_instructions(cls, additional_info: Sequence[str] | None = None) -> str:  # pragma: no cover - trivial
        """
        Supply long-form instructions for the LLM describing the task.

        :return: Instruction text passed to the model
        :rtype: str
        """

    @classmethod
    def get_user_prompt(cls, name: str) -> str:  # pragma: no cover - trivial
        """
        Build a user-facing prompt for a specific entity name (show/movie).

        :param name: Name of the entity (show or movie)
        :type name: str

        :return: User prompt string
        :rtype: str
        """

    @classmethod
    def json_format_instructions(cls) -> str:  # pragma: no cover - trivial
        """
        Return an instruction string that tells the model to output JSON
        matching the expected schema for the format.

        :return: JSON format instruction text
        :rtype: str
        """

    def to_dict(self) -> dict:  # pragma: no cover - trivial
        """
        Serialize this model/format instance to a plain dict suitable for
        JSON transport or storage.

        :return: Mapping of primitive values
        :rtype: dict
        """

    def to_json(self, json_file_path: Path | str) -> None:  # pragma: no cover - trivial
        """
        Persist this model/format instance to a JSON file.

        :param json_file_path: Destination path for JSON
        :type json_file_path: str | Path

        :return: None
        :rtype: None
        """

    @classmethod
    def from_dict(cls, data: dict) -> "ModelFormatProtocol":  # pragma: no cover - trivial
        """
        Reconstruct a model/format instance from a plain mapping.

        :param data: Mapping containing the model fields
        :type data: dict

        :return: New instance implementing ModelFormatProtocol
        :rtype: ModelFormatProtocol
        """

    @classmethod
    def from_json(cls, json_file_path: Path | str) -> "ModelFormatProtocol":  # pragma: no cover - trivial
        """
        Load a model/format instance from a JSON file on disk.

        :param json_file_path: Path to JSON file
        :type json_file_path: str | Path

        :return: New instance implementing ModelFormatProtocol
        :rtype: ModelFormatProtocol
        """

    def render(self, console: Console) -> None:  # pragma: no cover - trivial
        """
        Render a readable representation of the model to the provided
        Rich Console instance.

        :param console: Rich Console to render output to
        :type console: Console

        :return: None
        :rtype: None
        """

    # to_dict / to_json / from_dict / from_json / render
