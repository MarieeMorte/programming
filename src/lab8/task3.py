"""
Скрипт для управления системными процессами и переменными окружения.
Содержит отдельные функции для каждой операции.
"""

import os
import platform

import psutil
from psutil import AccessDenied, NoSuchProcess, TimeoutExpired


def list_processes() -> list[dict]:
    """Возвращает список всех процессов с PID и именем."""
    processes = []
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            processes.append(proc.info)
        except (NoSuchProcess, AccessDenied):
            continue
    return processes


def get_process_info(pid: int) -> dict:
    """Возвращает детальную информацию о процессе."""
    p = psutil.Process(pid)
    info = {
        "pid": pid,  # используем переданный PID
        "name": p.name(),
        "exe": p.exe(),
        "cmdline": " ".join(p.cmdline()),
        "status": p.status(),
        "username": p.username(),
        "create_time": p.create_time(),
        "cpu_percent": p.cpu_percent(interval=0.1),
        "memory_info": p.memory_info()._asdict(),
        "num_threads": p.num_threads(),
        "nice": p.nice() if hasattr(p, "nice") else None,
    }
    return info


def kill_process(pid: int) -> bool:
    """Завершает процесс с заданным PID."""
    p = psutil.Process(pid)
    p.terminate()
    try:
        p.wait(timeout=3)
    except TimeoutExpired:
        p.kill()
    return True


def show_env_vars() -> dict:
    """Возвращает словарь всех переменных окружения."""
    return dict(os.environ)


def add_env_var(key: str, value: str) -> None:
    """Добавляет или изменяет переменную окружения."""
    os.environ[key] = value


def set_process_priority(pid: int, priority: int) -> bool:
    """Устанавливает приоритет (nice) для процесса."""
    p = psutil.Process(pid)
    p.nice(priority)
    return True


def system_info() -> dict:
    """Возвращает информацию о системе."""
    info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count_logical": psutil.cpu_count(),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "memory": psutil.virtual_memory()._asdict(),
        "disk_usage": None,
        "swap": None,
    }
    try:
        if os.name == "nt":
            drive = os.path.splitdrive(os.path.abspath(__file__))[0] + "\\"
            usage = psutil.disk_usage(drive)
        else:
            usage = psutil.disk_usage("/")
        info["disk_usage"] = usage._asdict()
    except (PermissionError, OSError):
        pass

    try:
        swap = psutil.swap_memory()
        info["swap"] = swap._asdict()
    except (RuntimeError, OSError):
        pass

    return info


# --- Вспомогательные функции для меню ---
def _show_processes():
    for p in list_processes():
        print(f"{p['pid']:5} {p['name']}")


def _show_process_info():
    try:
        pid = int(input("Введите PID: "))
        info = get_process_info(pid)
        for k, v in info.items():
            print(f"{k}: {v}")
    except ValueError:
        print("Ошибка: PID должен быть числом.")
    except NoSuchProcess:
        print("Процесс не найден.")
    except AccessDenied:
        print("Нет доступа.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Ошибка: {e}")


def _kill_process():
    try:
        pid = int(input("Введите PID: "))
        kill_process(pid)
        print(f"Процесс {pid} завершён.")
    except ValueError:
        print("Ошибка: PID должен быть числом.")
    except NoSuchProcess:
        print("Процесс не найден.")
    except AccessDenied:
        print("Недостаточно прав.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Ошибка: {e}")


def _show_env():
    print("\nТекущие переменные окружения:")
    for k, v in sorted(show_env_vars().items()):
        print(f"{k}={v}")
    add = input("\nДобавить/изменить переменную? (y/n): ").lower()
    if add == "y":
        key = input("Имя переменной: ").strip()
        if key:
            val = input("Значение: ").strip()
            add_env_var(key, val)
            print(f"Переменная {key} установлена.")


def _set_priority():
    try:
        pid = int(input("Введите PID: "))
        priority = int(input("Значение nice (-20..19, меньше = выше приоритет): "))
        set_process_priority(pid, priority)
        print(f"Приоритет процесса {pid} изменён на {priority}.")
    except ValueError:
        print("Ошибка: введите целое число.")
    except NoSuchProcess:
        print("Процесс не найден.")
    except AccessDenied:
        print("Недостаточно прав.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Ошибка: {e}")


def _show_system_info():
    info = system_info()
    print(f"\nСистема: {info['system']} {info['release']}")
    print(f"Узел: {info['node']}")
    print(f"Процессор: {info['processor'] or 'неизвестно'}")
    print(
        f"Ядра: {info['cpu_count_logical']} логических, " f"{info['cpu_count_physical']} физических"
    )
    mem = info["memory"]
    print(
        f"Память: всего {mem['total'] // (1024 ** 3)} ГБ, "
        f"свободно {mem['available'] // (1024 ** 3)} ГБ "
        f"({mem['percent']}% использовано)"
    )
    disk = info.get("disk_usage")
    if disk is not None:
        print(
            f"Диск: всего {disk['total'] // (1024 ** 3)} ГБ, "
            f"свободно {disk['free'] // (1024 ** 3)} ГБ "
            f"({disk['percent']}% занято)"
        )
    swap = info.get("swap")
    if swap is not None:
        print(
            f"Swap: {swap['used'] // (1024 ** 3)} ГБ из "
            f"{swap['total'] // (1024 ** 3)} ГБ ({swap['percent']}%)"
        )


def main():
    """Интерактивное меню."""
    while True:
        print("\n" + "=" * 40)
        print("СИСТЕМНЫЙ МЕНЕДЖЕР")
        print("=" * 40)
        print("a) Список процессов")
        print("b) Информация о процессе")
        print("c) Завершить процесс")
        print("d) Переменные окружения (показать/добавить)")
        print("e) Изменить приоритет процесса")
        print("f) Информация о системе")
        print("g) Выход")
        choice = input("Выберите опцию: ").strip().lower()

        if choice == "g":
            print("Выход.")
            break
        if choice == "a":
            _show_processes()
        elif choice == "b":
            _show_process_info()
        elif choice == "c":
            _kill_process()
        elif choice == "d":
            _show_env()
        elif choice == "e":
            _set_priority()
        elif choice == "f":
            _show_system_info()
        else:
            print("Неверный выбор. Введите a-g.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана.")
