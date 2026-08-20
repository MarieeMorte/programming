"""
Модуль с unit-тестами для декоратора retry из задания 2.
Проверяет повторные вызовы при ошибках, фильтрацию исключений и работу с задержками.
"""

import unittest
from unittest.mock import patch

from src.lab6.task2 import retry


class TestRetryDecorator(unittest.TestCase):
    """Тесты для декоратора retry."""

    def test_success_first_attempt(self):
        """Проверяет, что при успешном первом вызове задержек не происходит."""

        @retry(attempts=3, delay=0.1)
        def always_ok():
            return "OK"

        with patch("time.sleep") as mock_sleep:
            result = always_ok()
            self.assertEqual(result, "OK")
            mock_sleep.assert_not_called()

    def test_retry_until_success(self):
        """Проверяет, что декоратор повторяет вызовы, пока функция не вернёт успех."""
        counter = 0

        @retry(attempts=3, delay=0.1)
        def flaky():
            nonlocal counter
            counter += 1
            if counter < 3:
                raise ValueError("Временная ошибка")
            return "Успех"

        with patch("time.sleep") as mock_sleep:
            result = flaky()
            self.assertEqual(result, "Успех")
            self.assertEqual(counter, 3)
            self.assertEqual(mock_sleep.call_count, 2)

    def test_all_attempts_fail(self):
        """Проверяет, что если все попытки неудачны, исключение пробрасывается."""

        @retry(attempts=2, delay=0.1)
        def always_fail():
            raise RuntimeError("Всегда падает")

        with patch("time.sleep") as mock_sleep:
            with self.assertRaises(RuntimeError):
                always_fail()
            mock_sleep.assert_called_once_with(0.1)

    def test_filter_exceptions(self):
        """Проверяет, что неподходящие исключения не перехватываются и повторных попыток нет."""

        @retry(attempts=3, delay=0.1, exceptions=(ValueError, TypeError))
        def raise_other():
            raise IndexError("Не подходит")

        with patch("time.sleep") as mock_sleep:
            with self.assertRaises(IndexError):
                raise_other()
            mock_sleep.assert_not_called()

    def test_filter_catches(self):
        """Проверяет, что подходящие исключения перехватываются и приводят к повтору."""
        counter = 0

        @retry(attempts=3, delay=0.1, exceptions=ValueError)
        def raise_value_error():
            nonlocal counter
            counter += 1
            if counter < 3:
                raise ValueError("Перехватываем")
            return "OK"

        with patch("time.sleep") as mock_sleep:
            result = raise_value_error()
            self.assertEqual(result, "OK")
            self.assertEqual(counter, 3)
            mock_sleep.assert_called_with(0.1)

    def test_catch_all_exceptions(self):
        """Проверяет, что при exceptions=None перехватываются все исключения."""
        counter = 0

        @retry(attempts=2, delay=0.1, exceptions=None)
        def any_exception():
            nonlocal counter
            counter += 1
            if counter == 1:
                raise ValueError("Любая ошибка")
            return "OK"

        with patch("time.sleep") as mock_sleep:
            result = any_exception()
            self.assertEqual(result, "OK")
            mock_sleep.assert_called_once_with(0.1)


if __name__ == "__main__":
    unittest.main()
