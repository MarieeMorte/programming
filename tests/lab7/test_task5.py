"""Unit-тесты для задания 5 (гонка данных)."""

import unittest

from src.lab7.task5 import run_threads


class TestRaceCondition(unittest.TestCase):
    """Тесты для демонстрации гонки данных."""

    def test_without_lock_incorrect(self):
        """Проверяем, что без блокировки результат не равен ожидаемому."""
        threads = 4
        iterations = 50000
        expected = threads * iterations
        result = run_threads(threads, iterations, use_lock=False)
        self.assertLess(result, expected)

    def test_with_lock_correct(self):
        """Проверяем, что с блокировкой результат равен ожидаемому."""
        threads = 4
        iterations = 50000
        expected = threads * iterations
        result = run_threads(threads, iterations, use_lock=True)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
