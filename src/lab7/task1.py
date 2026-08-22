"""Модуль с базовой асинхронной функцией async_print и демонстрацией."""

import asyncio


async def async_print(delay: float, message: str) -> None:
    """Асинхронно ждёт delay секунд, затем выводит message."""
    await asyncio.sleep(delay)
    print(message)


async def main():
    """Демонстрация конкурентного выполнения async_print."""
    tasks = [
        async_print(2, "Сообщение через 2 с"),
        async_print(1, "Сообщение через 1 с"),
        async_print(3, "Сообщение через 3 с"),
    ]
    start = asyncio.get_event_loop().time()
    await asyncio.gather(*tasks)
    elapsed = asyncio.get_event_loop().time() - start
    print(f"Общее время выполнения: {elapsed} с (ожидаем ~3 с)")


if __name__ == "__main__":
    asyncio.run(main())
