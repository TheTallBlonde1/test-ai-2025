"""Tests for protocol contract compliance across all model types."""

from aiss.models.shared import ModelType


def test_models_expose_protocol_methods():
    """
    Ensure every registered model exposes the expected Protocol methods.

    Verifies that all model types registered in ModelType enum implement
    the required protocol methods (get_instructions, get_user_prompt,
    json_format_instructions) and that these methods return strings.
    """
    registered_classes = {model_type.get_model_from_name() for model_type in ModelType}

    for cls in registered_classes:
        # class-level methods should exist and be callable
        assert hasattr(cls, "get_instructions") and callable(getattr(cls, "get_instructions"))
        assert hasattr(cls, "get_user_prompt") and callable(getattr(cls, "get_user_prompt"))
        assert hasattr(cls, "json_format_instructions") and callable(getattr(cls, "json_format_instructions"))

        # calling them should return strings
        assert isinstance(cls.get_instructions(), str)
        assert isinstance(cls.get_user_prompt("X"), str)
        assert isinstance(cls.json_format_instructions(), str)
