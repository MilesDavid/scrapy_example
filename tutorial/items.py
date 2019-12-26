# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field

from scrapy.loader.processors import TakeFirst
from scrapy.loader.processors import Join


class LinkItem(Item):
    name = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())

    @classmethod
    def extract_from_selectors(cls, obj, name_selector='./text()', url_selector='./@href'):
        return cls(
            name=obj.xpath(name_selector).get(),
            url=obj.xpath(url_selector).get()
        )


class QuoteItem(Item):
    content = Field(output_processor=TakeFirst())
    author = Field(output_processor=TakeFirst())
    author_link = Field(output_processor=TakeFirst())

    tags = Field(output_processor=Join())
