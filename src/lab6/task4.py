"""Модуль с декоратором call_limiter для ограничения числа вызовов методов класса."""

import types
from functools import wraps


def call_limiter(limit: int):
    """Декоратор класса, ограничивающий количество вызовов каждого метода."""
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer!")

    def make_wrapper(method, method_name):
        """Создаёт обёртку, которая считает вызовы метода для каждого экземпляра."""

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # pylint: disable=protected-access
            if not hasattr(self, "_call_limiter_counts"):
                self._call_limiter_counts = {}

            counts = self._call_limiter_counts
            current = counts.get(method_name, 0)
            # pylint: disable=protected-access

            if current >= limit:
                raise RuntimeError(f"Method '{method_name}' exceeded call limit of {limit}")

            counts[method_name] = current + 1
            return method(self, *args, **kwargs)

        return wrapper

    def decorator(target_class):
        for attr_name, attr_value in list(target_class.__dict__.items()):
            if isinstance(attr_value, types.FunctionType):
                wrapped = make_wrapper(attr_value, attr_name)
                setattr(target_class, attr_name, wrapped)
        return target_class

    return decorator
