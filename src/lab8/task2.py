"""Модуль для работы с директориями."""

import os
from datetime import datetime


def ensure_original_file():
    """Создаёт исходный файл lab_os_file.txt, если его нет."""
    filename = "lab_os_file.txt"
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Исходный файл для задания 2. Создан: {datetime.now()}\n")
    return filename


def print_directory_contents(directory, label=""):
    """Выводит содержимое директории с обработкой ошибок."""
    try:
        items = os.listdir(directory)
        print(f"{label}Содержимое {directory}:")
        for item in items:
            print(f"  {item}")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Не удалось прочитать {directory}: {e}")


def copy_file(src, dst):
    """Копирует файл вручную (чтение/запись). Возвращает True при успехе."""
    try:
        with open(src, "rb") as f_in:
            data = f_in.read()
        with open(dst, "wb") as f_out:
            f_out.write(data)
        return True
    except OSError as e:
        print(f"Ошибка копирования {src} -> {dst}: {e}")
        return False


def safe_rename(src, dst):
    """Переименовывает/перемещает файл, обрабатывает ошибки."""
    try:
        os.rename(src, dst)
        return True
    except OSError as e:
        print(f"Ошибка переименования/перемещения {src} -> {dst}: {e}")
        return False


def create_extra_files(filenames):
    """Создаёт несколько файлов в текущей директории."""
    for name in filenames:
        try:
            with open(name, "w", encoding="utf-8") as f:
                f.write(f"Файл {name}\n")
        except OSError as e:
            print(f"Не удалось создать {name}: {e}")


def prepare_nested_and_move():
    """Выполняет пункты 1-3."""
    original = ensure_original_file()
    copy_path = "lab_os_file_copy.txt"
    if copy_file(original, copy_path):
        print(f"Создана копия: {copy_path}")

    nested_dir = os.path.join("dir1", "dir2")
    os.makedirs(nested_dir, exist_ok=True)
    moved_copy = os.path.join(nested_dir, "moved_copy.txt")
    if safe_rename(copy_path, moved_copy):
        print(f"Копия перемещена и переименована в: {moved_copy}")

    new_file = "new_file.txt"
    with open(new_file, "w", encoding="utf-8") as f:
        f.write("Содержимое нового файла.\n")
    renamed_moved = os.path.join(nested_dir, "renamed_new.txt")
    if safe_rename(new_file, renamed_moved):
        print(f"Новый файл перемещён и переименован в: {renamed_moved}")

    return nested_dir


def walk_and_print():
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


def main():
    """Выполняет все операции задания 2."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Перешли в {script_dir}")

    nested_dir = prepare_nested_and_move()

    create_extra_files(["extra1.txt", "extra2.txt"])
    print_directory_contents(".", "Корневая папка: ")
    print()

    os.chdir(nested_dir)
    print(f"Перешли в {nested_dir}")
    print_directory_contents(".", "Содержимое вложенной папки: ")
    os.chdir(script_dir)
    print("Вернулись в корневую папку.\n")

    empty_dir = "empty_dir"
    try:
        os.mkdir(empty_dir)
        print(f"Создана пустая директория: {empty_dir}")
        os.rmdir(empty_dir)
        print(f"Директория {empty_dir} удалена.")
    except OSError as e:
        print(f"Ошибка при работе с {empty_dir}: {e}")

    nested_path = os.path.join("nested1", "nested2")
    try:
        os.makedirs(nested_path, exist_ok=True)
        with open(os.path.join("nested1", "fileA.txt"), "w", encoding="utf-8") as f:
            f.write("Файл в первой вложенной папке.\n")
        with open(os.path.join(nested_path, "fileB.txt"), "w", encoding="utf-8") as f:
            f.write("Файл в глубокой вложенности.\n")
        print("Созданы вложенные директории nested1/nested2 с файлами.")
    except OSError as e:
        print(f"Ошибка создания вложенных директорий: {e}")

    walk_and_print()


if __name__ == "__main__":
    main()
