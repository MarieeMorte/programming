"""Модуль с декоратором logger для логирования методов класса."""

import time
from functools import wraps


def logger(show_magic_methods=True):
    """Декоратор класса для логирования вызовов всех его методов."""

    def make_wrapper(method, method_name, class_name):
        """Создаёт обёртку для одного метода с логированием."""

        @wraps(method)
        def wrapper(*args, **kwargs):
            print(f"Вызов метода: {class_name}.{method_name}")
            print(f"Аргументы: args={args}, kwargs={kwargs}")

            start = time.perf_counter()
            result = method(*args, **kwargs)
            end = time.perf_counter()

            print(f"Время выполнения: {end - start} сек.")
            print(f"Результат: {result}")
            return result

        return wrapper

    def decorator(target_class):
        for attribute_name, attribute_value in list(target_class.__dict__.items()):
            if callable(attribute_value) and not isinstance(attribute_value, type):
                is_magic = attribute_name.startswith("__") and attribute_name.endswith("__")
                if not show_magic_methods and is_magic:
                    continue

                wrapped_method = make_wrapper(
                    attribute_value, attribute_name, target_class.__name__
                )
                setattr(target_class, attribute_name, wrapped_method)

        return target_class

    return decorator
