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

callback is a callable or a string (in which case a method from the spider object with that name will be used) to be called for each link extracted with the specified link_extractor. This callback receives a response as its first argument and must return a list containing Item and/or Request objects (or any subclass of them).

follow is a boolean which specifies if links should be followed from each response extracted with this rule. If callback is None follow defaults to True, otherwise it defaults to False.

## pipelines.py

## useful for debugging

### log to command line

In the crawler class, do:

    self.logger.info('now crawling item page: %s', response.url)

# Run your crawler

    scrapy crawl crawler_dygod

Or

    scrapy crawl crawler_dygod -o output.json
