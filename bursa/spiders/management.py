#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver

from ..spiders import *
from ..items import ManagementItem
from ..models import Company as CompanyModel


class ManagementSpider(scrapy.Spider):
    name = 'management_spider'
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
            request = scrapy.Request(
                self.company_page_url_template.format(site_id=site_id),
                callback=self.parse_company_page
            )
            request.meta['company_id'] = company_id

            yield request

    def parse_company_page(self, response):
        company_id = response.meta['company_id']
        sel = scrapy.Selector(response=response)

        # get rows (skip first row)
        table = sel.xpath(u'//b[text()="ועדת ביקורת"]/../../..')
        rows = table.xpath('./tr[position()>1]')

        # get data per row
        for row in rows:
            # continue if row is but with a single td
            if len(row.xpath(u'./td')) <= 1:
                continue

            # init Item
            item = ManagementItem(company_id=company_id)

            item['audit_committee'] = get_boolean_value(row.xpath(u'./td[1]/text()')[0].extract())
            item['expertise'] = get_boolean_value(row.xpath(u'./td[2]/text()')[0].extract())
            item['proxy_rate'] = cast_to_num(row.xpath(u'./td[3]/text()')[0].extract())
            item['capital_rate'] = cast_to_num(row.xpath(u'./td[4]/text()')[0].extract())
            item['stock_count'] = cast_to_num(row.xpath(u'./td[5]/text()')[0].extract())
            item['security_name'] = remove_dash(row.xpath(u'./td[6]/text()')[0].extract())
            item['position'] = row.xpath(u'./td[7]/b/text()|./td[7]/text()')[0].extract()
            item['name'] = row.xpath(u'./td[last()]/b/text()|./td[last()]/text()')[0].extract()

            yield item