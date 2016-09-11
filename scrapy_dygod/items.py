# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDygodItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    download_link = scrapy.Field()
    imdb_score = scrapy.Field()
    
    pass
