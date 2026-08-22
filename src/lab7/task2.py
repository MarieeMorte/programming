"""Модуль с функцией для конкурентного запуска трёх задач async_print."""

import asyncio

from src.lab7.task1 import async_print


async def run_multiple() -> list[str]:
    """Запускает три задачи async_print с задержками 2, 1, 3 секунды."""
    messages = [
        ("Через 2 секунды", 2),
        ("Через 1 секунду", 1),
        ("Через 3 секунды", 3),
    ]
    tasks = [async_print(delay, msg) for msg, delay in messages]
    await asyncio.gather(*tasks)
    return [msg for msg, _ in messages]


async def main():
    """Демонстрация работы."""
    start = asyncio.get_event_loop().time()
    await run_multiple()
    elapsed = asyncio.get_event_loop().time() - start
    print(f"Общее время выполнения: {elapsed:.2f} с (ожидаем ~3 с)")


if __name__ == "__main__":
    asyncio.run(main())
