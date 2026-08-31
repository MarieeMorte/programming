"""Unit-тесты для задания 3 (версия с subprocess и /FORMAT:LIST)."""

import os
import unittest
from unittest.mock import patch

from src.lab8.task3 import (
    change_to_script_directory,
    get_process_info,
    kill_process,
    list_processes,
    set_process_priority,
    system_info,
)


class TestChangeDirectory(unittest.TestCase):
    """Тесты для функции change_to_script_directory."""

    @patch("src.lab8.task3.os.getcwd")
    @patch("src.lab8.task3.os.chdir")
    @patch("src.lab8.task3.os.path.dirname")
    @patch("src.lab8.task3.os.path.abspath")
    @patch("src.lab8.task3.__file__", "C:\\some\\path\\task3.py")
    def test_change_to_script_directory(self, mock_abspath, mock_dirname, mock_chdir, mock_getcwd):
        """Проверяем переход в директорию скрипта."""
        mock_abspath.return_value = "C:\\some\\path\\task3.py"
        mock_dirname.return_value = "C:\\some\\path"
        mock_getcwd.return_value = "C:\\other"
        with patch("builtins.print") as mock_print:
            change_to_script_directory()
            mock_chdir.assert_called_once_with("C:\\some\\path")
            mock_print.assert_called_once_with("Перешли в C:\\some\\path")

    @patch("src.lab8.task3.os.getcwd")
    @patch("src.lab8.task3.os.chdir")
    @patch("src.lab8.task3.os.path.dirname")
    @patch("src.lab8.task3.os.path.abspath")
    @patch("src.lab8.task3.__file__", "C:\\same\\task3.py")
    def test_change_to_script_directory_already_there(
            self, mock_abspath, mock_dirname, mock_chdir, mock_getcwd
    ):
        """Если уже в нужной директории, переход не происходит."""
        mock_abspath.return_value = "C:\\same\\task3.py"
        mock_dirname.return_value = "C:\\same"
        mock_getcwd.return_value = "C:\\same"
        with patch("builtins.print") as mock_print:
            change_to_script_directory()
            mock_chdir.assert_not_called()
            mock_print.assert_not_called()


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
        """Проверяем парсинг вывода wmic в формате LIST."""
        mock_run_cmd.return_value = (
            "Name=python.exe\n"
            "Status=Running\n"
            "CommandLine=C:\\Python\\python.exe script.py\n"
            "ThreadCount=5\n"
            "WorkingSetSize=104857600"
        )
        info = get_process_info(1234)
        expected = {
            "pid": 1234,
            "name": "python.exe",
            "status": "Running",
            "cmdline": "C:\\Python\\python.exe script.py",
            "num_threads": 5,
            "memory_mb": 100,
        }
        self.assertEqual(info, expected)
        mock_run_cmd.assert_called_once_with(
            "wmic process where ProcessId=1234 get "
            "Name,Status,CommandLine,ThreadCount,WorkingSetSize /FORMAT:LIST"
        )

    @patch("src.lab8.task3._run_cmd")
    def test_get_process_info_empty_output(self, mock_run_cmd):
        """Проверяем поведение при пустом выводе (процесс не найден)."""
        mock_run_cmd.return_value = ""
        info = get_process_info(9999)
        expected = {
            "pid": 9999,
            "name": "N/A",
            "status": "N/A",
            "cmdline": "",
            "num_threads": 0,
            "memory_mb": 0,
        }
        self.assertEqual(info, expected)

    @patch("src.lab8.task3._run_cmd")
    def test_get_process_info_missing_fields(self, mock_run_cmd):
        """Проверяем, что отсутствующие поля заполняются значениями по умолчанию."""
        mock_run_cmd.return_value = "Name=python.exe\nThreadCount=2"
        info = get_process_info(1234)
        self.assertEqual(info["name"], "python.exe")
        self.assertEqual(info["status"], "N/A")
        self.assertEqual(info["cmdline"], "")
        self.assertEqual(info["num_threads"], 2)
        self.assertEqual(info["memory_mb"], 0)

    @patch("src.lab8.task3._run_cmd")
    def test_kill_process(self, mock_run_cmd):
        """Проверяем вызов taskkill."""
        kill_process(1234)
        mock_run_cmd.assert_called_once_with("taskkill /PID 1234 /F", check=True)

    @patch("src.lab8.task3._run_cmd")
    def test_set_process_priority_valid_class(self, mock_run_cmd):
        """Проверяем вызов с корректным классом приоритета (0-4)."""
        set_process_priority(1234, 2)
        mock_run_cmd.assert_called_once_with(
            "wmic process where ProcessId=1234 call setpriority 2", check=True
        )
        set_process_priority(5678, 0)
        mock_run_cmd.assert_called_with(
            "wmic process where ProcessId=5678 call setpriority 0", check=True
        )

    def test_set_process_priority_invalid_class(self):
        """Проверяем, что выбрасывается ValueError при недопустимом классе."""
        with self.assertRaises(ValueError):
            set_process_priority(1234, -1)
        with self.assertRaises(ValueError):
            set_process_priority(1234, 5)


class TestSystemInfo(unittest.TestCase):
    """Тесты для системной информации."""

    @patch("src.lab8.task3.platform.system")
    @patch("src.lab8.task3._run_cmd")
    def test_system_info(self, mock_run_cmd, mock_platform):
        """Проверяем сбор информации через wmic (CSV)."""
        mock_platform.return_value = "Windows"
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
        self.assertAlmostEqual(info["memory"]["percent"], 50.0, places=1)
        self.assertEqual(info["disk"]["total"], 107374182400)
        self.assertEqual(info["disk"]["free"], 53687091200)
        self.assertAlmostEqual(info["disk"]["percent"], 50.0, places=1)
        self.assertEqual(info["swap"]["total"], 4096 * 1024 * 1024)
        self.assertEqual(info["swap"]["used"], 2048 * 1024 * 1024)
        self.assertAlmostEqual(info["swap"]["percent"], 50.0, places=1)

    @patch("src.lab8.task3._run_cmd")
    def test_system_info_partial_data(self, mock_run_cmd):
        """Проверяем поведение при отсутствии части данных."""
        mock_run_cmd.side_effect = ["", "", ""]
        info = system_info()
        self.assertEqual(info["memory"], {})
        self.assertEqual(info["disk"], {})
        self.assertEqual(info["swap"], {})

    @patch("src.lab8.task3._run_cmd")
    def test_system_info_invalid_numbers(self, mock_run_cmd):
        """Проверяем, что некорректные числа не ломают код."""
        mock_run_cmd.side_effect = [
            '"TotalVisibleMemorySize","FreePhysicalMemory"\n"abc","def"',
            '"Size","FreeSpace"\n"xyz","uvw"',
            '"AllocatedBaseSize","CurrentUsage"\n"",""',
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
