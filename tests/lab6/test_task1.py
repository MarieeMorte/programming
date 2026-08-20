"""
Модуль с unit-тестами для декоратора logger из задания 1.
Проверяет вывод логов, сохранение метаданных, работу с аргументами и вывод времени.
"""

import io
import re
import time
import unittest
from unittest.mock import patch

from src.lab6.task1 import logger


class TestLoggerDecorator(unittest.TestCase):
    """Тесты для декоратора logger."""

    def test_logger_output(self):
        """Проверяем, что декоратор печатает имя, аргументы, время и результат."""

        @logger
        def add(a, b, c=0):
            return a + b + c

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = add(2, 3, c=5)
            output = mock_stdout.getvalue()

        self.assertIn("Вызов функции: add", output)
        self.assertIn("Аргументы: args=(2, 3), kwargs={'c': 5}", output)
        self.assertIn("Время выполнения:", output)
        self.assertIn("сек.", output)
        self.assertIn("Результат: 10", output)

        self.assertEqual(result, 10)

    def test_logger_metadata(self):
        """Проверяем, что @wraps сохраняет имя и документацию."""

        @logger
        def multiply(x, y):
            """Умножает два числа."""
            return x * y

        self.assertEqual(multiply.__name__, "multiply")
        self.assertEqual(multiply.__doc__, "Умножает два числа.")

    def test_logger_with_different_args(self):
        """Убеждаемся, что декоратор корректно передаёт любые аргументы."""

        @logger
        def concat(*args, sep=" "):
            return sep.join(str(a) for a in args)

        result = concat("Hello", "world", sep=" - ")
        self.assertEqual(result, "Hello - world")

    def test_logger_time_output(self):
        """Проверяем, что время выполнения выводится как число с плавающей точкой."""

        @logger
        def sleep_sort(a):
            time.sleep(0.01)
            return a

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            sleep_sort(42)
            output = mock_stdout.getvalue()

        match = re.search(r"Время выполнения:\s+([0-9.]+)\s+сек\.", output)
        self.assertIsNotNone(match)
        time_value = float(match.group(1))
        self.assertTrue(0.005 < time_value < 0.05)


if __name__ == "__main__":
    unittest.main()
