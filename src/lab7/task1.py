"""Модуль с базовой асинхронной функцией async_print и демонстрацией."""

import asyncio


async def async_print(delay: float, message: str) -> None:
    """Асинхронно ждёт delay секунд, затем выводит message."""
    await asyncio.sleep(delay)
    print(message)


async def main():
    """Демонстрация работы async_print (один вызов)."""
    await async_print(1, "Привет, мир!")


if __name__ == "__main__":
    asyncio.run(main())
