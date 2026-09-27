# Scrapy settings for the whiskyscrapper project.
# Full list: https://docs.scrapy.org/en/latest/topics/settings.html

BOT_NAME = "whiskyscrapper"

SPIDER_MODULES = ["whiskyscrapper.spiders"]
NEWSPIDER_MODULE = "whiskyscrapper.spiders"

# Crawl responsibly: obey robots.txt, identify yourself, and don't hammer the site.
ROBOTSTXT_OBEY = True
USER_AGENT = "whiskyscrapper (+https://github.com/George-Kibe/websitescrapping)"
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 30

# Cache responses locally while developing selectors (stored in .scrapy/).
HTTPCACHE_ENABLED = False

ITEM_PIPELINES = {
    "whiskyscrapper.pipelines.WhiskyscrapperPipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"
