import scrapy

from postscrape.items import Post


def clean(text: str | None) -> str:
    """Collapse the tabs/newlines WordPress leaves around text."""
    return " ".join((text or "").split())


class PostsSpider(scrapy.Spider):
    """Blog post titles, dates and authors from zyte.com, following pagination."""

    name = "posts"
    allowed_domains = ["www.zyte.com"]
    start_urls = ["https://www.zyte.com/blog/"]

    def parse(self, response):
        for post in response.css("div.oxy-post"):
            yield Post(
                title=clean(post.css("a.oxy-post-title::text").get()),
                date=clean(post.css("div.oxy-post-image-date-overlay::text").get()),
                author=clean(post.css("div.oxy-post-meta-author::text").get()).removeprefix("By "),
            )

        next_page = response.css("a.page-numbers.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
