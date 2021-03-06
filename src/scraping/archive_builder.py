import os.path
import time
import uuid
from typing import List

import cv2

import src.utils.web_driver_utils
from src.predict import AdaptivePredictor
from src.scraping.element_archiver import ElementArchiver
from src.scraping.element_extractor_interface import ElementExtractorInterface
from src.scraping.html_dataset_encoder import HtmlDatasetEncoder

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.bounding_box_utils import convertRelativeToWebpage
from src.utils.rcnn_utils import checkForIntersection
from src.utils.rectangle import Rect

REGION_INTERSECTED_TAG = "intersected_region"
URL_TAG = "url"
class ArchiveBuilder:
    def __init__(self, data_location, driver: webdriver = None):
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver._web_element_cls = WebElement
        self.element_archiver = ElementArchiver(data_location)

        self.rcnn_predictor = AdaptivePredictor("/Users/mathew/github/adaptive-web-scraping/models/CoVa-dataset-train-V1.pt", driver=self.driver)

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

        screenshot_loaded = cv2.imread(master_screenshot_absolute_path)
        filtered_relative_regions, filtered_absolute_regions = self.rcnn_predictor.predict_interest_regions(screenshot_loaded)

        # extra_features_path = f"{master_screenshot_id}.csv"

        extra_features_path = f"extra-features.csv"
        extra_features_path_absolute_path = os.path.join(self.element_archiver.data_location,
                                                         self.element_archiver.index_dictionary["configuration"][
                                                             "extraFeatures"], extra_features_path)


        html_encoder = HtmlDatasetEncoder(element_extractor.available_categories(), extra_features_path_absolute_path)

        for category in element_extractor.available_categories():
            extracted_elements = element_extractor.extract_elements(self.driver, category)
            for extracted_element in extracted_elements:
                try:
                    intersected_with_region = checkForIntersection(filtered_relative_regions, self.driver, extracted_element, debug=True)
                    additional_features = {
                        REGION_INTERSECTED_TAG: int(intersected_with_region),
                        URL_TAG: url
                    }
                    dict_encoded = html_encoder.encode_element(extracted_element, category,
                                                               additional_features=additional_features)
                    print(dict_encoded)


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