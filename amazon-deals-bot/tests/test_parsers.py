"""Offline tests for the Amazon page parsers, using small hand-written HTML samples."""

import unittest
from unittest import mock

from bs4 import BeautifulSoup

from amazon_deals import (
    Deal,
    TelegramSender,
    coupon_url,
    next_page_url,
    parse_coupons,
    parse_daily_deals,
    parse_search_results,
)


def soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


class ParserTests(unittest.TestCase):
    def test_coupons(self):
        page = soup(
            """
            <div class="a-section coupon" data-promoid="ABC123">
              <div class="a-section coupon-description">Laptop stand</div>
              <img class="a-dynamic-image coupon-image" src="https://img/1.jpg">
              <span class="a-size-medium a-color-success a-text-bold">Save 15%</span>
            </div>
            <div class="coupon" data-promoid="NOIMG"><div class="coupon-description">x</div></div>
            """
        )
        deals = parse_coupons(page)
        self.assertEqual(len(deals), 1)
        self.assertEqual(deals[0].link, "https://www.amazon.com/promotion/psp/ABC123")
        self.assertIn("Coupon: 15%", deals[0].details)

    def test_daily_deals(self):
        page = soup(
            """
            <div class="DealGridItem-module__dealItemContent_newhash">
              <a href="/dp/B0001">link</a><img src="https://img/2.jpg">
              <div class="DealContent-module__truncate_otherhash">Headphones</div>
              <span class="a-price-whole">49</span>
            </div>
            """
        )
        [deal] = parse_daily_deals(page)
        self.assertEqual(deal.link, "https://www.amazon.com/dp/B0001")
        self.assertIn("Price: 49", deal.details)
        self.assertIn("Offer expired", deal.details)

    def test_search_results_and_pagination(self):
        page = soup(
            """
            <div data-component-type="s-search-result">
              <h2><a href="/dp/B0002"><span>Monitor</span></a></h2>
              <img class="s-image" src="https://img/3.jpg">
              <span class="a-price"><span class="a-offscreen">$99.00</span></span>
              <span class="a-price a-text-price"><span class="a-offscreen">$129.00</span></span>
            </div>
            <a class="s-pagination-item s-pagination-next" href="/s?k=monitor&page=2">Next</a>
            """
        )
        [deal] = parse_search_results(page)
        self.assertEqual(deal.title, "Monitor")
        self.assertIn("Previously: $129.00", deal.details)
        self.assertIn("Now: $99.00", deal.details)
        self.assertEqual(next_page_url(page), "https://www.amazon.com/s?k=monitor&page=2")
        self.assertIsNone(next_page_url(soup("<span class='s-pagination-next s-pagination-disabled'>")))

    def test_urls_are_encoded(self):
        self.assertEqual(
            coupon_url("Men's Fashion"),
            "https://www.amazon.com/hz/coupons/search?searchText=Men%27s+Fashion",
        )


class TelegramSenderTests(unittest.TestCase):
    def test_dry_run_prints_instead_of_sending(self):
        sender = TelegramSender("token", "chat", dry_run=True)
        deal = Deal("Title", "https://link", "https://img", "details")
        with mock.patch("amazon_deals.requests.post") as post, \
                mock.patch("builtins.print"):
            sender.send(deal)
        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
