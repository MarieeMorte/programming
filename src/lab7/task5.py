"""Демонстрация гонки данных при инкременте глобальной переменной в нескольких потоках."""

import threading
import time

COUNTER = 0


def increment(iterations: int) -> None:
    """
    Увеличивает глобальный счётчик iterations раз, разбивая операцию
    на чтение, задержку и запись для гарантированного проявления гонки.
    """
    global COUNTER  # pylint: disable=global-statement
    for _ in range(iterations):
        temp = COUNTER
        time.sleep(0)
        COUNTER = temp + 1


def main() -> None:
    """Запускает 10 потоков, каждый выполняет 100 000 инкрементов без синхронизации."""
    threads_count = 10
    iterations = 100000
    expected = threads_count * iterations

    threads = [threading.Thread(target=increment, args=(iterations,)) for _ in range(threads_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Ожидалось: {expected}, получено: {COUNTER}")


if __name__ == "__main__":
    main()
