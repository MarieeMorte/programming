import time
from functools import wraps


def retry(attempts, delay, exceptions=None):
    """
    Декоратор для повторного вызова функции при возникновении исключений.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if exceptions is not None:
                        exc_types = exceptions if isinstance(exceptions, tuple) else (exceptions,)
                        if not any(isinstance(e, exc_type) for exc_type in exc_types):
                            raise
                    if attempt == attempts:
                        raise
                    time.sleep(delay)
            raise RuntimeError("Unreachable")

        return wrapper

    return decorator
