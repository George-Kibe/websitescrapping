"""
Save IMDb's Top 250 movies chart to an Excel workbook.

Usage:
    python imdb_top_movies.py            # writes "IMDB Movie Ratings.xlsx"

IMDb renders the visible chart with JavaScript, but the page also embeds
the full list as JSON-LD structured data, which is what this script reads.
"""

import json

import openpyxl
from bs4 import BeautifulSoup

from common import get_soup

URL = "https://www.imdb.com/chart/top/"
OUTPUT = "IMDB Movie Ratings.xlsx"
HEADER = ["Rank", "Title", "Rating", "Votes", "Genre", "URL"]


def parse_movies(soup: BeautifulSoup) -> list[list]:
    """Return one row per movie from the page's JSON-LD ItemList."""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except json.JSONDecodeError:
            continue
        if data.get("@type") != "ItemList":
            continue

        rows = []
        for rank, element in enumerate(data.get("itemListElement", []), start=1):
            movie = element.get("item", {})
            rating = movie.get("aggregateRating", {})
            rows.append(
                [
                    element.get("position", rank),
                    movie.get("alternateName") or movie.get("name"),
                    rating.get("ratingValue"),
                    rating.get("ratingCount"),
                    movie.get("genre"),
                    movie.get("url"),
                ]
            )
        return rows
    return []


def main() -> None:
    movies = parse_movies(get_soup(URL))
    if not movies:
        raise SystemExit("Could not find the movie list; IMDb may have changed its page.")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Top Rated Movies IMDB"
    sheet.append(HEADER)
    for row in movies:
        sheet.append(row)
    workbook.save(OUTPUT)
    print(f"Saved {len(movies)} movies to {OUTPUT}")


if __name__ == "__main__":
    main()
