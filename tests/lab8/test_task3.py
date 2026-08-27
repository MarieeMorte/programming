"""Unit-тесты для задания 3 (упрощённая версия)."""

import os
import unittest
from unittest.mock import MagicMock, patch

import psutil  # type: ignore

from src.lab8.task3 import (
    add_env_var,
    get_process_info,
    kill_process,
    list_processes,
    set_process_priority,
    show_env_vars,
    system_info,
)


class TestProcessFunctions(unittest.TestCase):
    """Тесты для функций работы с процессами."""

    def test_list_processes_returns_list(self):
        """Проверяем, что list_processes возвращает список словарей."""
        procs = list_processes()
        self.assertIsInstance(procs, list)
        if procs:
            self.assertIn("pid", procs[0])
            self.assertIn("name", procs[0])

    @patch("psutil.Process")
    def test_get_process_info_success(self, mock_process):
        """Проверяем получение информации о процессе (упрощённый набор полей)."""
        mock_instance = MagicMock()
        mock_instance.name.return_value = "test_proc"
        mock_instance.status.return_value = "running"
        mock_instance.username.return_value = "user"
        mock_instance.cpu_percent.return_value = 5.0
        mock_instance.memory_info.return_value.rss = 100 * 1024 * 1024  # 100 МБ
        mock_instance.cmdline.return_value = ["test", "--arg"]
        mock_instance.num_threads.return_value = 1
        mock_instance.nice.return_value = 0
        mock_process.return_value = mock_instance

        info = get_process_info(1234)
        self.assertEqual(info["pid"], 1234)
        self.assertEqual(info["name"], "test_proc")
        self.assertEqual(info["status"], "running")
        self.assertEqual(info["username"], "user")
        self.assertEqual(info["cpu_percent"], 5.0)
        self.assertEqual(info["memory_mb"], 100)
        self.assertEqual(info["cmdline"], "test --arg")
        self.assertEqual(info["num_threads"], 1)
        self.assertEqual(info["nice"], 0)

    @patch("psutil.Process")
    def test_get_process_info_not_found(self, mock_process):
        """Проверяем обработку ошибки, если процесс не найден."""
        mock_process.side_effect = psutil.NoSuchProcess(1234)
        with self.assertRaises(psutil.NoSuchProcess):
            get_process_info(1234)

    @patch("psutil.Process")
    def test_kill_process_success(self, mock_process):
        """Проверяем успешное завершение процесса."""
        mock_instance = MagicMock()
        mock_process.return_value = mock_instance
        result = kill_process(1234)
        self.assertTrue(result)
        mock_instance.terminate.assert_called_once()
        mock_instance.wait.assert_called_once_with(timeout=3)

    @patch("psutil.Process")
    def test_kill_process_timeout(self, mock_process):
        """Проверяем принудительное убийство при таймауте."""
        mock_instance = MagicMock()
        mock_instance.wait.side_effect = psutil.TimeoutExpired(3)
        mock_process.return_value = mock_instance
        result = kill_process(1234)
        self.assertTrue(result)
        mock_instance.terminate.assert_called_once()
        mock_instance.kill.assert_called_once()


class TestEnvFunctions(unittest.TestCase):
    """Тесты для работы с переменными окружения."""

    def test_show_env_vars(self):
        """Проверяем, что возвращается словарь."""
        env = show_env_vars()
        self.assertIsInstance(env, dict)
        self.assertIn("PATH", env)

    def test_add_env_var(self):
        """Проверяем добавление/изменение переменной."""
        key = "TEST_VAR"
        value = "test_value"
        add_env_var(key, value)
        self.assertEqual(os.environ.get(key), value)
        del os.environ[key]


class TestPriorityFunction(unittest.TestCase):
    """Тесты для изменения приоритета."""

    @patch("psutil.Process")
    def test_set_priority_success(self, mock_process):
        """Проверяем успешное изменение приоритета."""
        mock_instance = MagicMock()
        mock_process.return_value = mock_instance
        result = set_process_priority(1234, -5)
        self.assertTrue(result)
        mock_instance.nice.assert_called_once_with(-5)


class TestSystemInfo(unittest.TestCase):
    """Тесты для системной информации."""

    def test_system_info_returns_dict(self):
        """Проверяем, что system_info возвращает словарь с ключевыми полями."""
        info = system_info()
        self.assertIsInstance(info, dict)
        self.assertIn("system", info)
        self.assertIn("cpu_count", info)  # теперь ожидаем cpu_count
        self.assertIn("memory", info)
        self.assertIn("disk", info)
        self.assertIn("swap", info)


if __name__ == "__main__":
    unittest.main()
