"""Shared helpers for the BeautifulSoup scripts."""

import csv
from collections.abc import Iterable, Sequence
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Many sites reject the default python-requests User-Agent.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 30  # seconds


def get_soup(url: str, session: requests.Session | None = None) -> BeautifulSoup:
    """Download a page and parse it, raising on HTTP errors."""
    response = (session or requests).get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def text_of(element) -> str:
    """Stripped text of a BeautifulSoup element, or "" when it is missing."""
    return element.get_text(" ", strip=True) if element else ""


def write_csv(path: str | Path, header: Sequence[str], rows: Iterable[Sequence]) -> int:
    """Write rows to a CSV file and return how many were written."""
    count = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
            count += 1
    return count
