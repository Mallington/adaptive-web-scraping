from typing import List

from selenium import webdriver

from src.scraping.element_extractor_interface import ElementExtractorInterface


class EtsyExtractor(ElementExtractorInterface):
    def __init__(self):
        pass

    def extract_elements(self, dom: webdriver.Firefox) -> List[webdriver.Firefox]:
        """Extract all matching dom elements"""
        return [dom.find_element_by_id('listing-page-cart')]