import unittest

from scrapy.http import HtmlResponse, Request

from whiskyscrapper.items import Whisky
from whiskyscrapper.spiders.whiskyspider import WhiskySpider, parse_price

URL = "https://www.whiskyshop.com/scotch-whisky/all"
HTML = """
<div class="product-item-info">
  <a class="product-item-link" href="https://www.whiskyshop.com/a"> Dram A </a>
  <span class="price">£1,234.50</span>
</div>
<div class="product-item-info">
  <a class="product-item-link" href="https://www.whiskyshop.com/b">Dram B</a>
</div>
""".encode()


class WhiskySpiderTests(unittest.TestCase):
    def test_parse(self):
        response = HtmlResponse(url=URL, body=HTML, request=Request(URL))
        results = list(WhiskySpider().parse(response))
        self.assertEqual(
            results,
            [
                Whisky(name="Dram A", price=1234.5, in_stock=True, link="https://www.whiskyshop.com/a"),
                Whisky(name="Dram B", price=None, in_stock=False, link="https://www.whiskyshop.com/b"),
            ],
        )

    def test_parse_price(self):
        self.assertEqual(parse_price("£45.00"), 45.0)
        self.assertIsNone(parse_price("Sold out"))
        self.assertIsNone(parse_price(None))


if __name__ == "__main__":
    unittest.main()
