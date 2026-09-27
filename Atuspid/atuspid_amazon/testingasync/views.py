"""An async Django view that fetches several pages concurrently with aiohttp."""

import asyncio

import aiohttp
from bs4 import BeautifulSoup
from django.http import JsonResponse

BOOK_PAGES = [f"https://books.toscrape.com/catalogue/page-{n}.html" for n in range(1, 5)]


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


def book_titles(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    return [a["title"] for a in soup.select("article.product_pod h3 a[title]")]


async def books(request):
    """Fetch all pages at once (not one after another) and return the book titles."""
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        pages = await asyncio.gather(*(fetch(session, url) for url in BOOK_PAGES))
    return JsonResponse({url: book_titles(html) for url, html in zip(BOOK_PAGES, pages, strict=True)})
