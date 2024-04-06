import functools
from typing import Callable, TypeVar, ParamSpec, Coroutine, Any

from sqlalchemy.exc import SQLAlchemyError

from swapmaster.core.utils.exceptions import GatewayError

Params = ParamSpec("Params")
TReturn = TypeVar("TReturn")


def exception_mapper(
        func: Callable[Params, Coroutine[Any, Any, TReturn]]
) -> Callable[Params, Coroutine[Any, Any, TReturn]]:
    """Application layer won't know about sqlalchemy errors"""
    @functools.wraps(func)
    def wrapped_func(*args: Params.args, **kwargs: Params.kwargs) -> TReturn:
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as error:
            raise GatewayError from error
    return wrapped_func
