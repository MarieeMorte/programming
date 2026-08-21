"""Модуль с декоратором retry для повторных вызовов функций при ошибках."""

import time
from functools import wraps


def retry(attempts, delay, exceptions: list = None):
    """Декоратор для повторного вызова функции при возникновении исключений."""

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return function(*args, **kwargs)
                except Exception as exception:  # pylint: disable=broad-except
                    if exceptions is not None:
                        if not any(
                            isinstance(exception, exception_type) for exception_type in exceptions
                        ):
                            raise
                    if attempt == attempts:
                        raise
                    time.sleep(delay)
            raise RuntimeError("Unreachable")

        return wrapper

    return decorator
