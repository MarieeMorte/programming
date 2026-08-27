"""Скрипт для управления системными процессами."""

import os
import platform
import subprocess


def _run_cmd(cmd, check=False):
    """Выполняет команду и возвращает stdout."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, shell=True, encoding="oem", check=check
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, OSError, ValueError):
        return ""


def list_processes():
    """Возвращает список (pid, name)."""
    output = _run_cmd("tasklist /FO CSV /NH")
    processes = []
    for line in output.splitlines():
        parts = line.strip('"').split('","')
        if len(parts) >= 2:
            try:
                processes.append((int(parts[1]), parts[0]))
            except ValueError:
                continue
    return processes


def get_process_info(pid):
    """Возвращает словарь с информацией о процессе."""
    info = {"pid": pid}
    cmd = (
        f"wmic process where ProcessId={pid} get "
        f"Name,Status,CommandLine,ThreadCount,WorkingSetSize /FORMAT:CSV"
    )
    output = _run_cmd(cmd)
    if output:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].strip('"').split('","')
            if len(parts) >= 5:
                info["name"] = parts[0]
                info["status"] = parts[1]
                info["cmdline"] = parts[2]
                info["num_threads"] = int(parts[3]) if parts[3].isdigit() else 0
                mem_bytes = int(parts[4]) if parts[4].isdigit() else 0
                info["memory_mb"] = mem_bytes // (1024 * 1024)
    info.setdefault("username", "N/A")
    info.setdefault("cpu_percent", 0.0)
    info.setdefault("nice", None)
    return info


def kill_process(pid):
    """Завершает процесс."""
    _run_cmd(f"taskkill /PID {pid} /F", check=True)


def set_process_priority(pid, priority):
    """Устанавливает приоритет."""
    if priority <= -5:
        win_priority = 0
    elif priority <= 5:
        win_priority = 2
    elif priority <= 15:
        win_priority = 3
    else:
        win_priority = 4
    _run_cmd(f"wmic process where ProcessId={pid} call setpriority {win_priority}", check=True)


def system_info():
    """Возвращает информацию о системе (память, диск, swap)."""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "memory": {},
        "disk": {},
        "swap": {},
    }
    output = _run_cmd("wmic os get TotalVisibleMemorySize,FreePhysicalMemory /FORMAT:CSV")
    if output:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].strip('"').split('","')
            if len(parts) >= 2:
                total_kb = int(parts[0]) if parts[0].isdigit() else 0
                free_kb = int(parts[1]) if parts[1].isdigit() else 0
                if total_kb:
                    info["memory"] = {
                        "total": total_kb * 1024,
                        "available": free_kb * 1024,
                        "percent": 100 - (free_kb / total_kb * 100),
                    }
    drive = os.path.splitdrive(os.path.abspath(__file__))[0] + "\\"
    cmd = f"wmic logicaldisk where DeviceID='{drive}' get Size,FreeSpace /FORMAT:CSV"
    output = _run_cmd(cmd)
    if output:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].strip('"').split('","')
            if len(parts) >= 2:
                total = int(parts[0]) if parts[0].isdigit() else 0
                free = int(parts[1]) if parts[1].isdigit() else 0
                if total:
                    info["disk"] = {
                        "total": total,
                        "free": free,
                        "percent": (1 - free / total) * 100,
                    }
    output = _run_cmd("wmic pagefile get AllocatedBaseSize,CurrentUsage /FORMAT:CSV")
    if output:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].strip('"').split('","')
            if len(parts) >= 2:
                total_mb = int(parts[0]) if parts[0].isdigit() else 0
                used_mb = int(parts[1]) if parts[1].isdigit() else 0
                if total_mb:
                    info["swap"] = {
                        "total": total_mb * 1024 * 1024,
                        "used": used_mb * 1024 * 1024,
                        "percent": (used_mb / total_mb) * 100,
                    }
    return info


def _show_processes():
    """Выводит список процессов."""
    for pid, name in list_processes():
        print(f"{pid:5} {name}")


def _show_process_info():
    """Запрашивает PID и выводит детальную информацию."""
    try:
        pid = int(input("PID: "))
        info = get_process_info(pid)
        for k, v in info.items():
            print(f"{k}: {v}")
    except ValueError:
        print("Ошибка: введите число.")
    except (OSError, subprocess.CalledProcessError, KeyError) as e:
        print(f"Ошибка: {e}")


def _kill_process_interactive():
    """Запрашивает PID и завершает процесс."""
    try:
        pid = int(input("PID: "))
        kill_process(pid)
        print(f"Процесс {pid} завершён.")
    except ValueError:
        print("Ошибка: введите число.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Не удалось завершить: {e}")


def _set_priority_interactive():
    """Запрашивает PID и новое значение nice, меняет приоритет."""
    try:
        pid = int(input("PID: "))
        priority = int(input("nice (-20..19): "))
        set_process_priority(pid, priority)
        print(f"Приоритет {pid} изменён.")
    except ValueError:
        print("Ошибка ввода.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Ошибка: {e}")


def _show_env_interactive():
    """Показывает переменные окружения и позволяет добавить новую."""
    for k, v in sorted(os.environ.items()):
        print(f"{k}={v}")
    add = input("Добавить/изменить? (y/n): ").strip().lower()
    if add == "y":
        key = input("Имя: ").strip()
        if key:
            val = input("Значение: ").strip()
            os.environ[key] = val
            print(f"Переменная {key} установлена.")


def _show_system_info_interactive():
    """Выводит информацию о системе (ОС, память, диск, swap)."""
    info = system_info()
    print(f"\nОС: {info['system']} {info['release']}")
    print(f"Процессор: {info['processor']}")
    print(f"Ядра: {info['cpu_count']}")
    mem = info.get("memory", {})
    if mem:
        print(
            f"Память: всего {mem['total'] // (1024 ** 3)} ГБ, "
            f"доступно {mem['available'] // (1024 ** 3)} ГБ ({mem['percent']:.1f}%)"
        )
    disk = info.get("disk", {})
    if disk:
        print(
            f"Диск: всего {disk['total'] // (1024 ** 3)} ГБ, "
            f"свободно {disk['free'] // (1024 ** 3)} ГБ ({disk['percent']:.1f}%)"
        )
    swap = info.get("swap", {})
    if swap:
        print(
            f"Swap: {swap['used'] // (1024 ** 3)} ГБ из "
            f"{swap['total'] // (1024 ** 3)} ГБ ({swap['percent']:.1f}%)"
        )


def main():
    """Главное меню программы."""
    menu = {
        "a": _show_processes,
        "b": _show_process_info,
        "c": _kill_process_interactive,
        "d": _show_env_interactive,
        "e": _set_priority_interactive,
        "f": _show_system_info_interactive,
    }
    while True:
        print("Системный менеджер")
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
