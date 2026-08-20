"""
Модуль с unit-тестами для декоратора класса logger из задания 3.
Проверяет логирование всех методов, фильтрацию магических методов,
обработку статических и классовых методов, сохранение метаданных.
"""

import io
import unittest
from unittest.mock import patch

from src.lab6.task3 import logger


class TestLoggerClassDecorator(unittest.TestCase):
    """Тесты для декоратора класса logger."""

    def test_logging_all_methods_including_magic(self):
        """Проверяем, что логируются все методы, включая магические."""

        @logger(show_magic_methods=True)
        class TestClass:
            """Внутренний тестовый класс."""

            # pylint: disable=too-few-public-methods

            def __init__(self, x):
                """Инициализация с сохранением значения."""
                self.x = x

            def method(self, y):
                """Простой метод, возвращающий сумму."""
                return self.x + y

            def __str__(self):
                """Строковое представление объекта."""
                return f"Test({self.x})"

            def __add__(self, other):
                """Сложение двух объектов."""
                return TestClass(self.x + other.x)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            obj = TestClass(10)
            obj.method(5)
            str(obj)
            _ = obj + TestClass(3)
            output = mock_stdout.getvalue()

        self.assertIn("Метод: __init__", output)
        self.assertIn("Метод: method", output)
        self.assertIn("Метод: __str__", output)
        self.assertIn("Метод: __add__", output)
        self.assertIn("Результат: 15", output)
        self.assertIn("Результат: Test(10)", output)

    def test_skip_magic_methods(self):
        """Проверяем, что при show_magic_methods=False магические методы не логируются."""

        @logger(show_magic_methods=False)
        class TestClass:
            """Внутренний тестовый класс."""

            # pylint: disable=too-few-public-methods

            def __init__(self, x):
                """Инициализация с сохранением значения."""
                self.x = x

            def method(self, y):
                """Простой метод, возвращающий сумму."""
                return self.x + y

            def __str__(self):
                """Строковое представление объекта."""
                return f"Test({self.x})"

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            obj = TestClass(10)
            obj.method(5)
            str(obj)
            output = mock_stdout.getvalue()

        self.assertIn("Метод: method", output)
        self.assertNotIn("Метод: __init__", output)
        self.assertNotIn("Метод: __str__", output)

    def test_skip_critical_magic_methods(self):
        """Проверяем, что критические методы (__getattribute__ и др.) не оборачиваются."""

        @logger(show_magic_methods=True)
        class TestClass:
            """Внутренний тестовый класс."""

            # pylint: disable=too-few-public-methods

            def __init__(self, x):
                """Инициализация с сохранением значения."""
                self.x = x

            def __getattribute__(self, name):
                """Переопределённый доступ к атрибутам."""
                return object.__getattribute__(self, name)

        try:
            obj = TestClass(5)
            self.assertEqual(obj.x, 5)
        except RecursionError:
            self.fail("__getattribute__ был обёрнут, вызвав рекурсию")

    def test_static_methods(self):
        """Проверяем, что статические методы логируются."""

        @logger(show_magic_methods=True)
        class TestClass:
            """Внутренний тестовый класс."""

            # pylint: disable=too-few-public-methods

            @staticmethod
            def static_method(a, b):
                """Статический метод, складывающий два числа."""
                return a + b

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = TestClass.static_method(3, 4)
            output = mock_stdout.getvalue()
        self.assertEqual(result, 7)
        self.assertIn("Метод: static_method", output)
        self.assertIn("Результат: 7", output)

    def test_class_methods(self):
        """Проверяем, что классовые методы логируются."""

        @logger(show_magic_methods=True)
        class TestClass:
            """Внутренний тестовый класс."""

            # pylint: disable=too-few-public-methods

            @classmethod
            def class_method(cls, x):
                """Классовый метод, умножающий число на 2."""
                return x * 2

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = TestClass.class_method(5)
            output = mock_stdout.getvalue()
        self.assertEqual(result, 10)
        self.assertIn("Метод: class_method", output)
        self.assertIn("Результат: 10", output)

    def test_preserve_metadata(self):
        """Проверяем, что имя и документация метода сохраняются (благодаря @wraps)."""

        @logger(show_magic_methods=True)
        class TestClass:
            """Внутренний тестовый класс."""

            # pylint: disable=too-few-public-methods

            def my_method(self, x):
                """Документация."""
                return x

        self.assertEqual(TestClass.my_method.__name__, "my_method")
        self.assertEqual(TestClass.my_method.__doc__, "Документация.")


if __name__ == "__main__":
    unittest.main()
