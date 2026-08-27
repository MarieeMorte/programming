"""Unit-тесты для задания 2."""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from src.lab8.task2 import main


class TestDirectories(unittest.TestCase):
    """Тесты для скрипта task2.py с изоляцией через моки."""

    def setUp(self):
        """Создаём временную папку и подменяем __file__, чтобы main работал в ней."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        # Патчим __file__ в модуле task2, чтобы main считал, что он лежит в temp_dir
        self.patcher = patch("src.lab8.task2.__file__", os.path.join(self.temp_dir, "task2.py"))
        self.mock_file = self.patcher.start()

    def tearDown(self):
        """Останавливаем патч, возвращаемся в исходную директорию и удаляем временную папку."""
        self.patcher.stop()
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_copy_exists(self):
        """Проверяет, что исходный файл и его перемещённая копия существуют."""
        main()
        original = os.path.join(self.temp_dir, "lab_os_file.txt")
        moved_copy = os.path.join(self.temp_dir, "dir1", "dir2", "moved_copy.txt")
        self.assertTrue(os.path.exists(original))
        self.assertTrue(os.path.exists(moved_copy))

    def test_move_and_rename_copy(self):
        """Проверяет, что копия перемещена в нужную папку и переименована."""
        main()
        moved_copy = os.path.join(self.temp_dir, "dir1", "dir2", "moved_copy.txt")
        self.assertTrue(os.path.exists(moved_copy))
        self.assertEqual(os.path.basename(moved_copy), "moved_copy.txt")
        self.assertEqual(os.path.dirname(moved_copy), os.path.join(self.temp_dir, "dir1", "dir2"))

    def test_move_and_rename_new_file(self):
        """Проверяет, что новый файл перемещён и переименован одной командой os.rename."""
        main()
        renamed_new = os.path.join(self.temp_dir, "dir1", "dir2", "renamed_new.txt")
        self.assertTrue(os.path.exists(renamed_new))
        self.assertEqual(os.path.basename(renamed_new), "renamed_new.txt")
        self.assertEqual(os.path.dirname(renamed_new), os.path.join(self.temp_dir, "dir1", "dir2"))
        # Проверяем, что исходный файл new_file.txt не остался в корне
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "new_file.txt")))

    def test_extra_files_created(self):
        """Проверяет, что дополнительные файлы созданы в корневой папке."""
        main()
        extra1 = os.path.join(self.temp_dir, "extra1.txt")
        extra2 = os.path.join(self.temp_dir, "extra2.txt")
        self.assertTrue(os.path.exists(extra1))
        self.assertTrue(os.path.exists(extra2))
        # Проверяем содержимое (необязательно, но можно)
        with open(extra1, "r", encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), "Файл extra1.txt")
        with open(extra2, "r", encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), "Файл extra2.txt")

    def test_empty_dir_created_and_deleted(self):
        """Проверяет, что пустая директория была создана и удалена."""
        main()
        empty_dir = os.path.join(self.temp_dir, "empty_dir")
        self.assertFalse(os.path.exists(empty_dir))

    def test_nested_dirs_and_files(self):
        """Проверяет создание вложенных директорий nested1/nested2 и файлов в них."""
        main()
        deep_dir = os.path.join(self.temp_dir, "nested1", "nested2")
        deep_file = os.path.join(deep_dir, "fileB.txt")
        shallow_file = os.path.join(self.temp_dir, "nested1", "fileA.txt")
        self.assertTrue(os.path.exists(deep_dir))
        self.assertTrue(os.path.exists(deep_file))
        self.assertTrue(os.path.exists(shallow_file))
        # Проверяем содержимое
        with open(deep_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), "Файл в глубокой вложенности.")
        with open(shallow_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read().strip(), "Файл в первой вложенной папке.")

    def test_walk_contains_all(self):
        """Проверяет, что обход дерева выполняется без ошибок."""
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")

    def test_working_directory_changes(self):
        """Проверяет, что после всех операций мы вернулись в корневую папку."""
        main()
        self.assertEqual(os.getcwd(), self.temp_dir)


if __name__ == "__main__":
    unittest.main()
