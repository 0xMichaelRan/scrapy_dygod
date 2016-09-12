# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_dygod.items import ScrapyDygodItem


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

    def parse_item(self, response):
        item = ScrapyDygodItem()

        self.logger.info('now crawling item page: %s', response.url)
        result = response.xpath('//div[@class="co_area2"]')

        item['url'] = response.url
        item['title'] = result.xpath('div[@class="title_all"]/h1/text()').extract()

        # the default image (first is poster)
        item['images'] = result.xpath('//div[@id="Zoom"]/p/img/@src').extract()
        # some older version of web page have this as poster
        item['images'].extend(result.xpath('//div[@id="Zoom"]/tr/td/p/img/@src').extract())
        # append the movie screenshot images
        item['images'].extend(result.xpath('//div[@id="Zoom"]/div/img/@src').extract())

        # if (item['images'] != null and len(item['images']) > 0)
        #     item['poster_image']=item['images'][0]

        # TODO: extract download_link
        # item['download_link'] = result.xpath('//div[@id="description"]').extract()

        item['raw_content'] = result.xpath('//div[@id="Zoom"]/p/text()').extract()

        for line in item['raw_content']:
            if 'imdb' in line.lower():
                item['imdb_score'] = line
                break
        # TODO: crawl the IMDB score and save it into the item

        return item
