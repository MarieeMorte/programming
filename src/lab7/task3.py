"""Сравнение синхронных и асинхронных HTTP-запросов с разными задержками."""

import asyncio
import time

import aiohttp
import requests
from aiohttp import ClientError
from requests.exceptions import RequestException

URLS = [
    "https://httpbin.org/get",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/5",
]


def sync_requests() -> tuple[dict[str, float], float]:
    """Выполняет запросы синхронно."""
    print("Синхронный режим")
    times = {}
    start_total = time.perf_counter()

    for url in URLS:
        start = time.perf_counter()
        try:
            response = requests.get(url, timeout=10)
            elapsed = time.perf_counter() - start
            times[url] = elapsed
            print(f"Ответ от {url}: {elapsed:.3f} с (статус {response.status_code})")
        except RequestException as e:
            elapsed = time.perf_counter() - start
            times[url] = elapsed
            print(f"Ошибка при запросе к {url}: {e} (затрачено {elapsed:.3f} с)")

    total = time.perf_counter() - start_total
    print(f"Общее время: {total:.3f} с\n")
    return times, total


async def fetch_url(session: aiohttp.ClientSession, url: str) -> tuple[str, float]:
    """Асинхронно выполняет GET-запрос к одному URL."""
    start = time.perf_counter()
    try:
        async with session.get(url, timeout=10) as response:
            await response.text()
            elapsed = time.perf_counter() - start
            print(f"Ответ от {url}: {elapsed:.3f} с (статус {response.status})")
            return url, elapsed
    except (ClientError, asyncio.TimeoutError) as e:
        elapsed = time.perf_counter() - start
        print(f"Ошибка при запросе к {url}: {e} (затрачено {elapsed:.3f} с)")
        return url, elapsed


async def async_requests() -> tuple[dict[str, float], float]:
    """Выполняет запросы асинхронно (конкурентно)."""
    print("Асинхронный режим")
    start_total = time.perf_counter()
    times = {}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)
        for url, elapsed in results:
            times[url] = elapsed

    total = time.perf_counter() - start_total
    print(f"Общее время: {total:.3f} с\n")
    return times, total


async def main():
    """Демонстрация сравнения."""
    sync_requests()
    await async_requests()


if __name__ == "__main__":
    asyncio.run(main())
