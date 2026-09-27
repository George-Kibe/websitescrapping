"""Offline tests for the page parsers, using small hand-written HTML samples."""

import json
import unittest

from bs4 import BeautifulSoup

from contact_extractor import extract_contacts
from imdb_top_movies import parse_movies
from pararius_listings import parse_listings
from table_scraper import extract_tables
from umg_leaderboard import parse_leaderboard


def soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


class ContactExtractorTests(unittest.TestCase):
    def test_finds_phones_and_emails_in_text_and_links(self):
        page = soup(
            """
            <p>Call 0722 123 456 or email info@example.co.ke</p>
            <a href="mailto:sales@example.com?subject=Hi">Sales</a>
            <a href="tel:+254700000000">Phone</a>
            """
        )
        phones, emails = extract_contacts(page)
        self.assertIn("0722 123 456", phones)
        self.assertIn("+254700000000", phones)
        self.assertEqual(emails, ["info@example.co.ke", "sales@example.com"])


class TableScraperTests(unittest.TestCase):
    def test_extracts_rows_and_skips_empty_tables(self):
        page = soup(
            """
            <table><tr><th>Name</th><th>Price</th></tr>
                   <tr class="special"><td>A</td><td>1</td></tr>
                   <tr><td>B</td><td>2</td></tr></table>
            <table></table>
            """
        )
        self.assertEqual(extract_tables(page), [[["Name", "Price"], ["A", "1"], ["B", "2"]]])
        self.assertEqual(extract_tables(page, row_selector="tr.special"), [[["A", "1"]]])


class LeaderboardTests(unittest.TestCase):
    def test_parses_rows(self):
        page = soup(
            """
            <table id="leaderboard-table"><tbody>
              <tr><td>1</td><td><a href="#"><img></a><a href="#">Player One</a></td><td>x</td><td>9,000</td></tr>
              <tr><td>short row</td></tr>
            </tbody></table>
            """
        )
        self.assertEqual(parse_leaderboard(page), [("1", "Player One", "9,000")])


class ParariusTests(unittest.TestCase):
    def test_parses_listing(self):
        page = soup(
            """
            <section class="listing-search-item">
              <a class="listing-search-item__link--title" href="/apartment-for-rent/x">Flat X</a>
              <div class="listing-search-item__sub-title">1011 AB Amsterdam</div>
              <div class="listing-search-item__price">EUR 2,000 per month</div>
              <li class="illustrated-features__item--surface-area">60 m2</li>
            </section>
            <section class="listing-search-item"></section>
            """
        )
        listings = parse_listings(page)
        self.assertEqual(listings[0]["title"], "Flat X")
        self.assertEqual(listings[0]["link"], "https://www.pararius.com/apartment-for-rent/x")
        self.assertEqual(listings[0]["area"], "60 m2")
        self.assertEqual(listings[1]["title"], "")  # missing fields don't crash


class ImdbTests(unittest.TestCase):
    def test_reads_json_ld_item_list(self):
        data = {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "position": 1,
                    "item": {
                        "name": "Movie",
                        "url": "https://www.imdb.com/title/tt1/",
                        "genre": "Drama",
                        "aggregateRating": {"ratingValue": 9.3, "ratingCount": 100},
                    },
                }
            ],
        }
        page = soup(
            '<script type="application/ld+json">{"@type": "Organization"}</script>'
            f'<script type="application/ld+json">{json.dumps(data)}</script>'
        )
        self.assertEqual(
            parse_movies(page), [[1, "Movie", 9.3, 100, "Drama", "https://www.imdb.com/title/tt1/"]]
        )

    def test_returns_empty_list_without_data(self):
        self.assertEqual(parse_movies(soup("<p>nothing</p>")), [])


if __name__ == "__main__":
    unittest.main()
