import scrapy


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    site_id = scrapy.Field()
