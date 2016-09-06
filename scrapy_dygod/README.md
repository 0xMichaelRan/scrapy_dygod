# How to Setup a crawler for www.dygod.net

## Quick setup

reference [here](http://doc.scrapy.org/en/latest/topics/commands.html?highlight=template#genspider)

    scrapy startproject scrapy_dygod
    cd scrapy_dygod
    scrapy genspider -l
    scrapy genspider -t crawl crawler_dygod www.dygod.net


Now go ahead and make some modifications to 

1. items.py
1. spider/crawler_dygod.py
1. pipelines.py

# Coding!

## items.py

Look at one of the item page, what information do we need? 

    class ScrapyDygodItem(scrapy.Item):
        title = scrapy.Field()
        image = scrapy.Field()
        download_link = scrapy.Field()
        pass

So far, so good. 

## spider/crawler_dygod.py

### part 1: crawling rules

> __[callback](http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules)__ is a callable or a string to be called for each link extracted with the specified link_extractor. 
>
> This callback receives a response as its first argument and must return a list containing Item and/or Request objects (or any subclass of them).

> __follow__ is a boolean which specifies if links should be followed from each response extracted with this rule. 
>
> __If callback is None__ follow defaults to __True__, otherwise it defaults to __False__.

The most basic crawling rule I come up with is like this: 

    class CrawlerDygodSpider(CrawlSpider):
        name = 'crawler_dygod'
        allowed_domains = ['www.dygod.net']
        start_urls = ['http://www.dygod.net/html/gndy/oumei/index.html']
        rules = (
            # 欧美电影 item list
            Rule(LinkExtractor(allow='\/html\/gndy\/oumei\/')),
            # 精品电影 item page
            Rule(LinkExtractor(allow='\/html\/gndy\/dyzz\/\d+\/\d+\.html'), callback='parse_item', follow=True),
            # 综合电影 item page
            Rule(LinkExtractor(allow='\/html\/gndy\/jddy\/\d+\/\d+\.html'), callback='parse_item', follow=True),
        )

Now, we just need to implement parse_item() function. 

At this stage, we are ready to test the crawler. However before doing so, one last step is to set a time gap of delay in settings.py

    DOWNLOAD_DELAY = 3

(otherwise you will received error like this:)

    [<twisted.python.failure.Failure twisted.internet.error.ConnectionDone: Connection was closed cleanly.>]

or 

    Connection to the other side was lost in a non-clean fashion: Connection lost.

### part 2: parse_item() function



## pipelines.py

## useful for debugging

### log to command line

In the crawler class, do:

    self.logger.info('now crawling item page: %s', response.url)

# Run your crawler

    scrapy crawl crawler_dygod

Or

    scrapy crawl crawler_dygod -o output.json
