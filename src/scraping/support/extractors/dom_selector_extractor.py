import os
from typing import List

from selenium import webdriver
import time
from src.scraping.element_extractor_interface import ElementExtractorInterface
from src.utils.web_driver_utils import run_script

class DomExtractorSelector(ElementExtractorInterface):
    def __init__(self, categories, other_elements=None):
        self.other_elements = other_elements
        self.categories = categories + [other_elements]

    def extract_elements(self, dom: webdriver.Firefox,  category : str) -> List[webdriver.Firefox]:

        if self.other_elements is not None and category == self.other_elements:
            return []
        else:
            """Extract all matching dom elements"""
            os.system(f"say {category} elements &")

            run_script(dom, os.path.join(os.path.dirname(__file__), '../../resources/jquery.js'),
                       os.path.join(os.path.dirname(__file__), '../../resources/domoutlinelib.js'),
                       os.path.join(os.path.dirname(__file__), '../../resources/domoutlinerun.js'))

            while not dom.execute_script("""return window.selection_finished"""):
                time.sleep(0.1)
                pass
            return dom.execute_script("""return window.selected_elements""")

    def available_categories(self) -> List[str]:

        return self.categories
