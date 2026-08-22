"""Unit-тесты для задания 4 (потоки)."""

import unittest

from src.lab7.task4 import run_sequential, run_threaded


class TestThreading(unittest.TestCase):
    """Тесты для последовательного и потокового выполнения."""

    def setUp(self):
        """Подготовка данных для тестов."""
        self.messages = ["A", "B", "C"]
        self.delay = 1.0
        self.tolerance = 0.3

    def test_sequential_time(self):
        """Проверяем, что последовательное время ≈ количество * задержка."""
        total = run_sequential(self.messages, self.delay)
        expected = len(self.messages) * self.delay
        self.assertAlmostEqual(total, expected, delta=self.tolerance)

    def test_threaded_time(self):
        """Проверяем, что потоковое время ≈ задержка (максимальная)."""
        total = run_threaded(self.messages, self.delay)
        expected = self.delay
        self.assertAlmostEqual(total, expected, delta=self.tolerance)

    def test_threaded_faster_than_sequential(self):
        """Проверяем, что потоки выполняются быстрее последовательного."""
        seq_time = run_sequential(self.messages, self.delay)
        thr_time = run_threaded(self.messages, self.delay)
        self.assertLess(thr_time, seq_time)


if __name__ == "__main__":
    unittest.main()
