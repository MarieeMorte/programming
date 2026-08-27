"""Unit-тесты для задания 1 (упрощённая версия с main)."""

import os
import shutil
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

from src.lab8.task1 import main


class TestOSLab(unittest.TestCase):
    """Тесты для скрипта task1.py с изоляцией через моки."""

    def setUp(self):
        """Создаём временную папку и подменяем __file__, чтобы main работал в ней."""
        self.temp_dir = tempfile.mkdtemp()
        # Сохраняем исходную директорию
        self.original_dir = os.getcwd()
        # Патчим __file__ в модуле task1, чтобы main думал, что он лежит в temp_dir
        self.patcher = patch("src.lab8.task1.__file__", os.path.join(self.temp_dir, "task1.py"))
        self.mock_file = self.patcher.start()

    def tearDown(self):
        """Останавливаем патч и удаляем временную папку."""
        self.patcher.stop()
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_file_created(self):
        """Проверяем, что файл создаётся в целевой директории."""
        main()
        file_path = os.path.join(self.temp_dir, "lab_os_file.txt")
        self.assertTrue(os.path.exists(file_path))

    def test_file_size(self):
        """Проверяем, что размер файла соответствует данным."""
        main()
        file_path = os.path.join(self.temp_dir, "lab_os_file.txt")
        with open(file_path, "rb") as f:
            content = f.read()
        size = os.path.getsize(file_path)
        self.assertEqual(size, len(content))
        self.assertGreater(size, 0)

    def test_metadata_dates(self):
        """Проверяем, что даты изменения и доступа установлены корректно."""
        main()
        file_path = os.path.join(self.temp_dir, "lab_os_file.txt")
        mtime = os.path.getmtime(file_path)
        atime = os.path.getatime(file_path)
        now = datetime.now().timestamp()
        self.assertGreater(mtime, 0)
        self.assertGreater(atime, 0)
        self.assertLess(abs(now - mtime), 10)
        self.assertLess(abs(now - atime), 10)

    def test_user_displayed(self):
        """Проверяем, что пользователь выводится (хотя бы не пусто)."""
        # Перехватываем вывод, чтобы проверить наличие пользователя
        with patch("builtins.print") as mock_print:
            main()
            # Ищем среди вызовов print строку с "Пользователь:"
            calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
            self.assertTrue(any("Пользователь:" in s for s in calls))

    def test_permissions_changed(self):
        """Проверяем, что права доступа изменились."""
        main()
        file_path = os.path.join(self.temp_dir, "lab_os_file.txt")
        if os.name == "nt":
            # На Windows просто проверяем, что файл доступен для записи
            self.assertTrue(os.access(file_path, os.W_OK))
        else:
            stat = os.stat(file_path)
            perm = stat.st_mode & 0o777
            self.assertEqual(perm, 0o644)

    def test_directory_change(self):
        """Проверяем, что скрипт переходит в папку скрипта (temp_dir)."""
        self.assertNotEqual(os.getcwd(), self.temp_dir)
        main()
        self.assertEqual(os.getcwd(), self.temp_dir)
        file_path = os.path.join(self.temp_dir, "lab_os_file.txt")
        self.assertTrue(os.path.exists(file_path))

    def test_file_exists_check(self):
        """Проверяем, что файл существует после выполнения main."""
        main()
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "lab_os_file.txt")))


if __name__ == "__main__":
    unittest.main()
