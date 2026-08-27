"""Модуль для работы с файлами с использованием библиотеки os."""

import os
from datetime import datetime


def main():
    """Создаёт файл, выводит его свойства и меняет права доступа."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Перешли в {os.getcwd()}")

    filename = "lab_os_file.txt"
    data = f"Тестовые данные. Время: {datetime.now()}\nВторая строка."

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    if not os.path.exists(filename):
        raise RuntimeError("Файл не создан")

    print(f"Размер: {os.path.getsize(filename)} байт")
    print(f"Изменён: {datetime.fromtimestamp(os.path.getmtime(filename))}")
    print(f"Доступ: {datetime.fromtimestamp(os.path.getatime(filename))}")

    try:
        user = os.getlogin()
    except OSError:
        user = os.environ.get("USER") or os.environ.get("USERNAME") or "неизвестно"
    print(f"Пользователь: {user}")

    old_perm = os.stat(filename).st_mode & 0o777
    print(f"Старые права: {oct(old_perm)}")
    os.chmod(filename, 0o644)
    new_perm = os.stat(filename).st_mode & 0o777
    print(f"Новые права: {oct(new_perm)}")


if __name__ == "__main__":
    main()
