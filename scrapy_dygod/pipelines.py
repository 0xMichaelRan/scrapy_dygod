# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import datetime
import time

from scrapy.conf import settings


class AddCommonFieldsPipeline(object):

    def process_item(self, item, spider):
        # set current timestamp
        ts = time.time()
        item['update_time'] = (datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

        print "This item is been added common fields. "
        return item


class MongodbPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.update(
            {'key': item['url']},
            dict(item), upsert=True
        )

        print "This item is added to MongoDB: " + item['url']
        return item
