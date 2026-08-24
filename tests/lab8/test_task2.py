"""Unit-тесты для задания 2 (работа с директориями)."""

import os
import shutil
import tempfile
import unittest

from src.lab8.task2 import process_directories


class TestDirectories(unittest.TestCase):
    """Набор тестов для проверки операций с директориями."""

    def setUp(self):
        """Создаём временную папку для изолированного тестирования."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()

    def tearDown(self):
        """Удаляем временную папку и восстанавливаем исходную директорию."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_copy_exists(self):
        """Проверяет, что исходный файл и его перемещённая копия существуют."""
        info = process_directories(self.temp_dir)
        self.assertTrue(os.path.exists(info["original"]))
        self.assertTrue(os.path.exists(info["moved_copy"]))

    def test_move_and_rename_copy(self):
        """Проверяет, что копия перемещена в нужную папку и переименована."""
        info = process_directories(self.temp_dir)
        self.assertTrue(os.path.exists(info["moved_copy"]))
        self.assertEqual(os.path.basename(info["moved_copy"]), "moved_copy.txt")
        self.assertEqual(os.path.dirname(info["moved_copy"]), info["nested_dir"])

    def test_move_and_rename_new_file(self):
        """Проверяет, что новый файл перемещён и переименован одной командой."""
        info = process_directories(self.temp_dir)
        self.assertTrue(os.path.exists(info["renamed_moved"]))
        self.assertEqual(os.path.basename(info["renamed_moved"]), "renamed_new.txt")
        self.assertEqual(os.path.dirname(info["renamed_moved"]), info["nested_dir"])

    def test_extra_files_created(self):
        """Проверяет, что дополнительные файлы созданы в корневой папке."""
        info = process_directories(self.temp_dir)
        for path in info["extra_files"]:
            self.assertTrue(os.path.exists(path))
            self.assertEqual(os.path.dirname(path), info["target_dir"])

    def test_empty_dir_created_and_deleted(self):
        """Проверяет, что пустая директория была создана и удалена."""
        info = process_directories(self.temp_dir)
        empty_dir = os.path.join(info["target_dir"], "empty_dir")
        self.assertFalse(os.path.exists(empty_dir))

    def test_nested_dirs_and_files(self):
        """Проверяет создание вложенных директорий и файлов в них."""
        info = process_directories(self.temp_dir)
        self.assertTrue(os.path.exists(info["deep_dir"]))
        self.assertTrue(os.path.exists(info["deep_file"]))
        self.assertTrue(os.path.exists(info["shallow_file"]))

    def test_walk_contains_all(self):
        """Проверяет, что функция обхода выполняется без ошибок."""
        process_directories(self.temp_dir)

    def test_working_directory_changes(self):
        """Проверяет, что после всех операций мы вернулись в корневую папку."""
        info = process_directories(self.temp_dir)
        self.assertEqual(os.getcwd(), info["target_dir"])


if __name__ == "__main__":
    unittest.main()
