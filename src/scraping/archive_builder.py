import os.path
import uuid
from typing import List

import cv2
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

        # self.driver.get_window_rect().
        master_screenshot_id = str(uuid.uuid4())
        master_screenshot_location = f"{master_screenshot_id}.png"
        master_screenshot_absolute_path = os.path.join(self.element_archiver.data_location, self.element_archiver.index_dictionary["configuration"]["masterScreenshotFolder"], master_screenshot_location)
        self.driver.save_screenshot(master_screenshot_absolute_path)
        self.element_archiver.add_master_snapshot({
            "id": master_screenshot_id,
            "master_screenshot_file": master_screenshot_location
        })


        for category in element_extractor.available_categories():
            extracted_elements = element_extractor.extract_elements(self.driver, category)
            for extracted_element in extracted_elements:
                try:
                    doc_width = self.driver.execute_script("""return window.innerWidth""")
                    doc_height = self.driver.execute_script("""return window.innerHeight""")
                    attributes= {
                        "dimensions": {
                            "x": (extracted_element.location['x'] + extracted_element.size['width'] / 2) / doc_width,
                            "y": (extracted_element.location['y'] + extracted_element.size['height'] / 2) / doc_height,
                            "width": extracted_element.size['width']/doc_width,
                            "height": extracted_element.size['height']/doc_height
                        },
                        "master_screenshot_id": master_screenshot_id
                    }


                    self.element_archiver.add_snapshot(self.driver, extracted_element, url, category, attributes)
                except Exception as e:
                    print("Error: Skipping Element")
                    print(e)

    def save(self):
        self.element_archiver.save()

    def close(self):
        self.driver.quit()