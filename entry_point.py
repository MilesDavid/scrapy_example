from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders import quoutes_spider


def run_quotes_crawler():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(quoutes_spider.QuotesSpider)
    process.start()  # the script will block here until the crawling is finished


def main():
    run_quotes_crawler()


if __name__ == '__main__':
    main()
