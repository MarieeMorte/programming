"""Модуль для демонстрации синхронного и потокового выполнения."""

import threading
import time

print_lock = threading.Lock()


def print_message(message: str, delay: float) -> None:
    """Печатает сообщение после указанной задержки."""
    time.sleep(delay)
    with print_lock:
        print(message)


def run_sequential(messages: list[str], delay: float) -> float:
    """Запускает print_message последовательно для каждого сообщения."""
    start = time.perf_counter()
    for msg in messages:
        print_message(msg, delay)
    total = time.perf_counter() - start
    print(f"Последовательное выполнение: {total:.3f} с")
    return total


def run_threaded(messages: list[str], delay: float) -> float:
    """Запускает print_message в отдельных потоках для каждого сообщения."""
    threads = []
    for msg in messages:
        thread = threading.Thread(target=print_message, args=(msg, delay))
        threads.append(thread)
        thread.start()

    start = time.perf_counter()
    for thread in threads:
        thread.join()
    total = time.perf_counter() - start
    print(f"Потоковое выполнение: {total:.3f} с")
    return total


def main():
    """Демонстрация сравнения."""
    messages = ["Сообщение 1", "Сообщение 2", "Сообщение 3"]
    delay = 2.0

    print("Сравнение последовательного и потокового выполнения\n")
    seq_time = run_sequential(messages, delay)
    thr_time = run_threaded(messages, delay)

    print(f"\nРазница: {seq_time - thr_time:.3f} с")


if __name__ == "__main__":
    main()
