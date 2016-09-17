# -*- coding: utf-8 -*-

import scrapy
import json


class ScrapyDygodItem(scrapy.Item):

    # common fields
    update_time = scrapy.Field()

    # item fields to be crawled
    url = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    download_link = scrapy.Field()
    raw_content = scrapy.Field()

    # item fields to be derived
    poster_image = scrapy.Field()
    imdb_score = scrapy.Field()
    douban_score = scrapy.Field()

    # override this, so that I get more pretty print of items crawled
    def __repr__(self):
        r = {}
        # I wish to exclude 'raw_content' from the item debug logging
        # http://stackoverflow.com/a/32910531
        for attr, value in self.__dict__['_values'].iteritems():
            if attr not in ['raw_content']:
                r[attr] = value
        return json.dumps(r, sort_keys=False, indent=4, separators=(',', ': '))

    pass
