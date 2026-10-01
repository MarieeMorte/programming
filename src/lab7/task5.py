"""Демонстрация гонки данных при инкременте глобальной переменной в нескольких потоках."""

import threading
import time

COUNTER = 0


def increment(iterations: int) -> None:
    """Увеличивает глобальный счётчик iterations раз с разрывом операции."""
    global COUNTER  # pylint: disable=global-statement
    for _ in range(iterations):
        temp = COUNTER
        time.sleep(0)
        COUNTER = temp + 1


def run_threads(thread_count: int, iterations: int) -> int:
    """Запускает thread_count потоков, каждый выполняет increment(iterations)."""
    global COUNTER  # pylint: disable=global-statement
    COUNTER = 0
    threads = [threading.Thread(target=increment, args=(iterations,)) for _ in range(thread_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return COUNTER


def main() -> None:
    """Демонстрация гонки данных."""
    threads = 10
    iterations = 100000
    expected = threads * iterations
    result = run_threads(threads, iterations)
    print(f"Ожидалось: {expected}, получено: {result}")


if __name__ == "__main__":
    main()
