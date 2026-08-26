"""Модуль с базовой асинхронной функцией async_print и демонстрацией."""

import asyncio


async def async_print(delay: float, message: str) -> None:
    """Асинхронно ждёт delay секунд, затем выводит message."""
    await asyncio.sleep(delay)
    print(message)


async def main():
    """Демонстрация конкурентного выполнения async_print."""
    loop = asyncio.get_running_loop()

    tasks = [
        async_print(2, "Сообщение через 2 с"),
        async_print(1, "Сообщение через 1 с"),
        async_print(3, "Сообщение через 3 с"),
    ]

    start = loop.time()
    await asyncio.gather(*tasks)
    elapsed = loop.time() - start

    print(f"Общее время выполнения: {elapsed:.3f} с")


if __name__ == "__main__":
    asyncio.run(main())
