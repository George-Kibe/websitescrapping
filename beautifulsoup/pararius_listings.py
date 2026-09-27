"""
Scrape rental listings from pararius.com into a CSV file.

Usage:
    python pararius_listings.py                     # Amsterdam, first page
    python pararius_listings.py --city rotterdam --pages 3
"""

import argparse
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from common import get_soup, text_of, write_csv

BASE_URL = "https://www.pararius.com"


def parse_listings(soup: BeautifulSoup) -> list[dict[str, str]]:
    listings = []
    for item in soup.select("section.listing-search-item"):
        title_link = item.select_one("a.listing-search-item__link--title")
        listings.append(
            {
                "title": text_of(title_link),
                "location": text_of(
                    item.select_one(".listing-search-item__sub-title, .listing-search-item__location")
                ),
                "price": text_of(item.select_one(".listing-search-item__price")),
                "area": text_of(item.select_one(".illustrated-features__item--surface-area")),
                "link": urljoin(BASE_URL, title_link["href"]) if title_link else "",
            }
        )
    return listings


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape rental listings from pararius.com.")
    parser.add_argument("--city", default="amsterdam")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--output", default="housing.csv")
    args = parser.parse_args()

    listings = []
    with requests.Session() as session:
        for page in range(1, args.pages + 1):
            url = f"{BASE_URL}/apartments/{args.city}/page-{page}"
            page_listings = parse_listings(get_soup(url, session))
            print(f"Page {page}: {len(page_listings)} listings")
            if not page_listings:
                break
            listings.extend(page_listings)
            time.sleep(1)  # be polite between pages

    fields = ["title", "location", "price", "area", "link"]
    count = write_csv(args.output, fields, ([row[f] for f in fields] for row in listings))
    print(f"Saved {count} listings to {args.output}")


if __name__ == "__main__":
    main()
