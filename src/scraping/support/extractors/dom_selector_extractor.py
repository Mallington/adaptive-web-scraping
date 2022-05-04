import os
from typing import List

from selenium import webdriver
import time
from src.scraping.element_extractor_interface import ElementExtractorInterface
from src.utils.web_driver_utils import run_script

class DomExtractorSelector(ElementExtractorInterface):
    def __init__(self, categories, other_elements=None):

        self.other_elements = other_elements
        self.categories = categories + [other_elements] if other_elements is not None else categories


    def accept_cookies(self, dom: webdriver.Firefox, urls) -> dict:
            """Extract all matching dom elements"""
            cookie_dict = {}
            for url in urls:
                dom.get(url)
                os.system(f"say Yum yum cookies &")

                run_script(dom, os.path.join(os.path.dirname(__file__), '../../resources/jquery.js'),
                           os.path.join(os.path.dirname(__file__), '../../resources/domoutlinelib.js'),
                           os.path.join(os.path.dirname(__file__), '../../resources/domoutlinerun.js'))

                while not dom.execute_script("""return window.selection_finished"""):
                    time.sleep(0.1)
                    pass
                cookie_dict[url] = dom.get_cookies()
                os.system(f"say Cookie accepted &")

            return cookie_dict
    def accept_cookies_auto(self, dom: webdriver.Firefox, cookie_dict: dict):
            """Extract all matching dom elements"""
            for url in list(cookie_dict.keys()):
                dom.get(url)
                for cookie in cookie_dict[url]:
                    dom.add_cookie(cookie)


    def extract_elements(self, dom: webdriver.Firefox, category : str, element_limit=90) -> List[webdriver.Firefox]:

        if self.other_elements is not None and category == self.other_elements:
            i=0
            final_list =[]

            for element in dom.find_elements_by_xpath("//*[not(child::*) and text()]"):
                if len(element.text) and not (hasattr(element, 'already_selected') and element.already_selected):
                    final_list += [element]
                    i += 1
                if i >= element_limit:
                    break
            return final_list

        else:
            """Extract all matching dom elements"""
            os.system(f"say {category} elements &")

            run_script(dom, os.path.join(os.path.dirname(__file__), '../../resources/jquery.js'),
                       os.path.join(os.path.dirname(__file__), '../../resources/domoutlinelib.js'),
                       os.path.join(os.path.dirname(__file__), '../../resources/domoutlinerun.js'))

            while not dom.execute_script("""return window.selection_finished"""):
                time.sleep(0.1)
                pass
            selected_elements = dom.execute_script("""return window.selected_elements""")

            for selected_element in selected_elements:
                selected_element.already_selected = True

            return selected_elements

    def available_categories(self) -> List[str]:

        return self.categories
