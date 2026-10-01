"""Unit-тесты для задания 1 с изолированными функциями."""

import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from src.lab8.task1 import (
    change_file_permissions,
    change_to_script_directory,
    create_file_with_data,
    main,
    print_current_user,
    print_file_info,
)


class TestTask1Functions(unittest.TestCase):
    """Тесты для отдельных функций task1.py."""

    def setUp(self):
        """Создаём временную директорию и файл для тестов."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        self.filepath = os.path.join(self.temp_dir, "lab_os_file.txt")
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("dummy content")

    def tearDown(self):
        """Возвращаемся в исходную директорию и удаляем временную."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_change_to_script_directory(self):
        """Проверяем, что функция переходит в директорию скрипта."""
        with patch("src.lab8.task1.__file__", os.path.join(self.temp_dir, "task1.py")):
            script_dir = change_to_script_directory()
            self.assertEqual(script_dir, self.temp_dir)
            self.assertEqual(os.getcwd(), self.temp_dir)

    def test_change_to_script_directory_already_there(self):
        """Если уже в нужной директории, переход не происходит."""
        os.chdir(self.temp_dir)
        with patch("src.lab8.task1.__file__", os.path.join(self.temp_dir, "task1.py")):
            script_dir = change_to_script_directory()
            self.assertEqual(script_dir, self.temp_dir)
            self.assertEqual(os.getcwd(), self.temp_dir)

    def test_create_file_with_data_success(self):
        """Файл создаётся и содержит данные."""
        os.remove(self.filepath)
        create_file_with_data(self.filepath)
        self.assertTrue(os.path.exists(self.filepath))
        with open(self.filepath, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Тестовые данные", content)
        self.assertIn("Вторая строка", content)
        self.assertGreater(len(content), 10)

    def test_create_file_with_data_raises_error(self):
        """Если файл не создался, выбрасывается RuntimeError."""
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(RuntimeError) as context:
                create_file_with_data(self.filepath)
            self.assertEqual(str(context.exception), "Файл не создан")

    def test_print_file_info(self):
        """Проверяем вывод информации о файле."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("test data")
        with patch("builtins.print") as mock_print:
            print_file_info(self.filepath)
            calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
            self.assertTrue(any("Размер:" in s for s in calls))
            self.assertTrue(any("Изменён:" in s for s in calls))
            self.assertTrue(any("Доступ:" in s for s in calls))

    def test_print_current_user_os_login(self):
        """Вывод пользователя через os.getlogin."""
        with patch("os.getlogin", return_value="testuser"):
            with patch("builtins.print") as mock_print:
                print_current_user()
                mock_print.assert_called_once_with("Пользователь: testuser")

    def test_print_current_user_fallback(self):
        """Если os.getlogin падает, используется переменная окружения."""
        with patch("os.getlogin", side_effect=OSError("no login")):

            def env_get_side_effect(key, default=None):
                if key in ("USER", "USERNAME"):
                    return "fallbackuser"
                return default

            with patch("os.environ.get", side_effect=env_get_side_effect):
                with patch("builtins.print") as mock_print:
                    print_current_user()
                    mock_print.assert_called_once_with("Пользователь: fallbackuser")

    def test_change_file_permissions_success(self):
        """Права успешно меняются на 0o644."""
        if os.name == "nt":
            with patch("os.chmod") as mock_chmod:
                change_file_permissions(self.filepath)
                mock_chmod.assert_called_once_with(self.filepath, 0o644)
        else:
            os.chmod(self.filepath, 0o777)
            with patch("builtins.print") as mock_print:
                change_file_permissions(self.filepath)
                stat = os.stat(self.filepath)
                self.assertEqual(stat.st_mode & 0o777, 0o644)
                calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
                self.assertTrue(any("Старые права" in s for s in calls))
                self.assertTrue(any("Новые права" in s for s in calls))

    def test_change_file_permissions_permission_error(self):
        """Если прав недостаточно, выводится сообщение об ошибке."""
        with patch("os.stat", return_value=MagicMock(st_mode=0o777)):
            with patch("os.chmod", side_effect=PermissionError("Access denied")):
                with patch("builtins.print") as mock_print:
                    change_file_permissions(self.filepath)
                    calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
                    self.assertTrue(any("Не удалось сменить права" in s for s in calls))

    def test_main_integration(self):
        """Полный прогон main во временной директории."""
        with patch("src.lab8.task1.__file__", os.path.join(self.temp_dir, "task1.py")):
            with patch("builtins.print"):
                main()
        self.assertTrue(os.path.exists(self.filepath))
        if os.name != "nt":
            stat = os.stat(self.filepath)
            self.assertEqual(stat.st_mode & 0o777, 0o644)

    def test_main_creates_file_in_correct_dir(self):
        """Проверяем, что main создаёт файл именно в директории скрипта."""
        other_dir = os.path.join(self.temp_dir, "other")
        os.makedirs(other_dir)
        os.chdir(other_dir)
        self.assertNotEqual(os.getcwd(), self.temp_dir)

        with patch("src.lab8.task1.__file__", os.path.join(self.temp_dir, "task1.py")):
            with patch("builtins.print"):
                main()

        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "lab_os_file.txt")))
        self.assertFalse(os.path.exists(os.path.join(other_dir, "lab_os_file.txt")))


if __name__ == "__main__":
    unittest.main()
