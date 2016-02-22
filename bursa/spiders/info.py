#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
from ..items import CompanyItem

class InfoSpider(scrapy.Spider):
    name = 'info_spider'
    start_urls = ['http://maya.tase.co.il/bursa/indeximptoday.htm']
    company_page_url_template = 'http://maya.tase.co.il/bursa/CompanyDetails.asp?CompanyCd={site_id}'

    def __init__(self):
        self.driver = webdriver.Firefox()

    def closed(self, spider):
        self.driver.close()

    def parse(self, response):
        self.driver.get(response.url)

        # click the selectbox button
        self.driver.find_element_by_css_selector('#btncmbHavarothidden').click()

        # get selectbox element
        selectbox = self.driver.find_element_by_css_selector('#cmbHavarotselect')

        # iterate all option elements
        for option in selectbox.find_elements_by_tag_name('option'):
            # basic company info
            item = CompanyItem(
                site_id=int(option.get_attribute('value')),
                name=option.text
            )

            # rest of company data from company page
            request = scrapy.Request(
                self.company_page_url_template.format(site_id=item['site_id']),
                callback=self.parse_company_page
            )
            request.meta['item'] = item

            yield request

    def parse_company_page(self, response):
        sel = scrapy.Selector(response=response)

        item = response.meta['item']
        item.update(dict(
            description=self.get_content_by_title(u':תיאור חברה', sel),
            email='',
            website=self.get_content_by_title(u':אתר', sel, link=True),
            corporate_number=self.get_content_by_title(u'מספר ברשם:', sel),
            issuer_number=self.get_content_by_title(u'מספר מנפיק:', sel),
            sector=self.get_content_by_title(u'ענף על:', sel),
            industry=self.get_content_by_title(u'ענף:', sel),
            niche=self.get_content_by_title(u'תת ענף:', sel),
            location=self.get_content_by_title(u':מקום התאגדות', sel),
        ))
        # email: sel.xpath('//table[@class="td_Main_Company_Details"]//a[contains(@href, "mailto:")]].text()').extract()[0],

        return item

    @staticmethod
    def get_content_by_title(title, sel, link=False):
        # prepare selector
        selector = u'//*[text()="{0}"]/ancestor::td/preceding-sibling::td[1]'
        if link:
            selector += '/a'
        selector += '/text()'
        selector = selector.format(title)

        # get result
        result = sel.xpath(selector).extract()
        if result and len(result):
            result = result[0]
            if result.isdigit():
                result = int(result)

            return result
        else:
            return result
