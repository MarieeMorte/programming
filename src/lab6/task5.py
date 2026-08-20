import asyncio
import time


async def func1():
    """Первая асинхронная функция: 3 принта с задержками 1 с и 4 с."""
    print("func1: начало")
    await asyncio.sleep(1)
    print("func1: после 1 с")
    await asyncio.sleep(4)
    print("func1: после 4 с (всего 5 с)")
    return "func1 завершена"


async def func2():
    """Вторая асинхронная функция: 4 принта с задержками 3 с, 1 с, 1 с."""
    print("func2: начало")
    await asyncio.sleep(3)
    print("func2: после 3 с")
    await asyncio.sleep(1)
    print("func2: после 1 с (всего 4 с)")
    await asyncio.sleep(1)
    print("func2: после 1 с (всего 5 с)")
    return "func2 завершена"


async def main():
    """Запуск обеих функций конкурентно."""
    start = time.perf_counter()
    results = await asyncio.gather(func1(), func2())
    elapsed = time.perf_counter() - start
    print(f"\nОбщее время выполнения: {elapsed:.2f} сек.")
    print(f"Результаты: {results}")


if __name__ == "__main__":
    asyncio.run(main())
