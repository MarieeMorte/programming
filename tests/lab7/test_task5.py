"""Unit-тесты для задания 5."""

import unittest

from src.lab7.task5 import run_threads


class TestRaceCondition(unittest.TestCase):
    """Тесты для демонстрации гонки данных."""

    def test_race_condition(self):
        """Проверяем, что без синхронизации результат меньше ожидаемого."""
        threads = 4
        iterations = 50000
        expected = threads * iterations
        result = run_threads(threads, iterations)
        self.assertLess(result, expected)


if __name__ == "__main__":
    unittest.main()
