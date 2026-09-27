import scrapy

from whiskyscrapper.items import Whisky


def parse_price(text: str | None) -> float | None:
    """'£1,234.50' -> 1234.5; None when there is no price."""
    if not text:
        return None
    try:
        return float(text.replace("£", "").replace(",", "").strip())
    except ValueError:
        return None


class WhiskySpider(scrapy.Spider):
    """Names, prices and links of every scotch whisky on whiskyshop.com."""

    name = "whisky"
    allowed_domains = ["www.whiskyshop.com"]
    start_urls = ["https://www.whiskyshop.com/scotch-whisky/all"]

    def parse(self, response):
        for product in response.css("div.product-item-info"):
            price = parse_price(product.css("span.price::text").get())
            yield Whisky(
                name=(product.css("a.product-item-link::text").get() or "").strip(),
                price=price,
                in_stock=price is not None,
                link=product.css("a.product-item-link::attr(href)").get(default=""),
            )

        next_page = response.css("a.action.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
