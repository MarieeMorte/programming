"""Unit-тесты для задания 3 (версия без psutil)."""

import os
import unittest
from unittest.mock import patch

from src.lab8.task3 import (
    get_process_info,
    kill_process,
    list_processes,
    set_process_priority,
    system_info,
)


class TestProcessFunctions(unittest.TestCase):
    """Тесты для функций работы с процессами."""

    @patch("src.lab8.task3._run_cmd")
    def test_list_processes(self, mock_run_cmd):
        """Проверяем парсинг вывода tasklist."""
        mock_run_cmd.return_value = (
            '"cmd.exe","1234","Console","1","8 192 K"\n'
            '"notepad.exe","5678","Console","1","12 345 K"'
        )
        procs = list_processes()
        self.assertEqual(procs, [(1234, "cmd.exe"), (5678, "notepad.exe")])
        mock_run_cmd.assert_called_once_with("tasklist /FO CSV /NH")

    @patch("src.lab8.task3._run_cmd")
    def test_get_process_info(self, mock_run_cmd):
        """Проверяем парсинг вывода wmic."""
        mock_run_cmd.return_value = (
            '"Name","Status","CommandLine","ThreadCount","WorkingSetSize"\n'
            '"python.exe","Running","C:\\Python\\python.exe script.py","5","104857600"'
        )
        info = get_process_info(1234)
        expected = {
            "pid": 1234,
            "name": "python.exe",
            "status": "Running",
            "cmdline": "C:\\Python\\python.exe script.py",
            "num_threads": 5,
            "memory_mb": 100,
            "username": "N/A",
            "cpu_percent": 0.0,
            "nice": None,
        }
        self.assertEqual(info, expected)
        mock_run_cmd.assert_called_once_with(
            "wmic process where ProcessId=1234 get "
            "Name,Status,CommandLine,ThreadCount,WorkingSetSize /FORMAT:CSV"
        )

    @patch("src.lab8.task3._run_cmd")
    def test_get_process_info_empty_output(self, mock_run_cmd):
        """Проверяем поведение при пустом выводе (процесс не найден)."""
        mock_run_cmd.return_value = ""
        info = get_process_info(9999)
        self.assertEqual(info["pid"], 9999)
        self.assertIsNone(info.get("name"))
        self.assertEqual(info["username"], "N/A")
        self.assertEqual(info["cpu_percent"], 0.0)
        self.assertIsNone(info["nice"])
        mock_run_cmd.assert_called_once()

    @patch("src.lab8.task3._run_cmd")
    def test_kill_process(self, mock_run_cmd):
        """Проверяем вызов taskkill."""
        kill_process(1234)
        mock_run_cmd.assert_called_once_with("taskkill /PID 1234 /F", check=True)

    @patch("src.lab8.task3._run_cmd")
    def test_set_process_priority_normal(self, mock_run_cmd):
        """Проверяем преобразование nice -> приоритет Windows."""
        set_process_priority(1234, 0)
        mock_run_cmd.assert_called_once_with(
            "wmic process where ProcessId=1234 call setpriority 2", check=True
        )

    @patch("src.lab8.task3._run_cmd")
    def test_set_process_priority_high(self, mock_run_cmd):
        """Проверяем высокий приоритет (nice <= -5)."""
        set_process_priority(1234, -10)
        mock_run_cmd.assert_called_once_with(
            "wmic process where ProcessId=1234 call setpriority 0", check=True
        )

    @patch("src.lab8.task3._run_cmd")
    def test_set_process_priority_low(self, mock_run_cmd):
        """Проверяем низкий приоритет (nice > 15)."""
        set_process_priority(1234, 18)
        mock_run_cmd.assert_called_once_with(
            "wmic process where ProcessId=1234 call setpriority 4", check=True
        )


class TestSystemInfo(unittest.TestCase):
    """Тесты для системной информации."""

    @patch("src.lab8.task3._run_cmd")
    def test_system_info(self, mock_run_cmd):
        """Проверяем сбор информации через wmic."""
        mock_run_cmd.side_effect = [
            '"TotalVisibleMemorySize","FreePhysicalMemory"\n"8388608","4194304"',
            '"Size","FreeSpace"\n"107374182400","53687091200"',
            '"AllocatedBaseSize","CurrentUsage"\n"4096","2048"',
        ]
        info = system_info()
        self.assertEqual(info["system"], "Windows")
        self.assertIn("release", info)
        self.assertIn("processor", info)
        self.assertIsNotNone(info["cpu_count"])
        self.assertAlmostEqual(info["memory"]["total"], 8388608 * 1024)
        self.assertAlmostEqual(info["memory"]["available"], 4194304 * 1024)
        self.assertAlmostEqual(info["memory"]["percent"], 50.0)
        self.assertEqual(info["disk"]["total"], 107374182400)
        self.assertEqual(info["disk"]["free"], 53687091200)
        self.assertAlmostEqual(info["disk"]["percent"], 50.0)
        self.assertEqual(info["swap"]["total"], 4096 * 1024 * 1024)
        self.assertEqual(info["swap"]["used"], 2048 * 1024 * 1024)
        self.assertAlmostEqual(info["swap"]["percent"], 50.0)

    @patch("src.lab8.task3._run_cmd")
    def test_system_info_partial_data(self, mock_run_cmd):
        """Проверяем поведение при отсутствии части данных."""
        mock_run_cmd.side_effect = [
            "",
            "",
            "",
        ]
        info = system_info()
        self.assertEqual(info["memory"], {})
        self.assertEqual(info["disk"], {})
        self.assertEqual(info["swap"], {})


class TestEnvFunctions(unittest.TestCase):
    """Тесты для переменных окружения."""

    def test_env_contains_path(self):
        """Проверяем, что os.environ содержит ключ PATH."""
        self.assertIn("PATH", os.environ)

    def test_env_modification(self):
        """Проверяем, что можно добавить и удалить переменную."""
        key = "TEST_VAR_UNIT"
        value = "test_value"
        os.environ[key] = value
        self.assertEqual(os.environ[key], value)
        del os.environ[key]
        self.assertNotIn(key, os.environ)


if __name__ == "__main__":
    unittest.main()
