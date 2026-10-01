"""Unit-тесты для задания 6 (решение гонки данных)."""

import unittest

from src.lab7.task6 import run_threads_safe


class TestLockSolution(unittest.TestCase):
    """Тесты для проверки корректности с блокировкой."""

    def test_correctness_with_lock(self):
        """Проверяем, что результат всегда равен ожидаемому."""
        threads = 4
        iterations = 50000
        expected = threads * iterations
        result = run_threads_safe(threads, iterations)
        self.assertEqual(result, expected)

    def test_reproducible_result(self):
        """Запускаем несколько раз и проверяем, что результат стабилен."""
        for _ in range(5):
            threads = 5
            iterations = 20000
            expected = threads * iterations
            result = run_threads_safe(threads, iterations)
            self.assertEqual(result, expected, "Результат должен быть всегда одинаковым")


if __name__ == "__main__":
    unittest.main()
