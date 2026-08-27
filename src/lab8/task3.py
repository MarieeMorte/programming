"""Скрипт для управления системными процессами и переменными окружения."""

import os
import platform

import psutil
from psutil import AccessDenied, NoSuchProcess, TimeoutExpired


def list_processes():
    """Возвращает список всех процессов с PID и именем."""
    return [p.info for p in psutil.process_iter(["pid", "name"]) if p.info]


def get_process_info(pid):
    """Возвращает детальную информацию о процессе."""
    p = psutil.Process(pid)
    mem = p.memory_info()
    return {
        "pid": pid,
        "name": p.name(),
        "status": p.status(),
        "username": p.username(),
        "cpu_percent": p.cpu_percent(interval=0.1),
        "memory_mb": mem.rss // (1024 * 1024),
        "cmdline": " ".join(p.cmdline()),
        "num_threads": p.num_threads(),
        "nice": p.nice() if hasattr(p, "nice") else None,
    }


def kill_process(pid):
    """Завершает процесс."""
    p = psutil.Process(pid)
    p.terminate()
    try:
        p.wait(timeout=3)
    except TimeoutExpired:
        p.kill()
    return True


def show_env_vars():
    """Возвращает переменные окружения."""
    return dict(os.environ)


def add_env_var(key, value):
    """Добавляет переменную окружения."""
    os.environ[key] = value


def set_process_priority(pid, priority):
    """Устанавливает приоритет nice."""
    p = psutil.Process(pid)
    p.nice(priority)
    return True


def system_info():
    """Возвращает информацию о системе."""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": None,
        "swap": None,
    }
    try:
        if os.name == "nt":
            drive = os.path.splitdrive(os.path.abspath(__file__))[0] + "\\"
            usage = psutil.disk_usage(drive)
        else:
            usage = psutil.disk_usage("/")
        info["disk"] = usage._asdict()
    except (PermissionError, OSError):
        pass
    try:
        info["swap"] = psutil.swap_memory()._asdict()
    except (RuntimeError, OSError):
        pass
    return info


def _show_processes():
    for p in list_processes():
        print(f"{p['pid']:5} {p['name']}")


def _show_process_info():
    try:
        pid = int(input("PID: "))
        info = get_process_info(pid)
        for k, v in info.items():
            print(f"{k}: {v}")
    except ValueError:
        print("Ошибка: введите число.")
    except NoSuchProcess:
        print("Процесс не найден.")
    except AccessDenied:
        print("Нет доступа.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Ошибка: {e}")


def _kill_process_interactive():
    try:
        pid = int(input("PID: "))
        kill_process(pid)
        print(f"Процесс {pid} завершён.")
    except ValueError:
        print("Ошибка: введите число.")
    except NoSuchProcess:
        print("Процесс не найден.")
    except AccessDenied:
        print("Недостаточно прав.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Ошибка: {e}")


def _show_env_interactive():
    print("\nТекущие переменные:")
    for k, v in sorted(show_env_vars().items()):
        print(f"{k}={v}")
    add = input("Добавить/изменить? (y/n): ").lower()
    if add == "y":
        key = input("Имя: ").strip()
        if key:
            val = input("Значение: ").strip()
            add_env_var(key, val)
            print(f"Переменная {key} установлена.")


def _set_priority_interactive():
    try:
        pid = int(input("PID: "))
        priority = int(input("nice (-20..19): "))
        set_process_priority(pid, priority)
        print(f"Приоритет {pid} изменён на {priority}.")
    except ValueError:
        print("Ошибка: введите число.")
    except NoSuchProcess:
        print("Процесс не найден.")
    except AccessDenied:
        print("Недостаточно прав.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Ошибка: {e}")


def _show_system_info_interactive():
    info = system_info()
    print(f"\nОС: {info['system']} {info['release']}")
    if info["processor"]:
        print(f"Процессор: {info['processor']}")
    print(f"Ядра: {info['cpu_count']}")
    mem = info["memory"]
    print(
        f"Память: всего {mem['total'] // (1024 ** 3)} ГБ, "
        f"доступно {mem['available'] // (1024 ** 3)} ГБ ({mem['percent']}% использовано)"
    )
    if info["disk"] is not None:
        disk = info["disk"]
        # pylint: disable=unsubscriptable-object
        print(
            f"Диск: всего {disk['total'] // (1024 ** 3)} ГБ, "
            f"свободно {disk['free'] // (1024 ** 3)} ГБ ({disk['percent']}% занято)"
        )
    if info["swap"] is not None:
        swap = info["swap"]
        # pylint: disable=unsubscriptable-object
        print(
            f"Swap: {swap['used'] // (1024 ** 3)} ГБ из "
            f"{swap['total'] // (1024 ** 3)} ГБ ({swap['percent']}%)"
        )


def main():
    """Интерактивное меню."""
    menu = {
        "a": _show_processes,
        "b": _show_process_info,
        "c": _kill_process_interactive,
        "d": _show_env_interactive,
        "e": _set_priority_interactive,
        "f": _show_system_info_interactive,
    }
    while True:
        print("\n" + "=" * 40)
        print("СИСТЕМНЫЙ МЕНЕДЖЕР")
        print("=" * 40)
        print("a) Список процессов")
        print("b) Информация о процессе")
        print("c) Завершить процесс")
        print("d) Переменные окружения")
        print("e) Изменить приоритет")
        print("f) Информация о системе")
        print("g) Выход")
        choice = input("Выберите опцию: ").strip().lower()
        if choice == "g":
            print("Выход.")
            break
        if choice in menu:
            menu[choice]()
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана.")
