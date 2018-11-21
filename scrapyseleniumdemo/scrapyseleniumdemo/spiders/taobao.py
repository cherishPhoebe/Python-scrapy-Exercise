# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from urllib.parse import quote
from scrapyseleniumdemo.items import ProductItem
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from logging import getLogger

class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://www.taobao.com'
    logger = getLogger(__name__)

    def start_requests(self):        
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,10)
        self.browser.get(self.base_url)
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1,self.settings.get('MAX_PAGE')+1):
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
                input.send_keys(keyword)
                submit.click()
                itemlist = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist')))
                url = self.browser.current_url
                self.logger.debug(url)
                yield Request(url=url,callback=self.parse,meta={'page':page},dont_filter=True)

    def parse(self, response):
        products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class，"item")]')
        for product in products:
            item = ProductItem()
            item['price'] = ''.join(product.xpath ('.//div[contains(@class,"price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class,"title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class,"shop")]//text()').extract()).strip()
            item['image'] = ''.join(product.xpath('.//div[@class="pic"]//img[contains(@class,"img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class,"deal-cnt")]//text()') .extract_first()
            item['location'] = product.xpath('.//div[conta ins(@class,"location")]//text ()').extract_first()
            yield item