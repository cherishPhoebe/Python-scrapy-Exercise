# -*- coding: utf-8 -*-
import scrapy


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['cs.fang.com']
    start_urls = ['http://cs.fang.com/']

    def parse(self, response):
        pass
