import scrapy


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    site_id = scrapy.Field()
    description = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    registrar_number = scrapy.Field()
    issuer_number = scrapy.Field()
    market = scrapy.Field()
    sector = scrapy.Field()
    sub_sector = scrapy.Field()
    location = scrapy.Field()

class MarketCapItem(scrapy.Item):
    cap = scrapy.Field()
    company_id = scrapy.Field()

class StakeHolderItem(scrapy.Item):
    company_id = scrapy.Field()
    name = scrapy.Field()
    note = scrapy.Field()
    update_date = scrapy.Field()
    site_id = scrapy.Field()
    security_name = scrapy.Field()
    stock_count = scrapy.Field()
    capital_rate = scrapy.Field()
    proxy_rate = scrapy.Field()
    market_cap = scrapy.Field()
