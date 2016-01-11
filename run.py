from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import bursa.spiders as spiders

def main():
    process = CrawlerProcess(get_project_settings())
    # process.crawl(spiders.info.InfoSpider)
    # process.crawl(spiders.market_cap.MarketCapSpider)
    process.crawl(spiders.stake_holder.StakeHolderSpider)
    process.start()

if __name__ == "__main__":
    main()
