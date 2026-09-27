import unittest

from scrapy.http import HtmlResponse, Request

from postscrape.items import Post
from postscrape.spiders.posts_spider import PostsSpider

URL = "https://www.zyte.com/blog/"
HTML = b"""
<div class="oxy-post">
  <a class="oxy-post-title" href="/a">Post A</a>
  <div class="oxy-post-image-date-overlay">\n\t\tDecember 9, 2021\t </div>
  <div class="oxy-post-meta-author oxy-post-meta-item">\n\t\tBy Sarah Lang\t</div>
</div>
<a class="page-numbers next" href="/blog/page/2/">Next</a>
"""


class PostsSpiderTests(unittest.TestCase):
    def test_parse(self):
        response = HtmlResponse(url=URL, body=HTML, request=Request(URL))
        results = list(PostsSpider().parse(response))
        self.assertEqual(results[0], Post(title="Post A", date="December 9, 2021", author="Sarah Lang"))
        self.assertEqual(results[1].url, "https://www.zyte.com/blog/page/2/")

    def test_last_page_has_no_next_request(self):
        response = HtmlResponse(url=URL, body=b"<div class='oxy-post'></div>", request=Request(URL))
        results = list(PostsSpider().parse(response))
        self.assertEqual(results, [Post(title="", date="", author="")])


if __name__ == "__main__":
    unittest.main()
