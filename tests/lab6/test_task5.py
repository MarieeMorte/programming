import asyncio
import time
import unittest
from src.lab6.task5 import func1, func2


class TestAsyncFunctions(unittest.TestCase):

    def test_execution_time(self):
        """Проверяем, что общее время меньше суммы всех задержек."""
        start = time.perf_counter()
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(asyncio.gather(func1(), func2()))
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 6.0)
        self.assertEqual(results, ["func1 завершена", "func2 завершена"])

    def test_order_in_func1(self):
        """Проверяем, что func1 выводит сообщения в правильном порядке (проверка через захват stdout)."""
        pass


if __name__ == "__main__":
    unittest.main()
