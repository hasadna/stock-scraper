#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver

from . import cast_to_num
from ..items import MarketCapItem
from ..models import Company as CompanyModel

class MarketCapSpider(scrapy.Spider):
    name = 'market_cap_spider'
    start_urls = ['http://maya.tase.co.il']
    company_page_url_template = 'http://maya.tase.co.il/bursa/CompanyDetails.asp?CompanyCd={site_id}'

    def __init__(self):
        self.driver = webdriver.Firefox()

    def closed(self, spider):
        self.driver.close()

    def parse(self, response):
        # get all company ids and site_ids
        company_data = CompanyModel.select(CompanyModel.id, CompanyModel.site_id)
        company_data = ((s.id, s.site_id) for s in list(company_data))

        # iterate all companies in db
        for company_id, site_id in company_data:
            item = MarketCapItem(company_id=company_id)
            request = scrapy.Request(
                self.company_page_url_template.format(site_id=site_id),
                callback=self.parse_company_page
            )
            request.meta['item'] = item

            yield request

    def parse_company_page(self, response):
        sel = scrapy.Selector(response=response)
        cap = -1

        # get cap from page
        original_cap = sel.xpath(u'//*[text()="שווי שוק:"]/ancestor::td/preceding-sibling::td[1]/text()')[0].extract()

        try:
            # cast to int
            cap = cast_to_num(original_cap)
        except Exception as e:
            pass

        item = response.meta['item']
        item['cap'] = cap

        return item