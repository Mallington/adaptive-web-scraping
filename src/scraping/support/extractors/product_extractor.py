from typing import List

from selenium import webdriver

from src.scraping.element_extractor_interface import ElementExtractorInterface


class ProductExtractor(ElementExtractorInterface):
    def __init__(self):
        pass

    def extract_elements(self, dom: webdriver) -> List[webdriver.Firefox]:
        """Extract all matching dom elements"""
        pass