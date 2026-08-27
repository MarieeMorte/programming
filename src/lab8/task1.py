"""Модуль для работы с файлами с использованием библиотеки os."""

import os
from datetime import datetime


def process_files(target_dir: str = None) -> dict:
    """Выполняет все действия задания 1."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()

    if target_dir is None:
        target_dir = script_dir

    if current_dir != target_dir:
        os.chdir(target_dir)
        print(f"Перешли в директорию: {os.getcwd()}")

    filename = "lab_os_file.txt"
    data = f"Тестовые данные. Время создания: {datetime.now()}\n"
    data += "Строка для проверки размера."

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    if not os.path.exists(filename):
        raise RuntimeError("Файл не создан")

    size = os.path.getsize(filename)
    mtime = os.path.getmtime(filename)
    atime = os.path.getatime(filename)

    try:
        user = os.getlogin()
    except OSError:
        user = os.environ.get("USER") or os.environ.get("USERNAME") or "неизвестно"

    stat_info = os.stat(filename)
    permissions = stat_info.st_mode & 0o777

    new_permissions = 0o644
    os.chmod(filename, new_permissions)

    new_stat = os.stat(filename)
    new_perm = new_stat.st_mode & 0o777

    return {
        "filename": filename,
        "size": size,
        "mtime": mtime,
        "atime": atime,
        "user": user,
        "old_permissions": permissions,
        "new_permissions": new_perm,
        "full_path": os.path.abspath(filename),
    }


def main():
    """Демонстрация работы скрипта."""
    print("Работа с библиотекой os")
    info = process_files()
    print(f"Файл: {info['filename']}")
    print(f"Размер: {info['size']} байт")
    print(f"Изменён: {datetime.fromtimestamp(info['mtime'])}")
    print(f"Доступ: {datetime.fromtimestamp(info['atime'])}")
    print(f"Пользователь: {info['user']}")
    print(f"Старые права: {oct(info['old_permissions'])}")
    print(f"Новые права: {oct(info['new_permissions'])}")
    print(f"Полный путь: {info['full_path']}")


if __name__ == "__main__":
    main()
