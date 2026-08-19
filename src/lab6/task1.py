import time
from functools import wraps


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов функции: {func.__name__}")
        print(f"Аргументы: args={args}, kwargs={kwargs}")

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        print(f"Время выполнения: {end - start:.6f} сек.")
        print(f"Результат: {result}")
        return result

    return wrapper
