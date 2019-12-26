import json
from urllib.parse import urljoin

import scrapy

from scrapy.loader import ItemLoader

from items import QuoteItem
from items import LinkItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    main_url = 'http://quotes.toscrape.com/'

    def start_requests(self):
        urls = [
            self.main_url,
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _build_quote_tags_from_selector(self, selector):
        tags = [
            dict(LinkItem.extract_from_selectors(tag))
            for tag in selector
        ]

        return json.dumps(tags)

    def _build_quote_item_from_selector(self, selector):
        item_loader = ItemLoader(item=QuoteItem(), selector=selector)

        item_loader.add_xpath('content', './span[@class="text"]/text()')
        item_loader.add_xpath('author', './span/small[@class="author"]/text()')
        item_loader.add_xpath('author_link', './span/a/@href')

        tags = self._build_quote_tags_from_selector(selector.xpath('./div[@class="tags"]/a'))
        item_loader.add_value('tags', tags)

        return item_loader.load_item()

    def _get_quotes(self, response):
        quote_path = '//div[@class="quote"]'

        for quote_selector in response.xpath(quote_path):
            yield self._build_quote_item_from_selector(quote_selector)

    def parse(self, response):
        yield from self._get_quotes(response)

        next_page_relative_url = response.xpath('//li[@class="next"]/a/@href').get()
        if not next_page_relative_url:
            return

        next_page_url = urljoin(self.main_url, next_page_relative_url)
        yield response.follow(next_page_url, self.parse)
