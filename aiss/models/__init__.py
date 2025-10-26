"""Aggregated exports for film, television, and game models."""

from .find_model import FindModelRequest
from .games import *  # noqa: F401,F403
from .games import __all__ as _games_all
from .movies import *  # noqa: F401,F403
from .movies import __all__ as _movies_all
from .shared import ModelType, ModelTypeResult, ResultType, TableSchema
from .shows import *  # noqa: F401,F403
from .shows import __all__ as _shows_all

__all__ = (
    list(_movies_all)
    + list(_shows_all)
    + list(_games_all)
    + [
        "ResultType",
        "ModelType",
        "ModelTypeResult",
        "FindModelRequest",
        "TableSchema",
    ]
)
