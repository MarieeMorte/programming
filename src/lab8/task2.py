"""Модуль для работы с директориями."""

import os
from datetime import datetime
from typing import List, Tuple


def change_to_script_directory() -> str:
    """Переходит в директорию, где находится скрипт, и возвращает её путь."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Перешли в {script_dir}")
    return script_dir


def ensure_original_file(filename: str = "lab_os_file.txt") -> str:
    """Создаёт исходный файл, если его нет, и возвращает его имя."""
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Исходный файл для задания 2. Создан: {datetime.now()}\n")
    return filename


def copy_file(src: str, dst: str) -> bool:
    """Копирует файл вручную (чтение/запись). Возвращает True при успехе."""
    try:
        with open(src, "rb") as f_in:
            data = f_in.read()
        with open(dst, "wb") as f_out:
            f_out.write(data)  # type: ignore
        print(f"Создана копия: {dst}")
        return True
    except OSError as e:
        print(f"Ошибка копирования {src} -> {dst}: {e}")
        return False


def move_and_rename_file(src: str, dst_dir: str, new_name: str) -> bool:
    """
    Перемещает файл в директорию dst_dir и переименовывает его в new_name.
    Создаёт промежуточные директории при необходимости.
    """
    try:
        os.makedirs(dst_dir, exist_ok=True)
        dst_path = os.path.join(dst_dir, new_name)
        os.rename(src, dst_path)
        print(f"Файл перемещён и переименован в: {dst_path}")
        return True
    except OSError as e:
        print(f"Ошибка перемещения/переименования {src} -> {dst_dir}/{new_name}: {e}")
        return False


def create_and_move_file(content: str, src_name: str, dst_dir: str, new_name: str) -> bool:
    """
    Создаёт файл с именем src_name, записывает content,
    затем перемещает его в dst_dir и переименовывает в new_name одной командой os.rename.
    """
    try:
        with open(src_name, "w", encoding="utf-8") as f:
            f.write(content)
        os.makedirs(dst_dir, exist_ok=True)
        dst_path = os.path.join(dst_dir, new_name)
        os.rename(src_name, dst_path)
        print(f"Новый файл перемещён и переименован в: {dst_path}")
        return True
    except OSError as e:
        print(f"Ошибка при создании/перемещении файла: {e}")
        return False


def create_extra_files(filenames: List[str]) -> None:
    """Создаёт несколько файлов в текущей директории."""
    for name in filenames:
        try:
            with open(name, "w", encoding="utf-8") as f:
                f.write(f"Файл {name}\n")
        except OSError as e:
            print(f"Не удалось создать {name}: {e}")


def print_directory_contents(directory: str, label: str = "") -> None:
    """Выводит содержимое директории с обработкой ошибок."""
    try:
        items = os.listdir(directory)
        print(f"{label}Содержимое {directory}:")
        for item in items:
            print(f"  {item}")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Не удалось прочитать {directory}: {e}")


def manage_empty_dir(dirname: str) -> None:
    """Создаёт пустую директорию и сразу удаляет её."""
    try:
        os.mkdir(dirname)
        print(f"Создана пустая директория: {dirname}")
        os.rmdir(dirname)
        print(f"Директория {dirname} удалена.")
    except OSError as e:
        print(f"Ошибка при работе с {dirname}: {e}")


def create_nested_dirs_with_files(base_path: str, file_pairs: List[Tuple[str, str]]) -> None:
    """
    Создаёт вложенные директории и файлы.
    file_pairs: список кортежей (относительный_путь_к_файлу, содержимое)
    """
    try:
        os.makedirs(base_path, exist_ok=True)
        for rel_path, content in file_pairs:
            full_path = os.path.join(base_path, rel_path)
            parent = os.path.dirname(full_path)
            if parent and not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"Созданы вложенные директории {base_path} с файлами.")
    except OSError as e:
        print(f"Ошибка создания вложенных директорий: {e}")


def walk_and_print() -> None:
    """Обходит текущую директорию и выводит папки и файлы."""
    print("\nОбход дерева каталогов")
    try:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if not d.startswith("__")]
            print(f"Папка: {root}")
            if files:
                print("  Файлы:", ", ".join(files))
            else:
                print("  Файлы: (нет)")
    except OSError as e:
        print(f"Ошибка при обходе дерева: {e}")


def main() -> None:
    """Выполняет все операции задания 2."""
    script_dir = change_to_script_directory()

    original = ensure_original_file()
    copy_path = "lab_os_file_copy.txt"
    copy_file(original, copy_path)

    nested_dir = os.path.join("dir1", "dir2")
    move_and_rename_file(copy_path, nested_dir, "moved_copy.txt")

    create_and_move_file(
        content="Содержимое нового файла.\n",
        src_name="new_file.txt",
        dst_dir=nested_dir,
        new_name="renamed_new.txt",
    )

    create_extra_files(["extra1.txt", "extra2.txt"])
    print_directory_contents(".", "Корневая папка: ")
    print()

    os.chdir(nested_dir)
    print(f"Перешли в {nested_dir}")
    print_directory_contents(".", "Содержимое вложенной папки: ")
    os.chdir(script_dir)
    print("Вернулись в корневую папку.\n")

    manage_empty_dir("empty_dir")

    create_nested_dirs_with_files(
        "nested1",
        [
            ("fileA.txt", "Файл в первой вложенной папке.\n"),
            (os.path.join("nested2", "fileB.txt"), "Файл в глубокой вложенности.\n"),
        ],
    )

    walk_and_print()


if __name__ == "__main__":
    main()
