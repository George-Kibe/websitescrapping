"""
Scrape the UMG Gaming XP leaderboard.

Usage:
    python umg_leaderboard.py            # prints and writes leaderboard.csv
"""

from bs4 import BeautifulSoup

from common import get_soup, text_of, write_csv

URL = "https://umggaming.com/leaderboards"


def parse_leaderboard(soup: BeautifulSoup) -> list[tuple[str, str, str]]:
    """Return (place, username, xp) for each leaderboard row."""
    rows = []
    for tr in soup.select("table#leaderboard-table tbody tr"):
        cells = tr.find_all("td")
        if len(cells) < 4:
            continue
        # The username cell holds an avatar link followed by the name link.
        links = cells[1].find_all("a")
        username = text_of(links[-1] if links else cells[1])
        rows.append((text_of(cells[0]), username, text_of(cells[3])))
    return rows


def main() -> None:
    rows = parse_leaderboard(get_soup(URL))
    for place, username, xp in rows:
        print(f"{place:>4}  {username:<30} {xp}")
    count = write_csv("leaderboard.csv", ["Place", "Username", "XP"], rows)
    print(f"\nSaved {count} rows to leaderboard.csv")


if __name__ == "__main__":
    main()
