"""Модуль для работы с директориями."""

import os
import shutil
from datetime import datetime


def ensure_original_file():
    """Создаёт исходный файл lab_os_file.txt, если его нет."""
    filename = "lab_os_file.txt"
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Исходный файл для задания 2. Создан: {datetime.now()}\n")
    return filename


def print_directory_contents(directory, label=""):
    """Выводит содержимое директории."""
    print(f"{label}Содержимое {directory}:")
    for item in os.listdir(directory):
        print(f"  {item}")


def main():
    """Выполняет все операции задания 2."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Перешли в {script_dir}")

    original = ensure_original_file()

    copy_path = "lab_os_file_copy.txt"
    shutil.copy2(original, copy_path)
    print(f"Создана копия: {copy_path}")

    nested_dir = os.path.join("dir1", "dir2")
    os.makedirs(nested_dir, exist_ok=True)
    moved_copy = os.path.join(nested_dir, "moved_copy.txt")
    shutil.move(copy_path, moved_copy)
    print(f"Копия перемещена и переименована в: {moved_copy}")

    new_file = "new_file.txt"
    with open(new_file, "w", encoding="utf-8") as f:
        f.write("Содержимое нового файла.\n")
    renamed_moved = os.path.join(nested_dir, "renamed_new.txt")
    os.rename(new_file, renamed_moved)
    print(f"Новый файл перемещён и переименован в: {renamed_moved}")

    for name in ["extra1.txt", "extra2.txt"]:
        with open(name, "w", encoding="utf-8") as f:
            f.write(f"Файл {name}\n")
    print("Созданы дополнительные файлы в корне.")

    print_directory_contents(".", "Корневая папка: ")
    print()

    os.chdir(nested_dir)
    print(f"Перешли в {nested_dir}")
    print_directory_contents(".", "Содержимое вложенной папки: ")
    os.chdir(script_dir)
    print("Вернулись в корневую папку.\n")

    empty_dir = "empty_dir"
    os.mkdir(empty_dir)
    print(f"Создана пустая директория: {empty_dir}")
    os.rmdir(empty_dir)
    print(f"Директория {empty_dir} удалена.")

    os.makedirs(os.path.join("nested1", "nested2"), exist_ok=True)
    with open(os.path.join("nested1", "fileA.txt"), "w", encoding="utf-8") as f:
        f.write("Файл в первой вложенной папке.\n")
    with open(os.path.join("nested1", "nested2", "fileB.txt"), "w", encoding="utf-8") as f:
        f.write("Файл в глубокой вложенности.\n")
    print("Созданы вложенные директории nested1/nested2 с файлами.")

    print("\nОбход дерева каталогов")
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith("__")]
        print(f"Папка: {root}")
        if files:
            print("  Файлы:", ", ".join(files))
        else:
            print("  Файлы: (нет)")


if __name__ == "__main__":
    main()
