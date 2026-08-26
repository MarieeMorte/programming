"""Unit-тесты для задания 3."""

import unittest

from src.lab7.task3 import async_requests, sync_requests


class TestRequests(unittest.IsolatedAsyncioTestCase):
    """Тесты для синхронной и асинхронной версий."""

    async def test_sync_vs_async_time(self):
        """Проверяем, что синхронное выполнение занимает больше времени, чем асинхронное."""
        _, sync_total = sync_requests()
        _, async_total = await async_requests()
        self.assertGreater(sync_total, async_total)
        self.assertGreater(sync_total, 5.0)

    async def test_async_time_approx_max_delay(self):
        """
        Проверяем, что асинхронное общее время приблизительно равно
        максимальной задержке (5 с) с погрешностью +- 2,5 секунды.
        """
        _, total = await async_requests()
        self.assertAlmostEqual(total, 5.0, delta=2.5)

    def test_returns_all_urls_sync(self):
        """Проверяем, что синхронная функция возвращает словарь со всеми URL."""
        times, _ = sync_requests()
        self.assertEqual(len(times), 3)
        for url in [
            "https://httpbin.org/get",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/5",
        ]:
            self.assertIn(url, times)

    async def test_returns_all_urls_async(self):
        """Проверяем, что асинхронная функция возвращает словарь со всеми URL."""
        times, _ = await async_requests()
        self.assertEqual(len(times), 3)
        for url in [
            "https://httpbin.org/get",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/5",
        ]:
            self.assertIn(url, times)
