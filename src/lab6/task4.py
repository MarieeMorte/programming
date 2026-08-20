"""
Модуль с декоратором call_limiter для ограничения числа вызовов методов класса.
"""

import types
from functools import wraps

SKIP_MAGIC = {
    "__getattribute__",
    "__setattr__",
    "__delattr__",
    "__getattr__",
    "__setitem__",
    "__delitem__",
    "__get__",
    "__set__",
    "__delete__",
}


def call_limiter(limit):
    """
    Декоратор класса, ограничивающий количество вызовов каждого метода.
    """
    if limit < 0:
        raise ValueError("limit must be non-negative")

    def decorator(cls):
        class_id = id(cls)

        for attr_name, attr_value in list(cls.__dict__.items()):
            if attr_name in SKIP_MAGIC:
                continue

            if isinstance(attr_value, types.FunctionType):
                wrapped = _limit_method(attr_value, limit, instance_based=True, class_id=None)
                setattr(cls, attr_name, wrapped)

            elif isinstance(attr_value, staticmethod):
                original_func = attr_value.__func__
                wrapped = _limit_method(original_func, limit, instance_based=False, class_id=class_id)
                setattr(cls, attr_name, staticmethod(wrapped))

            elif isinstance(attr_value, classmethod):
                original_func = attr_value.__func__
                wrapped = _limit_method(original_func, limit, instance_based=False, class_id=class_id)
                # noinspection PyTypeChecker
                setattr(cls, attr_name, classmethod(wrapped))

        return cls

    return decorator


def _limit_method(func, limit, instance_based, class_id):
    """
    Вспомогательная функция для обёртки отдельного метода с подсчётом вызовов.
    """
    counters = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        if instance_based:
            if not args:
                raise RuntimeError("Instance method called without self")
            key = id(args[0])
        else:
            if args and hasattr(args[0], "__class__"):
                if isinstance(args[0], type):
                    key = id(args[0])
                else:
                    key = class_id
            else:
                key = class_id

        current = counters.get(key, 0)
        if current >= limit:
            raise RuntimeError(f"Call limit ({limit}) exceeded for method {func.__name__}")

        counters[key] = current + 1
        return func(*args, **kwargs)

    return wrapper
