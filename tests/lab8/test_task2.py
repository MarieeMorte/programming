"""Unit-тесты для задания 2."""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from src.lab8.task2 import (
    change_to_script_directory,
    copy_file,
    create_and_move_file,
    create_extra_files,
    create_nested_dirs_with_files,
    ensure_original_file,
    main,
    manage_empty_dir,
    move_and_rename_file,
    print_directory_contents,
    walk_and_print,
)


# pylint: disable=too-many-public-methods
class TestTask2Functions(unittest.TestCase):
    """Тесты для отдельных функций task2.py."""

    def setUp(self):
        """Создаём временную директорию и исходный файл."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        self.original_file = os.path.join(self.temp_dir, "lab_os_file.txt")
        with open(self.original_file, "w", encoding="utf-8") as f:
            f.write("Original content for tests\n")
        self.dst_file = os.path.join(self.temp_dir, "copy.txt")

    def tearDown(self):
        """Возвращаемся в исходную директорию и удаляем временную."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_change_to_script_directory(self):
        """Переход в директорию скрипта."""
        with patch("src.lab8.task2.__file__", os.path.join(self.temp_dir, "task2.py")):
            script_dir = change_to_script_directory()
            self.assertEqual(script_dir, self.temp_dir)
            self.assertEqual(os.getcwd(), self.temp_dir)

    def test_change_to_script_directory_already_there(self):
        """Если уже в нужной директории, переход не происходит."""
        os.chdir(self.temp_dir)
        with patch("src.lab8.task2.__file__", os.path.join(self.temp_dir, "task2.py")):
            script_dir = change_to_script_directory()
            self.assertEqual(script_dir, self.temp_dir)
            self.assertEqual(os.getcwd(), self.temp_dir)

    def test_ensure_original_file_creates_if_missing(self):
        """Если файла нет, он создаётся."""
        os.remove(self.original_file)
        filename = ensure_original_file("lab_os_file.txt")
        self.assertEqual(filename, "lab_os_file.txt")
        self.assertTrue(os.path.exists(self.original_file))
        with open(self.original_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Исходный файл для задания 2", content)

    def test_ensure_original_file_does_not_overwrite(self):
        """Если файл уже есть, он не перезаписывается."""
        with open(self.original_file, "r", encoding="utf-8") as f:
            original_content = f.read()
        ensure_original_file("lab_os_file.txt")
        with open(self.original_file, "r", encoding="utf-8") as f:
            new_content = f.read()
        self.assertEqual(original_content, new_content)

    def test_copy_file_success(self):
        """Успешное копирование файла."""
        result = copy_file(self.original_file, self.dst_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.dst_file))
        with open(self.dst_file, "rb") as f:
            copied_data = f.read()
        with open(self.original_file, "rb") as f:
            original_data = f.read()
        self.assertEqual(copied_data, original_data)

    def test_copy_file_failure(self):
        """Ошибка при копировании (например, исходный файл не существует)."""
        with patch("builtins.print") as mock_print:
            result = copy_file("nonexistent.txt", self.dst_file)
            self.assertFalse(result)
            mock_print.assert_called_once()
            self.assertIn("Ошибка копирования", mock_print.call_args[0][0])

    def test_move_and_rename_file_success(self):
        """Перемещение и переименование с созданием папок."""
        src = self.original_file
        dst_dir = os.path.join("sub", "dir")
        new_name = "moved.txt"
        result = move_and_rename_file(src, dst_dir, new_name)
        self.assertTrue(result)
        expected_path = os.path.join(self.temp_dir, dst_dir, new_name)
        self.assertTrue(os.path.exists(expected_path))
        self.assertFalse(os.path.exists(src))
        with open(expected_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "Original content for tests\n")

    def test_move_and_rename_file_failure(self):
        """Ошибка при перемещении (например, исходный файл не существует)."""
        with patch("builtins.print") as mock_print:
            result = move_and_rename_file("nonexistent.txt", "sub", "new.txt")
            self.assertFalse(result)
            mock_print.assert_called_once()
            self.assertIn("Ошибка перемещения", mock_print.call_args[0][0])

    def test_create_and_move_file_success(self):
        """Создание файла и перемещение/переименование одной командой."""
        content = "Test content"
        src_name = "temp.txt"
        dst_dir = os.path.join("sub", "dir2")
        new_name = "final.txt"
        result = create_and_move_file(content, src_name, dst_dir, new_name)
        self.assertTrue(result)
        expected_path = os.path.join(self.temp_dir, dst_dir, new_name)
        self.assertTrue(os.path.exists(expected_path))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, src_name)))
        with open(expected_path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), content)

    def test_create_and_move_file_failure(self):
        """Ошибка при создании или перемещении."""
        with patch("os.rename", side_effect=OSError("Permission denied")):
            with patch("builtins.print") as mock_print:
                result = create_and_move_file("content", "src.txt", "dst", "new.txt")
                self.assertFalse(result)
                mock_print.assert_called_once()
                self.assertIn("Ошибка при создании/перемещении", mock_print.call_args[0][0])

    def test_create_extra_files(self):
        """Создание нескольких файлов."""
        filenames = ["a.txt", "b.txt"]
        create_extra_files(filenames)
        for name in filenames:
            path = os.path.join(self.temp_dir, name)
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read().strip(), f"Файл {name}")

    def test_create_extra_files_error(self):
        """Ошибка при создании файла (например, некорректное имя)."""
        with patch("builtins.open", side_effect=OSError("Invalid name")):
            with patch("builtins.print") as mock_print:
                create_extra_files(["bad:name.txt"])
                mock_print.assert_called_once()
                self.assertIn("Не удалось создать", mock_print.call_args[0][0])

    def test_print_directory_contents(self):
        """Вывод содержимого директории."""
        os.makedirs("subdir")
        with open("file1.txt", "w", encoding="utf-8") as f:
            f.write("data")
        with open("file2.txt", "w", encoding="utf-8") as f:
            f.write("data")
        with patch("builtins.print") as mock_print:
            print_directory_contents(".", "Label: ")
            calls = [call[0][0] for call in mock_print.call_args_list if call[0]]
            self.assertTrue(any("Label: Содержимое ." in s for s in calls))
            self.assertTrue(any("file1.txt" in s for s in calls))
            self.assertTrue(any("file2.txt" in s for s in calls))
            self.assertTrue(any("subdir" in s for s in calls))

    def test_print_directory_contents_error(self):
        """Ошибка при чтении директории."""
        with patch("os.listdir", side_effect=PermissionError("Access denied")):
            with patch("builtins.print") as mock_print:
                print_directory_contents(".")
                mock_print.assert_called_once()
                self.assertIn("Не удалось прочитать", mock_print.call_args[0][0])

    def test_manage_empty_dir_success(self):
        """Создание и удаление пустой директории."""
        dirname = "empty_test"
        manage_empty_dir(dirname)
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, dirname)))

    def test_manage_empty_dir_failure(self):
        """Ошибка при создании (например, уже существует)."""
        dirname = "existing"
        os.mkdir(dirname)
        with patch("builtins.print") as mock_print:
            manage_empty_dir(dirname)
            mock_print.assert_called_once()
            self.assertIn("Ошибка при работе с", mock_print.call_args[0][0])

    def test_create_nested_dirs_with_files(self):
        """Создание вложенных директорий и файлов."""
        base = "nested"
        file_pairs = [
            ("fileA.txt", "Content A"),
            (os.path.join("sub", "fileB.txt"), "Content B"),
        ]
        create_nested_dirs_with_files(base, file_pairs)
        file_a = os.path.join(self.temp_dir, base, "fileA.txt")
        file_b = os.path.join(self.temp_dir, base, "sub", "fileB.txt")
        self.assertTrue(os.path.exists(file_a))
        self.assertTrue(os.path.exists(file_b))
        with open(file_a, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Content A")
        with open(file_b, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Content B")

    def test_create_nested_dirs_with_files_error(self):
        """Ошибка при создании."""
        with patch("os.makedirs", side_effect=OSError("Cannot create")):
            with patch("builtins.print") as mock_print:
                create_nested_dirs_with_files("base", [("a.txt", "data")])
                mock_print.assert_called_once()
                self.assertIn("Ошибка создания вложенных директорий", mock_print.call_args[0][0])

    def test_walk_and_print(self):
        """Обход дерева без ошибок."""
        os.remove(self.original_file)
        os.makedirs(os.path.join("a", "b"))
        with open("root.txt", "w", encoding="utf-8") as f:
            f.write("")
        with open(os.path.join("a", "a.txt"), "w", encoding="utf-8") as f:
            f.write("")
        with patch("builtins.print") as mock_print:
            walk_and_print()
            all_output = " ".join(
                " ".join(str(arg) for arg in call[0]) for call in mock_print.call_args_list
            )
            self.assertIn("Папка: .", all_output)
            self.assertIn("root.txt", all_output)

    def test_walk_and_print_error(self):
        """Ошибка при обходе."""
        with patch("os.walk", side_effect=OSError("Access denied")):
            with patch("builtins.print") as mock_print:
                walk_and_print()
                self.assertEqual(mock_print.call_count, 2)
                second_call_args = mock_print.call_args_list[1][0][0]
                self.assertIn("Ошибка при обходе дерева", second_call_args)

    def test_main_integration(self):
        """Полный прогон main во временной директории."""
        with patch("src.lab8.task2.__file__", os.path.join(self.temp_dir, "task2.py")):
            with patch("builtins.print"):
                main()
        self.assertTrue(os.path.exists(self.original_file))
        moved_copy = os.path.join(self.temp_dir, "dir1", "dir2", "moved_copy.txt")
        self.assertTrue(os.path.exists(moved_copy))
        renamed_new = os.path.join(self.temp_dir, "dir1", "dir2", "renamed_new.txt")
        self.assertTrue(os.path.exists(renamed_new))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "extra1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "extra2.txt")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "empty_dir")))
        file_a = os.path.join(self.temp_dir, "nested1", "fileA.txt")
        file_b = os.path.join(self.temp_dir, "nested1", "nested2", "fileB.txt")
        self.assertTrue(os.path.exists(file_a))
        self.assertTrue(os.path.exists(file_b))
        self.assertEqual(os.getcwd(), self.temp_dir)


if __name__ == "__main__":
    unittest.main()
