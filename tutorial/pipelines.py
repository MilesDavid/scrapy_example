from pprint import pformat
from scrapy.exceptions import DropItem

import postgresql.driver as pg_driver


class QuotesPipeline:
    _DB_DSN = {
        'host': 'localhost',
        'database': 'quotes',
        'user': 'postgres',
        'password': 'postgres',
        'port': 5432,
    }

    def _create_insert_item_stmt(self):
        return self._connection.prepare(
            """
            INSERT INTO quote("content", "author", "author_link", "tags")
            VALUES ($1::text, $2::text, $3::text, $4::json)
            ;
            """
        )

    def _create_exists_item_stmt(self):
        return self._connection.prepare(
            """
            SELECT "@quote"
            FROM "quote"
            WHERE "content" = $1::text
            ;
            """
        )

    def _insert_item(self, item):
        self._insert_item_stmt(
            item['content'],
            item['author'],
            item['author_link'],
            item['tags']
        )

    def _item_exists(self, item):
        result = self._item_exists_stmt(item['content'])
        return result

    def open_spider(self, spider):
        self._connection = pg_driver.connect(**self._DB_DSN)
        self._insert_item_stmt = self._create_insert_item_stmt()
        self._item_exists_stmt = self._create_exists_item_stmt()

    def close_spider(self, spider):
        self._connection.close()

    def process_item(self, item, spider):
        if self._item_exists(item):
            raise DropItem('Item exists: {}'.format(pformat(item, indent=4)))

        self._insert_item(item)

        return item
