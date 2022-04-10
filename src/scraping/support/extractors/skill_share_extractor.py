from typing import List

from selenium import webdriver

from src.scraping.element_extractor_interface import ElementExtractorInterface


class SkillShareExtractor(ElementExtractorInterface):
    def __init__(self):
        pass

    def extract_elements(self, dom: webdriver.Firefox,  category : str) -> List[webdriver.Firefox]:
        """Extract all matching dom elements"""
        if category == "product_information":
            return [dom.find_element_by_id('listing-page-cart')]
        elif category == "banner":
            return [dom.find_element_by_id("gnav-header-inner")]
        elif category == "navigation_bar":
            return [dom.find_element_by_id("desktop-category-nav")]
    def available_categories(self) -> List[str]:
        return ["product_information", "banner", "navigation_bar"]