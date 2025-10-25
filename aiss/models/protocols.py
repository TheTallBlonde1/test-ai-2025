from typing import Protocol


class ModelFormatProtocol(Protocol):
    """Protocol describing the minimal 'text format' API used by the
    various helper modules (openai_json/openai_parsed/etc).

    Implementations are expected to be classes (typically Pydantic models)
    with class/staticmethods that provide instruction text and user prompts.
    """

    @classmethod
    def get_instructions(cls) -> str:  # pragma: no cover - trivial
        ...

    @classmethod
    def get_user_prompt(cls, name: str) -> str:  # pragma: no cover - trivial
        ...

    @classmethod
    def json_format_instructions(cls) -> str:  # pragma: no cover - trivial
        ...
