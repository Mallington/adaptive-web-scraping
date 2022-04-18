import os
from typing import List

from selenium import webdriver
import time
from src.scraping.element_extractor_interface import ElementExtractorInterface
from src.utils.web_driver_utils import run_script

class DomExtractorSelector(ElementExtractorInterface):
    def __init__(self, categories):
        self.categories = categories

    def extract_elements(self, dom: webdriver.Firefox,  category : str) -> List[webdriver.Firefox]:
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
