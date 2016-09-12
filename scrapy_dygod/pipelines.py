# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# CleanDataPipeline
from scrapy.exceptions import DropItem
import re

# CommonFieldsPipeline
import datetime
import time

# MongodbPipeline
from scrapy.conf import settings
import pymongo

# logger
import logging
logger = logging.getLogger('pipeline')


class CleanDataPipeline(object):

    def process_item(self, item, spider):

        # if title is empty, discard item
        if not item or 'title' not in item or len(item['title']) == 0:
            logger.warning("Item dropped because no title: " + item['url'])
            raise DropItem("Missing title, %s" % item)
        item['title'] = item['title'][0];

        # get clean imdb_score
        # "imdb_score": "◎IMDB评分　5.4/10 from 952 users"
        if ('imdb_score' in item):
            imdb_score_raw = item['imdb_score'].encode("utf-8")
            matchObj2 = re.match( r'.*(\d+.\d+)\/\d+', imdb_score_raw, re.M|re.I)
            if matchObj2:
                item['imdb_score'] = matchObj2.group(1)
        else:
            logger.warning('IMDB score is not available. ' + item['url'])

        # get clean douban_score
        # "douban_score": "◎豆瓣评分　7.5/10 from 24126 users"
        if ('douban_score' in item):
            douban_score_raw = item['douban_score'].encode("utf-8")
            matchObj3 = re.match( r'.*(\d+.\d+)\/\d+', douban_score_raw, re.M|re.I)
            if matchObj3:
                item['douban_score'] = matchObj3.group(1)
        else:
            logger.warning('Douban score is not available. ' + item['url'])

        # finish the clean data pipeline
        logger.info("Data has been cleaned for this item: " + item['title'])
        return item


class CommonFieldsPipeline(object):

    def process_item(self, item, spider):
        # set current timestamp
        ts = time.time()
        item['update_time'] = (datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

        logger.info("This item is been added common fields. ")
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
            {'url': item['url']},
            dict(item), upsert=True
        )

        logger.info("This item is upsert-ed to MongoDB: " + item['url'])
        return item
