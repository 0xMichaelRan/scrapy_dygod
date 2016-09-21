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
        # there is still 30% of item pages without any images,
        # we might wish to discard these items

        # TODO T3T2: extract download_link
        # item['download_link'] = result.xpath('//div[@id="description"]').extract()

        item['raw_content'] = result.xpath('//div[@id="Zoom"]/p/text()').extract()
        item['release_date'] = result.xpath('//div[@class="co_content8"]/ul/text()')[0].extract()

        return item
