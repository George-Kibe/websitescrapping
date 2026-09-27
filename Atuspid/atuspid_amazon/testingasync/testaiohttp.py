"""
Download several pages concurrently with aiohttp, outside Django.

Usage:
    python testaiohttp.py
"""

import asyncio

import aiohttp
from bs4 import BeautifulSoup

URLS = [f"https://books.toscrape.com/catalogue/page-{n}.html" for n in range(1, 5)]


async def get_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def get_all(urls: list[str]) -> list[str]:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        return await asyncio.gather(*(get_page(session, url) for url in urls))


def main() -> None:
    for url, html in zip(URLS, asyncio.run(get_all(URLS)), strict=True):
        soup = BeautifulSoup(html, "lxml")
        pager = soup.select_one("li.current")
        print(url, "->", pager.get_text(strip=True) if pager else "no pager found")


if __name__ == "__main__":
    main()
