"""Демонстрация проблемы гонки данных при работе с общей переменной."""

import threading
import time

COUNTER = 0
LOCK = threading.Lock()


def increment_without_lock(iterations: int) -> None:
    """Увеличивает глобальный счётчик iterations раз без синхронизации."""
    global COUNTER  # pylint: disable=global-statement
    for _ in range(iterations):
        temp = COUNTER
        time.sleep(0)
        COUNTER = temp + 1


def increment_with_lock(iterations: int) -> None:
    """Увеличивает глобальный счётчик iterations раз с использованием блокировки."""
    global COUNTER  # pylint: disable=global-statement
    for _ in range(iterations):
        with LOCK:
            temp = COUNTER
            COUNTER = temp + 1


def run_threads(thread_count: int, iterations: int, use_lock: bool = False) -> int:
    """Запускает указанное количество потоков, каждый выполняет increment."""
    global COUNTER  # pylint: disable=global-statement
    COUNTER = 0

    threads = []
    target = increment_with_lock if use_lock else increment_without_lock

    for _ in range(thread_count):
        t = threading.Thread(target=target, args=(iterations,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return COUNTER


def main():
    """Демонстрация проблемы гонки данных."""
    threads = 10
    iterations = 100000

    print("=== Демонстрация гонки данных ===")
    print(f"Потоков: {threads}, итераций на поток: {iterations}")
    expected = threads * iterations
    print(f"Ожидаемое значение счётчика: {expected}\n")

    result_no_lock = run_threads(threads, iterations, use_lock=False)
    print(f"Результат без блокировки: {result_no_lock}")
    print(f"Потеряно операций: {expected - result_no_lock}")

    result_with_lock = run_threads(threads, iterations, use_lock=True)
    print(f"Результат с блокировкой: {result_with_lock}")
    print(f"Потеряно операций: {expected - result_with_lock}")

    print(
        "\nВывод: без синхронизации счётчик не достигает ожидаемого значения "
        "из-за гонки данных. Блокировка решает проблему."
    )


if __name__ == "__main__":
    main()
