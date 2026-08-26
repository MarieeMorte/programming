"""Unit-тесты для функции async_print."""

import asyncio
import unittest
from io import StringIO
from unittest.mock import patch

from src.lab7.task1 import async_print


class TestAsyncPrint(unittest.TestCase):
    """Тесты для async_print."""

    def test_delay(self):
        """Проверяет, что задержка соответствует переданной."""

        async def run():
            start = asyncio.get_event_loop().time()
            await async_print(0.5, "test")
            elapsed = asyncio.get_event_loop().time() - start
            self.assertAlmostEqual(elapsed, 0.5, delta=0.1)

        asyncio.run(run())

    def test_output(self):
        """Проверяет, что сообщение выводится корректно."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:

            async def run():
                await async_print(0.1, "Hello")

            asyncio.run(run())
            self.assertEqual(mock_stdout.getvalue().strip(), "Hello")


if __name__ == "__main__":
    unittest.main()
