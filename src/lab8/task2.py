"""
Модуль для работы с директориями: копирование, перемещение, переименование,
создание и удаление папок, обход дерева каталогов.
"""

import os
import shutil
from datetime import datetime
from typing import Optional


def ensure_original_file(base_dir: str) -> str:
    """Создаёт исходный файл lab_os_file.txt в base_dir, если его нет."""
    file_path = os.path.join(base_dir, "lab_os_file.txt")
    if not os.path.exists(file_path):
        data = f"Исходный файл для задания 2. Создан: {datetime.now()}\n"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
    return file_path


def copy_and_move_copy(original: str, base_dir: str) -> tuple[str, str]:
    """Копирует исходный файл, создаёт вложенные папки, перемещает копию и переименовывает её."""
    copy_path = os.path.join(base_dir, "lab_os_file_copy.txt")
    shutil.copy2(original, copy_path)
    print(f"Создана копия: {copy_path}")

    nested_dir = os.path.join(base_dir, "dir1", "dir2")
    os.makedirs(nested_dir, exist_ok=True)
    moved_copy = os.path.join(nested_dir, "moved_copy.txt")
    shutil.move(copy_path, moved_copy)
    print(f"Копия перемещена и переименована в: {moved_copy}")
    return nested_dir, moved_copy


def create_and_move_new_file(base_dir: str, nested_dir: str) -> str:
    """Создаёт новый файл и перемещает его с переименованием в nested_dir."""
    new_file = os.path.join(base_dir, "new_file.txt")
    with open(new_file, "w", encoding="utf-8") as f:
        f.write("Содержимое нового файла.\n")
    renamed_moved = os.path.join(nested_dir, "renamed_new.txt")
    os.rename(new_file, renamed_moved)
    print(f"Новый файл перемещён и переименован в: {renamed_moved}")
    return renamed_moved


def create_extra_files(base_dir: str) -> list[str]:
    """Создаёт несколько дополнительных файлов в корневой папке."""
    extra_files = []
    for name in ["extra1.txt", "extra2.txt"]:
        path = os.path.join(base_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Файл {name}\n")
        extra_files.append(path)
    print("Созданы дополнительные файлы в корне.")
    return extra_files


def create_nested_structure(base_dir: str) -> tuple[str, str, str]:
    """Создаёт вложенные директории nested1/nested2 с файлами."""
    deep_dir = os.path.join(base_dir, "nested1", "nested2")
    os.makedirs(deep_dir, exist_ok=True)
    deep_file = os.path.join(deep_dir, "fileB.txt")
    with open(deep_file, "w", encoding="utf-8") as f:
        f.write("Файл в глубокой вложенности.\n")
    shallow_file = os.path.join(base_dir, "nested1", "fileA.txt")
    with open(shallow_file, "w", encoding="utf-8") as f:
        f.write("Файл в первой вложенной папке.\n")
    print("Созданы вложенные директории nested1/nested2 с файлами.")
    return deep_dir, deep_file, shallow_file


def print_directory_contents(directory: str, label: str = ""):
    """Выводит содержимое директории."""
    print(f"{label}Содержимое {directory}:")
    for item in os.listdir(directory):
        print(f"  {item}")


def process_directories(target_dir: Optional[str] = None) -> dict:
    """Выполняет все операции задания 2."""
    if target_dir is None:
        target_dir = os.path.dirname(os.path.abspath(__file__))

    if os.getcwd() != target_dir:
        os.chdir(target_dir)
        print(f"Перешли в рабочую директорию: {target_dir}")

    original = ensure_original_file(target_dir)

    nested_dir, moved_copy = copy_and_move_copy(original, target_dir)

    renamed_moved = create_and_move_new_file(target_dir, nested_dir)

    extra_files = create_extra_files(target_dir)

    print_directory_contents(target_dir, "Корневая папка: ")
    print()

    os.chdir(nested_dir)
    print(f"Перешли в {nested_dir}")
    print_directory_contents(".", "Содержимое вложенной папки: ")
    os.chdir(target_dir)
    print("Вернулись в корневую папку.\n")

    empty_dir = os.path.join(target_dir, "empty_dir")
    os.mkdir(empty_dir)
    print(f"Создана пустая директория: {empty_dir}")
    os.rmdir(empty_dir)
    print(f"Директория {empty_dir} удалена.")

    deep_dir, deep_file, shallow_file = create_nested_structure(target_dir)

    print("\nОбход дерева каталогов")
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not d.startswith("__")]
        print(f"Папка: {root}")
        if files:
            print("  Файлы:", ", ".join(files))
        else:
            print("  Файлы: (нет)")

    return {
        "target_dir": target_dir,
        "original": original,
        "moved_copy": moved_copy,
        "renamed_moved": renamed_moved,
        "extra_files": extra_files,
        "nested_dir": nested_dir,
        "deep_dir": deep_dir,
        "deep_file": deep_file,
        "shallow_file": shallow_file,
    }


def main():
    """Демонстрация работы скрипта."""
    print("Задание 2: работа с директориями\n")
    process_directories()
    print("\nОперации завершены.")


if __name__ == "__main__":
    main()
