from scrapy.exceptions import DropItem


class WhiskyscrapperPipeline:
    """Drop products without a name."""

    def process_item(self, item, spider):
        if not item.name:
            raise DropItem("Product without a name")
        return item
