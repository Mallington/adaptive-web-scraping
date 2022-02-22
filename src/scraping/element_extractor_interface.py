from typing import List

from selenium import webdriver

class ElementExtractorInterface:
    def extract_elements(self, dom: webdriver) -> List[webdriver.Firefox]:
        """Extract all matching dom elements"""
        pass