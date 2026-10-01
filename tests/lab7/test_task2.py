"""Unit-тесты для функции run_multiple."""

import asyncio
import unittest
from io import StringIO
from unittest.mock import patch

from src.lab7.task2 import run_multiple


class TestRunMultiple(unittest.TestCase):
    """Тесты конкурентного запуска."""

    def test_execution_time(self):
        """Проверяет, что общее время ~3 секунды, а не сумма."""

        async def run():
            start = asyncio.get_event_loop().time()
            await run_multiple()
            elapsed = asyncio.get_event_loop().time() - start
            self.assertAlmostEqual(elapsed, 3.0, delta=0.2)

        asyncio.run(run())

    def test_output_messages(self):
        """Проверяет, что все три сообщения были выведены."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:

            async def run():
                await run_multiple()

            asyncio.run(run())
            output = mock_stdout.getvalue()
            expected_messages = [
                "Через 2 секунды",
                "Через 1 секунду",
                "Через 3 секунды",
            ]
            for msg in expected_messages:
                self.assertIn(msg, output)


if __name__ == "__main__":
    unittest.main()
