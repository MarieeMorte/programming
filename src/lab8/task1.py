"""Модуль для работы с файлами с использованием библиотеки os."""

import os
from datetime import datetime


def change_to_script_directory():
    """Переходит в директорию, где находится скрипт."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Перешли в {os.getcwd()}")
    return script_dir


def create_file_with_data(filepath: str) -> None:
    """Создаёт файл и записывает в него данные. Проверяет, что файл действительно создан."""
    data = f"Тестовые данные. Время: {datetime.now()}\nВторая строка."
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)

    if not os.path.exists(filepath):
        raise RuntimeError("Файл не создан")


def print_file_info(filepath: str) -> None:
    """Выводит размер файла в байтах, дату последнего изменения и дату последнего доступа."""
    print(f"Размер: {os.path.getsize(filepath)} байт")
    print(f"Изменён: {datetime.fromtimestamp(os.path.getmtime(filepath))}")
    print(f"Доступ: {datetime.fromtimestamp(os.path.getatime(filepath))}")


def print_current_user() -> None:
    """Выводит имя текущего пользователя."""
    try:
        user = os.getlogin()
    except OSError:
        user = os.environ.get("USER") or os.environ.get("USERNAME") or "неизвестно"
    print(f"Пользователь: {user}")


def change_file_permissions(filepath: str) -> None:
    """Показывает текущие права доступа, меняет их на 0o644 и выводит новые права."""
    old_perm = os.stat(filepath).st_mode & 0o777
    print(f"Старые права: {oct(old_perm)}")

    try:
        os.chmod(filepath, 0o644)
        new_perm = os.stat(filepath).st_mode & 0o777
        print(f"Новые права: {oct(new_perm)}")
    except PermissionError as e:
        print(f"Не удалось сменить права: {e}")


def main():
    """Основная функция: последовательно выполняет все пункты задания."""
    script_dir = change_to_script_directory()

    filename = "lab_os_file.txt"
    filepath = os.path.join(script_dir, filename)

    create_file_with_data(filepath)

    print_file_info(filepath)

    print_current_user()

    change_file_permissions(filepath)


if __name__ == "__main__":
    main()
