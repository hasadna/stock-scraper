from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bursa.spiders.company_info import CompanySpider

def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(CompanySpider)
    process.start()

if __name__ == "__main__":
    main()
