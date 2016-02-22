#!/usr/bin/python

import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import bursa.spiders as spiders

def main():
    t = sys.argv[1]
    process = CrawlerProcess(get_project_settings())

    if t == 'info':
        process.crawl(spiders.info.InfoSpider)
    elif t == 'market_cap':
        process.crawl(spiders.market_cap.MarketCapSpider)
    elif t == 'stakeholders':
        process.crawl(spiders.stake_holder.StakeHolderSpider)
    elif t == 'management':
        process.crawl(spiders.management.ManagementSpider)
    elif t == 'financial_report':
        process.crawl(spiders.financial_report.FinancialReportSpider)

    process.start()

if __name__ == "__main__":
    main()
