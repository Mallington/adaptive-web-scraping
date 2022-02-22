from typing import List

from selenium import webdriver

from src.scraping.element_archiver import ElementArchiver
from src.scraping.element_extractor_interface import ElementExtractorInterface

from selenium.webdriver.remote.webelement import WebElement

class ArchiveBuilder:
    def __init__(self, data_location, driver: webdriver = None):
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver._web_element_cls = WebElement
        self.element_archiver = ElementArchiver(data_location)

    def add_site(self, url: str, element_extractor: ElementExtractorInterface):
        self.driver.get(url)
        extracted_elements = element_extractor.extract_elements(self.driver)

        for extracted_element in extracted_elements:
            self.element_archiver.add_snapshot(self.driver, extracted_element, {})