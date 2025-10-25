from aiss.models.movie_model import MovieInfo
from aiss.models.show_model import ShowInfo


def test_models_expose_protocol_methods():
    """Ensure ShowInfo and MovieInfo expose the class methods required by the
    ModelFormatProtocol: get_instructions, get_user_prompt, json_format_instructions.
    """
    for cls in (ShowInfo, MovieInfo):
        # class-level methods should exist and be callable
        assert hasattr(cls, "get_instructions") and callable(getattr(cls, "get_instructions"))
        assert hasattr(cls, "get_user_prompt") and callable(getattr(cls, "get_user_prompt"))
        assert hasattr(cls, "json_format_instructions") and callable(getattr(cls, "json_format_instructions"))

        # calling them should return strings
        assert isinstance(cls.get_instructions(), str)
        assert isinstance(cls.get_user_prompt("X"), str)
        assert isinstance(cls.json_format_instructions(), str)
