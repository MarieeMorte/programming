"""Скрипт для управления системными процессами и переменными окружения."""

import os
import platform
import subprocess
from typing import Any, Dict, List, Tuple


def change_to_script_directory() -> None:
    """Переходит в директорию, где находится скрипт, используя os."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)
        print(f"Перешли в {script_dir}")


def _run_cmd(cmd: str, check: bool = False) -> str:
    """Выполняет команду в shell и возвращает stdout."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            encoding="oem",
            check=check,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, OSError, ValueError):
        return ""


def list_processes() -> List[Tuple[int, str]]:
    """Возвращает список кортежей (PID, имя_процесса)."""
    output = _run_cmd("tasklist /FO CSV /NH")
    processes = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        parts = line.split('","')
        if len(parts) >= 2:
            try:
                pid = int(parts[1])
                name = parts[0]
                processes.append((pid, name))
            except ValueError:
                continue
    return processes


def get_process_info(pid: int) -> Dict[str, Any]:
    """Возвращает словарь с информацией о процессе."""
    info: Dict[str, Any] = {"pid": pid}
    cmd = (
        f"wmic process where ProcessId={pid} get "
        f"Name,Status,CommandLine,ThreadCount,WorkingSetSize /FORMAT:LIST"
    )
    output = _run_cmd(cmd)
    if output:
        for line in output.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key == "Name":
                info["name"] = value or "N/A"
            elif key == "Status":
                info["status"] = value or "N/A"
            elif key == "CommandLine":
                info["cmdline"] = value
            elif key == "ThreadCount":
                info["num_threads"] = int(value) if value.isdigit() else 0
            elif key == "WorkingSetSize":
                mem_bytes = int(value) if value.isdigit() else 0
                info["memory_mb"] = mem_bytes // (1024 * 1024)
    info.setdefault("name", "N/A")
    info.setdefault("status", "N/A")
    info.setdefault("cmdline", "")
    info.setdefault("num_threads", 0)
    info.setdefault("memory_mb", 0)
    return info


def kill_process(pid: int) -> None:
    """Завершает процесс с указанным PID."""
    _run_cmd(f"taskkill /PID {pid} /F", check=True)


def set_process_priority(pid: int, priority_class: int) -> None:
    """Устанавливает класс приоритета процесса (0–5) через PowerShell."""
    if priority_class < 0 or priority_class > 5:
        raise ValueError("Класс приоритета должен быть от 0 до 5")

    class_map = {
        0: "Idle",
        1: "BelowNormal",
        2: "Normal",
        3: "AboveNormal",
        4: "High",
        5: "RealTime",
    }
    class_name = class_map[priority_class]
    cmd = (
        f'powershell -Command "'
        f"(Get-Process -Id {pid}).PriorityClass = "
        f'[System.Diagnostics.ProcessPriorityClass]::{class_name}"'
    )
    _run_cmd(cmd, check=True)


def _get_memory_info() -> Dict[str, Any]:
    """Возвращает информацию о физической памяти."""
    output = _run_cmd("wmic os get TotalVisibleMemorySize,FreePhysicalMemory /FORMAT:CSV")
    if output:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].strip('"').split('","')
            if len(parts) >= 2:
                total_kb = int(parts[0]) if parts[0].isdigit() else 0
                free_kb = int(parts[1]) if parts[1].isdigit() else 0
                if total_kb:
                    return {
                        "total": total_kb * 1024,
                        "available": free_kb * 1024,
                        "percent": 100 - (free_kb / total_kb * 100),
                    }
    return {}


def _get_disk_info() -> Dict[str, Any]:
    """Возвращает информацию о диске, на котором находится скрипт."""
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
                    return {
                        "total": total,
                        "free": free,
                        "percent": (1 - free / total) * 100,
                    }
    return {}


def _get_swap_info() -> Dict[str, Any]:
    """Возвращает информацию о файле подкачки."""
    output = _run_cmd("wmic pagefile get AllocatedBaseSize,CurrentUsage /FORMAT:CSV")
    if output:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].strip('"').split('","')
            if len(parts) >= 2:
                total_mb = int(parts[0]) if parts[0].isdigit() else 0
                used_mb = int(parts[1]) if parts[1].isdigit() else 0
                if total_mb:
                    return {
                        "total": total_mb * 1024 * 1024,
                        "used": used_mb * 1024 * 1024,
                        "percent": (used_mb / total_mb) * 100,
                    }
    return {}


def system_info() -> Dict[str, Any]:
    """Возвращает общую информацию о системе."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "processor": platform.processor() or "Unknown",
        "cpu_count": os.cpu_count() or 0,
        "memory": _get_memory_info(),
        "disk": _get_disk_info(),
        "swap": _get_swap_info(),
    }


def _show_processes() -> None:
    """Выводит список всех процессов."""
    for pid, name in list_processes():
        print(f"{pid:5} {name}")


def _show_process_info() -> None:
    """Запрашивает PID и выводит детальную информацию о процессе."""
    try:
        pid = int(input("PID: "))
        info = get_process_info(pid)
        for k, v in info.items():
            print(f"{k}: {v}")
    except ValueError:
        print("Ошибка: введите число.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Ошибка: {e}")


def _kill_process_interactive() -> None:
    """Запрашивает PID и завершает процесс."""
    try:
        pid = int(input("PID: "))
        kill_process(pid)
        print(f"Процесс {pid} завершён.")
    except ValueError:
        print("Ошибка: введите число.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Не удалось завершить: {e}")


def _set_priority_interactive() -> None:
    """Запрашивает PID и класс приоритета (0–4)."""
    try:
        pid = int(input("PID: "))
        print("Классы приоритета:")
        print("0 – IDLE")
        print("1 – BELOW NORMAL")
        print("2 – NORMAL")
        print("3 – ABOVE NORMAL")
        print("4 – HIGH")
        print("5 – REALTIME (требует прав администратора)")
        priority_class = int(input("Класс (0–5): "))
        set_process_priority(pid, priority_class)
        print(f"Приоритет {pid} изменён.")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Ошибка: {e}")


def _show_env_interactive() -> None:
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


def _show_system_info_interactive() -> None:
    """Выводит информацию о системе."""
    info = system_info()
    print(f"\nОС: {info['system']} {info['release']}")
    print(f"Процессор: {info['processor']}")
    print(f"Ядра: {info['cpu_count']}")

    mem = info.get("memory", {})
    if mem:
        total_gb = mem["total"] // (1024**3)
        avail_gb = mem["available"] // (1024**3)
        print(f"Память: всего {total_gb} ГБ, доступно {avail_gb} ГБ ({mem['percent']:.1f}%)")

    disk = info.get("disk", {})
    if disk:
        total_gb = disk["total"] // (1024**3)
        free_gb = disk["free"] // (1024**3)
        print(f"Диск: всего {total_gb} ГБ, свободно {free_gb} ГБ ({disk['percent']:.1f}%)")

    swap = info.get("swap", {})
    if swap:
        used_gb = swap["used"] // (1024**3)
        total_gb = swap["total"] // (1024**3)
        print(f"Swap: {used_gb} ГБ из {total_gb} ГБ ({swap['percent']:.1f}%)")


def main() -> None:
    """Главное меню программы."""
    change_to_script_directory()
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
        print("Системный менеджер")
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
