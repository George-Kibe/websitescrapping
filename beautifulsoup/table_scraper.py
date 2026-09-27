"""
Save the HTML tables on a page as CSV files.

Usage:
    python table_scraper.py https://comparables.co.ke/r_comparables/
    python table_scraper.py URL --selector "div.special_table table" --rows tr.special

Each matching table is written to table_1.csv, table_2.csv, ...
"""

import argparse

from bs4 import BeautifulSoup, Tag

from common import get_soup, write_csv


def table_rows(table: Tag, row_selector: str = "tr") -> list[list[str]]:
    """Cell text for each row of a table (header and data cells)."""
    rows = []
    for tr in table.select(row_selector):
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    return rows


def extract_tables(soup: BeautifulSoup, selector: str = "table", row_selector: str = "tr") -> list[list[list[str]]]:
    return [rows for table in soup.select(selector) if (rows := table_rows(table, row_selector))]


def main() -> None:
    parser = argparse.ArgumentParser(description="Save the HTML tables on a page as CSV files.")
    parser.add_argument("url", nargs="?", default="https://comparables.co.ke/r_comparables/")
    parser.add_argument("--selector", default="table", help="CSS selector for the tables (default: table)")
    parser.add_argument("--rows", default="tr", help="CSS selector for rows within a table (default: tr)")
    args = parser.parse_args()

    tables = extract_tables(get_soup(args.url), args.selector, args.rows)
    if not tables:
        print("No tables found.")
    for index, rows in enumerate(tables, start=1):
        path = f"table_{index}.csv"
        write_csv(path, rows[0], rows[1:])
        print(f"Saved {len(rows) - 1} rows to {path}")


if __name__ == "__main__":
    main()
