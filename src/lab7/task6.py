"""Решение проблемы гонки данных с помощью threading.Lock."""

import threading

COUNTER = 0
LOCK = threading.Lock()


def increment_with_lock(iterations: int) -> None:
    """Увеличивает глобальный счётчик iterations раз с использованием блокировки."""
    global COUNTER  # pylint: disable=global-statement
    for _ in range(iterations):
        with LOCK:
            temp = COUNTER
            COUNTER = temp + 1


def run_threads_safe(thread_count: int, iterations: int) -> int:
    """Запускает указанное количество потоков с использованием блокировки."""
    global COUNTER  # pylint: disable=global-statement
    COUNTER = 0

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=increment_with_lock, args=(iterations,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return COUNTER


def main():
    """Демонстрация корректной работы с блокировкой."""
    threads = 10
    iterations = 100000
    expected = threads * iterations

    print("=== Решение гонки данных с помощью блокировки ===")
    print(f"Потоков: {threads}, итераций на поток: {iterations}")
    print(f"Ожидаемое значение счётчика: {expected}")

    result = run_threads_safe(threads, iterations)
    print(f"Результат с блокировкой: {result}")
    print(f"Потеряно операций: {expected - result}")

    if result == expected:
        print("Проблема гонки данных устранена!")
    else:
        print("Что-то пошло не так.")


if __name__ == "__main__":
    main()
