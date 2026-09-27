"""
Amazon coupon/deal scraping and Telegram posting used by the offersapp views.

Pages are rendered in headless Chromium via Playwright; parsing is done with
BeautifulSoup so it can be unit-tested against static HTML.
"""

import logging
import random
import time
from dataclasses import dataclass
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

log = logging.getLogger(__name__)

AMAZON = "https://www.amazon.com"

COUPON_CATEGORIES = [
    "laptops", "bags", "books", "arts", "samsung", "suits", "macbook", "monitors",
    "iphones", "cabinets", "Automotive", "Baby", "Beauty", "Books", "Fashion", "Music",
    "Computers", "Tools", "Kindle", "Luggage", "Men's Fashion", "Software", "Sports", "Video Games",
]

SEARCH_CATEGORIES = [
    "laptops", "coupons", "offers", "monitors", "iphones", "cabinets", "Arts & Crafts",
    "Automotive", "Baby", "Beauty & Personal Care", "Books", "Digital Music", "Computers",
    "Tools & Home Improvement", "Deals", "Industrial & Scientific", "Kindle Store", "Luggage",
    "Men's Fashion", "Music, CDs & Vinyl", "Pet Supplies", "Software", "Sports & Outdoors",
    "Video Games", "Women's Fashion", "All Departments",
]


@dataclass
class Deal:
    title: str
    link: str
    image_url: str
    details: str

    @property
    def caption(self) -> str:
        return f"{self.title}\n{self.link}\n{self.details}"


# --------------------------------------------------------------------------- fetching


class Browser:
    """A headless Chromium instance reused for every page in a run."""

    def __enter__(self) -> "Browser":
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=True)
        return self

    def __exit__(self, *exc) -> None:
        self._browser.close()
        self._playwright.stop()

    def get_soup(self, url: str) -> BeautifulSoup:
        page = self._browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            page.wait_for_timeout(3_000)  # let client-side widgets render
            return BeautifulSoup(page.content(), "lxml")
        finally:
            page.close()


# --------------------------------------------------------------------------- parsing


def _text(element) -> str:
    return element.get_text(" ", strip=True) if element else ""


def coupon_url(category: str) -> str:
    return f"{AMAZON}/hz/coupons/search?searchText={quote_plus(category)}"


def search_url(category: str) -> str:
    return f"{AMAZON}/s?k={quote_plus(category)}&i=black-friday"


def parse_coupons(soup: BeautifulSoup) -> list[Deal]:
    deals = []
    for item in soup.select("div.coupon[data-promoid]"):
        title = _text(item.select_one("div.coupon-description"))
        image = item.select_one("img.coupon-image")
        if not title or not image:
            continue
        saving = _text(item.select_one("span.a-color-success")).replace("Save", "").strip()
        deals.append(
            Deal(
                title=title,
                link=f"{AMAZON}/promotion/psp/{item['data-promoid']}",
                image_url=image["src"],
                details=f"Coupon: {saving or 'see page'}\nApplied automatically at checkout",
            )
        )
    return deals


def parse_daily_deals(soup: BeautifulSoup) -> list[Deal]:
    deals = []
    # Amazon's CSS-module class names end in a build hash, so match on the stable prefix.
    for item in soup.select("div[class*='DealGridItem-module__dealItemContent']"):
        title = _text(item.select_one("div[class*='DealContent-module__truncate']"))
        link = item.select_one("a[href]")
        image = item.select_one("img[src]")
        if not title or not link or not image:
            continue
        price = _text(item.select_one("span.a-price-whole")) or "n/a"
        offer = _text(item.select_one("span.a-size-small.a-color-secondary")) or "Offer expired"
        deals.append(
            Deal(
                title=title,
                link=urljoin(AMAZON, link["href"]),
                image_url=image["src"],
                details=f"Type: DEAL OF THE DAY\nOffer details: {offer}\nPrice: {price}",
            )
        )
    return deals


def parse_search_results(soup: BeautifulSoup) -> list[Deal]:
    deals = []
    for item in soup.select("div[data-component-type='s-search-result']"):
        title = _text(item.select_one("h2"))
        link = item.select_one("h2 a[href], a.a-link-normal.a-text-normal[href]")
        image = item.select_one("img.s-image")
        if not title or not link or not image:
            continue
        prices = [_text(p) for p in item.select("span.a-price > span.a-offscreen")]
        current = prices[0] if prices else "n/a"
        previous = prices[1] if len(prices) > 1 else "n/a"
        deals.append(
            Deal(
                title=title,
                link=urljoin(AMAZON, link["href"]),
                image_url=image["src"],
                details=f"Previously: {previous}\nNow: {current}",
            )
        )
    return deals


def next_page_url(soup: BeautifulSoup) -> str | None:
    link = soup.select_one("a.s-pagination-next[href]")
    return urljoin(AMAZON, link["href"]) if link else None


# --------------------------------------------------------------------------- sending


class TelegramSender:
    def __init__(self, token: str, chat_id: str, dry_run: bool = False):
        self.url = f"https://api.telegram.org/bot{token}/sendPhoto"
        self.chat_id = chat_id
        self.dry_run = dry_run

    def send(self, deal: Deal) -> None:
        if self.dry_run:
            print(f"--- {deal.image_url}\n{deal.caption}\n")
            return
        response = requests.post(
            self.url,
            data={"chat_id": self.chat_id, "photo": deal.image_url, "caption": deal.caption},
            timeout=30,
        )
        if response.ok:
            log.info("Sent to Telegram: %s", deal.title[:60])
        else:
            log.warning("Telegram rejected %r: %s", deal.title[:60], response.text)


def post_deals(deals: list[Deal], sender: TelegramSender, delay: tuple[int, int]) -> None:
    log.info("Found %d deals", len(deals))
    for deal in deals:
        sender.send(deal)
        if not sender.dry_run:
            time.sleep(random.randint(*delay))  # avoid flooding the chat


# --------------------------------------------------------------------------- jobs


def run_coupons(browser: Browser, sender: TelegramSender) -> None:
    category = random.choice(COUPON_CATEGORIES)
    log.info("Checking coupons for %r", category)
    post_deals(parse_coupons(browser.get_soup(coupon_url(category))), sender, (60, 120))


def run_daily(browser: Browser, sender: TelegramSender) -> None:
    log.info("Checking today's deals")
    post_deals(parse_daily_deals(browser.get_soup(f"{AMAZON}/gp/goldbox")), sender, (5, 10))


def run_search(browser: Browser, sender: TelegramSender, pages: int = 2) -> None:
    category = random.choice(SEARCH_CATEGORIES)
    log.info("Checking discounted search results for %r", category)
    url = search_url(category)
    for _ in range(pages):
        soup = browser.get_soup(url)
        post_deals(parse_search_results(soup), sender, (60, 200))
        url = next_page_url(soup)
        if not url:
            break


JOBS = {"coupons": run_coupons, "daily-deals": run_daily, "multiple-deals": run_search}
