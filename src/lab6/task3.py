import time
import types
from functools import wraps

SKIP_MAGIC = {
    '__getattribute__', '__setattr__', '__delattr__',
    '__getattr__', '__setitem__', '__delitem__',
    '__get__', '__set__', '__delete__'
}


def logger(show_magic_methods=True):
    def decorator(cls):
        for attr_name, attr_value in list(cls.__dict__.items()):
            if attr_name in SKIP_MAGIC:
                continue

            if isinstance(attr_value, types.FunctionType):
                is_magic = attr_name.startswith('__') and attr_name.endswith('__')
                if is_magic and not show_magic_methods:
                    continue
                wrapped = _wrap_method(attr_value, cls.__name__)
                setattr(cls, attr_name, wrapped)

            elif isinstance(attr_value, staticmethod):
                original_func = attr_value.__func__
                wrapped_func = _wrap_method(original_func, cls.__name__)
                setattr(cls, attr_name, staticmethod(wrapped_func))

            elif isinstance(attr_value, classmethod):
                original_func = attr_value.__func__
                wrapped_func = _wrap_method(original_func, cls.__name__)
                # noinspection PyTypeChecker
                setattr(cls, attr_name, classmethod(wrapped_func))

        return cls

    return decorator


def _wrap_method(func, class_name):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Класс: {class_name}")
        print(f"Метод: {func.__name__}")
        print(f"Аргументы: args={args}, kwargs={kwargs}")

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        print(f"Время выполнения: {end - start:.6f} сек.")
        print(f"Результат: {result}")
        return result

    return wrapper
