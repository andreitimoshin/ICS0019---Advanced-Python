"""
@author: antimo
scrapy runspider -o scrapy_telephones.json scrapy_web_spider.py
"""

import scrapy
import time


class ArvutitarkSpider(scrapy.Spider):
    name = "arvutitark_spider"
    url = "https://arvutitark.ee/nutiseadmed/telefonid/1?brands=samsung,xiaomi&sort=top"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'UTF-8',
    }

    def start_requests(self):
        yield scrapy.http.Request(self.url, headers=self.headers)

    def parse(self, response):
        SET_SELECTOR = '.catalogue-product-wrapper'
        for cell in response.css(SET_SELECTOR):

            TITLE_SELECTOR = 'h4._name::attr(title)'
            PRICE_SELECTOR_1 = '._main-price .price-html::text'
            PRICE_SELECTOR_3 = '._main-price .price-html-decimal::text'
            IMAGE_SELECTOR = '._image-wrapper img::attr(src)'
            yield {
                'Title': cell.css(TITLE_SELECTOR).extract_first(),
                'Price': cell.css(PRICE_SELECTOR_1).extract_first().strip() + cell.css(PRICE_SELECTOR_3).extract_first(),
                'Picture href': cell.css(IMAGE_SELECTOR).extract_first()
            }

        NEXT_PAGE_SELECTOR = '._pagination-button.-arrow.-right a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()

        if next_page:
            time.sleep(3)
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.parse, headers=self.headers)
