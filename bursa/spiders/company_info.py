import scrapy
from selenium import webdriver
from ..items import CompanyItem

class CompanySpider(scrapy.Spider):
    name ='company_spider'
    start_urls = ['http://maya.tase.co.il/bursa/indeximptoday.htm']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        self.driver.get(response.url)

        # click the selectbox button
        self.driver.find_element_by_css_selector('#btncmbHavarothidden').click()

        # get selectbox element
        selectbox = self.driver.find_element_by_css_selector('#cmbHavarotselect')

        # iterate all option elements
        for option in selectbox.find_elements_by_tag_name('option'):
            yield CompanyItem(
                site_id=int(option.get_attribute('value')),
                name=option.text
            )
