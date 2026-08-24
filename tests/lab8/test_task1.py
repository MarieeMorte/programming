"""Unit-тесты для задания 1 лабораторной работы по библиотеке os."""

import os
import shutil
import tempfile
import unittest
from datetime import datetime

from src.lab8.task1 import process_files


class TestOSLab(unittest.TestCase):
    """Набор тестов для проверки работы с файлами через библиотеку os."""

    def setUp(self):
        """Создаём временную папку для изолированного тестирования."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()

    def tearDown(self):
        """Удаляем временную папку и восстанавливаем исходную директорию."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_file_created(self):
        """Проверяем, что файл создаётся в целевой директории."""
        info = process_files(self.temp_dir)
        self.assertTrue(os.path.exists(info["full_path"]))
        self.assertEqual(os.path.dirname(info["full_path"]), self.temp_dir)

    def test_file_size(self):
        """Проверяем, что размер файла соответствует записанным данным."""
        info = process_files(self.temp_dir)
        with open(info["full_path"], "rb") as f:
            content_bytes = f.read()
        self.assertEqual(info["size"], len(content_bytes))
        self.assertGreater(info["size"], 0)

    def test_metadata_dates(self):
        """Проверяем, что даты изменения и доступа установлены корректно."""
        info = process_files(self.temp_dir)
        now = datetime.now().timestamp()
        self.assertGreater(info["mtime"], 0)
        self.assertGreater(info["atime"], 0)
        self.assertLess(abs(now - info["mtime"]), 10)
        self.assertLess(abs(now - info["atime"]), 10)

    def test_user_returned(self):
        """Проверяем, что возвращается непустое имя пользователя."""
        info = process_files(self.temp_dir)
        self.assertIsInstance(info["user"], str)
        self.assertNotEqual(info["user"], "")

    def test_permissions_changed(self):
        """Проверяем, что права доступа изменились."""
        info = process_files(self.temp_dir)
        if os.name == "nt":
            self.assertFalse(os.access(info["full_path"], os.W_OK) is False)
            with open(info["full_path"], "a", encoding="utf-8") as f:
                f.write("test")
        else:
            self.assertNotEqual(info["old_permissions"], info["new_permissions"])
            self.assertEqual(info["new_permissions"], 0o644)

    def test_directory_change(self):
        """Проверяем, что скрипт переходит в целевую директорию."""
        self.assertNotEqual(os.getcwd(), self.temp_dir)
        info = process_files(self.temp_dir)
        self.assertEqual(os.getcwd(), self.temp_dir)
        self.assertEqual(os.path.dirname(info["full_path"]), self.temp_dir)

    def test_file_exists_check(self):
        """Проверяем, что файл существует после создания."""
        info = process_files(self.temp_dir)
        self.assertTrue(os.path.exists(info["full_path"]))


if __name__ == "__main__":
    unittest.main()
