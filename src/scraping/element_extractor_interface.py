from typing import List

from selenium import webdriver

class ElementExtractorInterface:
    def extract_elements(self, dom: webdriver, category : str) -> List[webdriver.Firefox]:
        """Extract all matching dom elements"""
        pass
    def available_categories(self) -> List[str]:
        """Returns available classes"""
        pass