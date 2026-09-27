from scrapy.exceptions import DropItem


class PostscrapePipeline:
    """Drop posts without a title and de-duplicate repeated posts."""

    def open_spider(self, spider):
        self.seen_titles = set()

    def process_item(self, item, spider):
        if not item.title:
            raise DropItem("Post without a title")
        if item.title in self.seen_titles:
            raise DropItem(f"Duplicate post: {item.title}")
        self.seen_titles.add(item.title)
        return item
