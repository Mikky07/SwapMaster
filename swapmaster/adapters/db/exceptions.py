import functools
from typing import Callable, TypeVar, ParamSpec

from sqlalchemy.exc import SQLAlchemyError

from swapmaster.core.utils.exceptions import GatewayError

Params = ParamSpec("Params")
ReturnValue = TypeVar("ReturnValue")


def exception_mapper(func: Callable[Params, ReturnValue]):
    """Application layer won't know about sqlalchemy errors"""
    @functools.wraps
    def wrapped_func(*args: Params.args, **kwargs: Params.kwargs):
        try:
            func(*args, **kwargs)
        except SQLAlchemyError as error:
            raise GatewayError from error
    return wrapped_func
