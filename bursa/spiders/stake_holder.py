#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import scrapy, re
from selenium import webdriver

from ..spiders import *
from ..items import StakeHolderItem
from ..models import Company as CompanyModel

class StakeHolderSpider(scrapy.Spider):
    name = 'stakeholder_spider'
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
        rows = sel.xpath('//div[@id="BIShort"]/table/tr[position()>1]')

        # get data per row
        for row in rows:
            # continue if row is but with a single td
            if len(row.xpath(u'./td')) <= 1:
                continue

            # init Item
            item = StakeHolderItem(company_id=company_id)

            # name
            name = self.get_row_name(row)
            # continue if no name
            if not name:
                continue
            item['name'] = name

            # note
            try:
                note = row.xpath(u'./td[2]/div/a/@onmouseover')[0].extract()
                item['note'] = re.match(r'disTip\(\'(.*)\',', note).group(1)
            except Exception as e:
                pass
                # no note, no biggie

            # update date
            update_date = row.xpath(u'./td[3]/text()')[0].extract()
            if update_date:
                update_date = datetime.datetime.strptime(update_date, "%d/%m/%Y")
                item['update_date'] = update_date

            item['security_name'] = row.xpath(u'./td[4]/text()')[0].extract()
            item['stock_count'] = cast_to_num(row.xpath(u'./td[5]/text()')[0].extract())
            item['capital_rate'] = cast_to_num(row.xpath(u'./td[6]/text()')[0].extract())
            item['proxy_rate'] = cast_to_num(row.xpath(u'./td[7]/text()')[0].extract())
            item['market_cap'] = cast_to_num(row.xpath(u'./td[8]/text()')[0].extract())

            yield item

    @classmethod
    def get_row_name(cls, row):
        """
        return name or get previous row name
        if no name appears, it means the row(s) above it display the name
        """
        name = ''
        try:
            name = row.xpath(u'./td[1]//text()')[0].extract()
        except IndexError as e:
            pass
        if not name.strip():
            previous_rows = row.xpath('./preceding-sibling::tr')
            if len(previous_rows) > 1:
                previous_row = row.xpath('./preceding-sibling::tr[1]')
                name = cls.get_row_name(previous_row)

        return name
