"""Интерактивный скрипт для управления системными процессами и переменными окружения."""
# pylint: disable=broad-exception-caught,protected-access

import os
import platform

import psutil  # type: ignore
from psutil import AccessDenied, NoSuchProcess, TimeoutExpired


def list_processes() -> list[dict]:
    """Возвращает список всех запущенных процессов в виде словарей."""
    processes = []
    for proc in psutil.process_iter(["pid", "name", "status", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (NoSuchProcess, AccessDenied):
            continue
    return processes


def format_process_list(processes: list[dict]) -> str:
    """Форматирует список процессов для красивого вывода."""
    if not processes:
        return "Нет доступных процессов."
    lines = ["PID   Name                          Status      CPU%   Memory%", "-" * 60]
    for p in processes:
        lines.append(
            f"{p['pid']:5d} {p['name']:30s} {p['status']:10s} "
            f"{p['cpu_percent']:6.1f} {p['memory_percent']:7.1f}"
        )
    return "\n".join(lines)


def get_process_info(pid: int) -> dict:
    """Возвращает детальную информацию о процессе с заданным PID."""
    proc = psutil.Process(pid)
    info = {
        "pid": pid,
        "name": proc.name(),
        "exe": proc.exe(),
        "cmdline": " ".join(proc.cmdline()),
        "status": proc.status(),
        "username": proc.username(),
        "create_time": proc.create_time(),
        "cpu_percent": proc.cpu_percent(interval=0.1),
        "memory_info": proc.memory_info()._asdict(),
        "connections": len(proc.connections()),
        "num_threads": proc.num_threads(),
        "nice": proc.nice() if hasattr(proc, "nice") else None,
    }
    return info


def format_process_info(info: dict) -> str:
    """Форматирует детальную информацию о процессе для вывода."""
    lines = [
        f"PID: {info['pid']}",
        f"Имя: {info['name']}",
        f"Исполняемый файл: {info['exe']}",
        f"Командная строка: {info['cmdline']}",
        f"Статус: {info['status']}",
        f"Пользователь: {info['username']}",
        f"Время создания: {info['create_time']}",
        f"Использование CPU: {info['cpu_percent']:.1f}%",
        f"Количество потоков: {info['num_threads']}",
        f"Открытых соединений: {info['connections']}",
        f"Nice (приоритет): {info['nice']}",
    ]
    mem = info["memory_info"]
    lines.append("Память:")
    for key, val in mem.items():
        lines.append(f"  {key}: {val}")
    return "\n".join(lines)


def kill_process(pid: int) -> bool:
    """Завершает процесс с заданным PID."""
    proc = psutil.Process(pid)
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except TimeoutExpired:
        proc.kill()
    return True


def show_env_vars() -> dict:
    """Возвращает словарь всех переменных окружения."""
    return dict(os.environ)


def add_env_var(key: str, value: str) -> None:
    """Добавляет или изменяет переменную окружения в текущем процессе."""
    os.environ[key] = value


def set_process_priority(pid: int, priority: int) -> bool:
    """Устанавливает приоритет для процесса."""
    proc = psutil.Process(pid)
    proc.nice(priority)
    return True


def get_disk_usage() -> dict | None:
    """Безопасно возвращает информацию об использовании диска."""
    try:
        if os.name == "nt":
            drive = os.path.splitdrive(os.path.abspath(__file__))[0] + "\\"
            usage = psutil.disk_usage(drive)
        else:
            usage = psutil.disk_usage("/")
        return usage._asdict()
    except (PermissionError, FileNotFoundError, Exception):
        return None


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
        "disk_usage": get_disk_usage(),
        "swap": None,
    }
    try:
        swap = psutil.swap_memory()
        info["swap"] = swap._asdict()
    except (RuntimeError, AttributeError, Exception):
        pass
    return info


def format_system_info(info: dict) -> str:
    """Форматирует системную информацию для вывода."""
    lines = [
        f"Система: {info['system']}",
        f"Имя узла: {info['node']}",
        f"Версия ОС: {info['release']} ({info['version']})",
        f"Архитектура: {info['machine']}",
        f"Процессор: {info['processor']}",
        f"Логические ядра: {info['cpu_count_logical']}",
        f"Физические ядра: {info['cpu_count_physical']}",
    ]
    if info["cpu_freq"]:
        freq = info["cpu_freq"]
        lines.append(
            f"Частота CPU: {freq['current']:.0f} МГц (мин: {freq['min']}, макс: {freq['max']})"
        )
    mem = info["memory"]
    lines.append(f"Общая память: {mem['total']} байт")
    lines.append(f"Доступная память: {mem['available']} байт")
    lines.append(f"Использовано: {mem['used']} байт ({mem['percent']}%)")
    if info["swap"]:
        swap = info["swap"]
        lines.append(
            f"Swap: всего {swap['total']}, использовано {swap['used']} " f"({swap['percent']}%)"
        )
    if info["disk_usage"]:
        disk = info["disk_usage"]
        lines.append(
            f"Использование диска: всего {disk['total']}, свободно {disk['free']} "
            f"({disk['percent']}%)"
        )
    return "\n".join(lines)


def _show_process_list():
    procs = list_processes()
    print(format_process_list(procs))


def _show_process_details():
    try:
        pid = int(input("Введите PID: "))
    except ValueError:
        print("Ошибка: PID должен быть целым числом.")
        return

    try:
        info = get_process_info(pid)
        print(format_process_info(info))
    except NoSuchProcess:
        print(f"Ошибка: процесс с PID {pid} не найден.")
    except AccessDenied:
        print(f"Ошибка: нет прав доступа к процессу {pid}.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


def _kill_process():
    try:
        pid = int(input("Введите PID: "))
    except ValueError:
        print("Ошибка: PID должен быть целым числом.")
        return

    try:
        kill_process(pid)
        print(f"Процесс {pid} успешно завершён.")
    except NoSuchProcess:
        print(f"Ошибка: процесс с PID {pid} не найден.")
    except AccessDenied:
        print(f"Ошибка: недостаточно прав для завершения процесса {pid}.")
    except Exception as e:
        print(f"Ошибка при завершении: {e}")


def _show_env():
    env = show_env_vars()
    for key, value in sorted(env.items()):
        print(f"{key}={value}")


def _add_env():
    key = input("Введите имя переменной: ").strip()
    if not key:
        print("Имя переменной не может быть пустым.")
        return
    value = input("Введите значение: ").strip()
    add_env_var(key, value)
    print(f"Переменная {key} установлена в '{value}'")


def _change_priority():
    try:
        pid = int(input("Введите PID: "))
    except ValueError:
        print("Ошибка: PID должен быть целым числом.")
        return

    try:
        priority = int(
            input("Введите значение nice (обычно -20..19, чем меньше, тем выше приоритет): ")
        )
    except ValueError:
        print("Ошибка: приоритет должен быть целым числом.")
        return

    try:
        set_process_priority(pid, priority)
        print(f"Приоритет процесса {pid} изменён на {priority}.")
    except NoSuchProcess:
        print(f"Ошибка: процесс с PID {pid} не найден.")
    except AccessDenied:
        print(f"Ошибка: недостаточно прав для изменения приоритета процесса {pid}.")
    except Exception as e:
        print(f"Ошибка: {e}")


def _show_system_info():
    info = system_info()
    print(format_system_info(info))


def interactive_menu():
    """Интерактивное меню для управления системой."""
    menu_actions = {
        "a": _show_process_list,
        "b": _show_process_details,
        "c": _kill_process,
        "d": _show_env,
        "e": _add_env,
        "f": _change_priority,
        "g": _show_system_info,
    }

    while True:
        print("\n" + "=" * 50)
        print("СИСТЕМНЫЙ МЕНЕДЖЕР")
        print("=" * 50)
        print("a) Список всех запущенных процессов")
        print("b) Детальная информация о процессе по PID")
        print("c) Завершить процесс по PID")
        print("d) Показать переменные окружения")
        print("e) Добавить/изменить переменную окружения")
        print("f) Изменить приоритет процесса")
        print("g) Показать информацию о системе")
        print("h) Выход")
        choice = input("Выберите опцию (a-h): ").strip().lower()

        if choice == "h":
            print("Выход.")
            break
        if choice in menu_actions:
            menu_actions[choice]()
        else:
            print("Неверный выбор. Пожалуйста, выберите a-h.")


def main():
    """Точка входа."""
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")


if __name__ == "__main__":
    main()
