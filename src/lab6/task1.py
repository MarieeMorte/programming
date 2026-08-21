"""Модуль с декоратором logger для логирования вызовов функций."""

import time
from functools import wraps


def logger(function):
    """Декоратор, выводящий имя функции, аргументы и время выполнения."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"Вызов функции: {function.__name__}")
        print(f"Аргументы: args={args}, kwargs={kwargs}")

        start = time.perf_counter()
        result = function(*args, **kwargs)
        end = time.perf_counter()

        print(f"Время выполнения: {end - start} сек.")
        print(f"Результат: {result}")
        return result

    return wrapper
