import scrapy 

class PostsSpider(scrapy.Spider):
    name ="posts"

    start_urls=['https://www.zyte.com/blog/page/1/', 'https://www.zyte.com/blog/page/2/']

    def parse(self, response):
        # page=response.url.split('/')[-1]
        # filename='posts-%s.html' %page #replace s with the page number
        # with open(filename, 'wb') as f: #wb reps writing mode or writing binary
        #     f.write(response.body)
        for post in response.css('div.oxy-post'):
            yield {
                'title': post.css('a.oxy-post-title::text').get(), #may need an index, .get() method returns a string
                'date': post.css('div.oxy-post-image-date-overlay::text').get().replace('\n','').replace('\t',''),
                'author': post.css('div.oxy-post-meta-author.oxy-post-meta-item::text').get().replace('\n','').replace('\t',''),
            }
        #next_page=response.css('a.page-numbers::attr(href)').get()
        next_page = response.css('a.page-numbers.next').attrib['href']
        if next_page is not None:
            #next_page=response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)