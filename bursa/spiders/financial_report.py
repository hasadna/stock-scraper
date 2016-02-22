#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver

from ..spiders import *
from ..items import FinancialReportItem
from ..models import Company as CompanyModel


class FinancialReportSpider(scrapy.Spider):
    name = 'financial_report_spider'
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

        ''' assumptions:
            1. Table title is דוחות כספיים
            2. The yearly data is in the 4th column (left most) of the table
        '''

        # get rows (skip first row)
        # THIS IS WHERE I STOPPED. THIS XPATH IS EVALUATING TO [] :/
        table = sel.xpath(u'//b[text()="דוחות כספיים"]/../../../../../../following-sibling::table/tbody')

        # init Item
        item = FinancialReportItem(company_id=company_id)

        item['year'] = table.xpath(u'./tr[1]/th[4]/font/b/text()')[0].extract()

        # balance
        item['total_balance']         = cast_to_num(table.xpath(u'./tr[3]/td[4]/text()')[0].extract())
        item['current_assets']        = cast_to_num(table.xpath(u'./tr[4]/td[4]/text()')[0].extract())
        item['long_term_assets']      = cast_to_num(table.xpath(u'./tr[5]/td[4]/text()')[0].extract())
        item['shareholders_equity']   = cast_to_num(table.xpath(u'./tr[6]/td[4]/text()')[0].extract())
        item['minority_equity']       = cast_to_num(table.xpath(u'./tr[7]/td[4]/text()')[0].extract())
        item['current_liabilities']   = cast_to_num(table.xpath(u'./tr[8]/td[4]/text()')[0].extract())
        item['long_term_liabilities'] = cast_to_num(table.xpath(u'./tr[9]/td[4]/text()')[0].extract())

        # statements report
        item['revenues']                                = cast_to_num(table.xpath(u'./tr[11]/td[4]/text()')[0].extract())
        item['gross_profit']                            = cast_to_num(table.xpath(u'./tr[12]/td[4]/text()')[0].extract())
        item['operating_income']                        = cast_to_num(table.xpath(u'./tr[13]/td[4]/text()')[0].extract())
        item['income_before_tax']                       = cast_to_num(table.xpath(u'./tr[14]/td[4]/text()')[0].extract())
        item['net_income']                              = cast_to_num(table.xpath(u'./tr[15]/td[4]/text()')[0].extract())
        item['net_income_attributable_to_shareholders'] = cast_to_num(table.xpath(u'./tr[16]/td[4]/text()')[0].extract())
        item['net earnings_per_share']                  = cast_to_num(table.xpath(u'./tr[17]/td[4]/text()')[0].extract())

        # more info
        item['dividend']                  = cast_to_num(table.xpath(u'./tr[19]/td[4]/text()')[0].extract())
        item['operating_activities_cash'] = cast_to_num(table.xpath(u'./tr[20]/td[4]/text()')[0].extract())

        # financial ratios
        item['capital_market']                 = cast_to_num(table.xpath(u'./tr[22]/td[4]/text()')[0].extract())
        item['multiplier']                     = cast_to_num(table.xpath(u'./tr[23]/td[4]/text()')[0].extract())
        item['capital_to_balance_sheet_ratio'] = cast_to_num(table.xpath(u'./tr[24]/td[4]/text()')[0].extract())
        item['return_on_equity']               = cast_to_num(table.xpath(u'./tr[25]/td[4]/text()')[0].extract())

        yield item