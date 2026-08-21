"""
Модуль с unit-тестами для декоратора logger для классов из задания 3.
Проверяет логирование методов (включая магические), фильтрацию магических методов,
сохранение метаданных и вывод времени.
"""

import io
import re
import time
import unittest
from unittest.mock import patch

from src.lab6.task3 import logger


class TestClassLoggerDecorator(unittest.TestCase):
    """Тесты для декоратора logger, применяемого к классам."""

    def test_logger_regular_method(self):
        """Проверяет логирование обычного метода класса."""

        @logger()
        class Calculator:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки логирования обычного метода."""

            def add(self, a, b):
                """Складывает два числа."""
                return a + b

        calc = Calculator()
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = calc.add(3, 5)
            output = mock_stdout.getvalue()

        self.assertIn("Вызов метода: Calculator.add", output)
        self.assertIn("args=(<", output)
        self.assertIn("3, 5", output)
        self.assertIn("kwargs={}", output)
        self.assertIn("Время выполнения:", output)
        self.assertIn("сек.", output)
        self.assertIn("Результат: 8", output)
        self.assertEqual(result, 8)

    def test_logger_magic_methods_enabled(self):
        """Проверяет, что при show_magic_methods=True логируются магические методы."""

        @logger()
        class Person:  # pylint: disable=too-few-public-methods
            """Класс-заглушка с магическими методами."""

            def __init__(self, name, age):
                self.name = name
                self.age = age

            def __str__(self):
                return f"{self.name}, {self.age}"

            def greet(self):
                """Обычный метод."""
                return f"Hello, {self.name}"

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            person = Person("Alice", 30)
            _ = str(person)
            _ = person.greet()
            output = mock_stdout.getvalue()

        self.assertIn("Вызов метода: Person.__init__", output)
        self.assertIn("args=(<", output)
        self.assertIn("'Alice', 30", output)
        self.assertIn("kwargs={}", output)
        self.assertIn("Результат: None", output)

        self.assertIn("Вызов метода: Person.__str__", output)
        self.assertIn("args=(<", output)
        self.assertIn("kwargs={}", output)
        self.assertIn("Результат: Alice, 30", output)

        self.assertIn("Вызов метода: Person.greet", output)
        self.assertIn("args=(<", output)
        self.assertIn("kwargs={}", output)
        self.assertIn("Результат: Hello, Alice", output)

    def test_logger_skip_magic_methods(self):
        """Проверяет, что при show_magic_methods=False магические методы не логируются."""

        @logger(show_magic_methods=False)
        class Person:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки пропуска магических методов."""

            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def get_name(self):
                """Возвращает имя."""
                return self.name

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            person = Person("Bob")
            _ = str(person)
            _ = person.get_name()
            output = mock_stdout.getvalue()

        self.assertNotIn("Вызов метода: Person.__init__", output)
        self.assertNotIn("Вызов метода: Person.__str__", output)
        self.assertIn("Вызов метода: Person.get_name", output)
        self.assertIn("Результат: Bob", output)

    def test_logger_metadata_preserved(self):
        """Проверяет, что декоратор сохраняет имя и документацию методов."""

        @logger()
        class Demo:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки сохранения метаданных."""

            def process(self, x):
                """Удваивает число."""
                return x * 2

        self.assertEqual(Demo.process.__name__, "process")
        self.assertEqual(Demo.process.__doc__, "Удваивает число.")

    def test_logger_with_different_args(self):
        """Проверяет логирование методов с произвольными аргументами (*args, **kwargs)."""

        @logger()
        class Formatter:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки различных аргументов."""

            def concat(self, *args, sep=" "):
                """Объединяет аргументы через разделитель."""
                return sep.join(str(a) for a in args)

        fmt = Formatter()
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = fmt.concat("Hello", "world", sep=" - ")
            output = mock_stdout.getvalue()

        self.assertIn("Вызов метода: Formatter.concat", output)
        self.assertIn("args=(<", output)
        self.assertIn("'Hello', 'world'", output)
        self.assertIn("kwargs={'sep': ' - '}", output)
        self.assertIn("Результат: Hello - world", output)
        self.assertEqual(result, "Hello - world")

    def test_logger_time_output(self):
        """Проверяет, что время выполнения выводится как число с плавающей точкой."""

        @logger()
        class Sleeper:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки времени выполнения."""

            def wait(self, seconds):
                """Ждёт указанное количество секунд."""
                time.sleep(seconds)
                return "done"

        obj = Sleeper()
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            obj.wait(0.01)
            output = mock_stdout.getvalue()

        match = re.search(r"Время выполнения:\s+([0-9.]+)\s+сек\.", output)
        self.assertIsNotNone(match)
        time_value = float(match.group(1))
        self.assertTrue(0.005 < time_value < 0.05)

    def test_logger_empty_class(self):
        """Проверяет, что декоратор корректно обрабатывает класс без методов."""

        @logger()
        class Empty:  # pylint: disable=too-few-public-methods
            """Пустой класс без методов."""

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            _ = Empty()
            output = mock_stdout.getvalue()
            self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
