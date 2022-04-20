import cv2

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.bounding_box_utils import convertRelativeToAbsolute
from src.utils.web_driver_utils import make_elements_red
from src.yolo.yolo_box_visualiser import show_image_with_labels
from src.yolo.yolo_model_handler import Model_Handler
import tempfile
from time import sleep

class AdaptivePredictor:
    def __init__(self, rccn_model_location, driver: webdriver = None):
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver._web_element_cls = WebElement

        self.model_handler = Model_Handler(rccn_model_location,
                                      [640, 640])


    def predict_url(self, url, load_wait =0):
        self.driver.get(url)
        sleep(load_wait)

        screenshot_file = tempfile.mktemp()
        self.driver.save_screenshot(screenshot_file)
        screenshot_loaded = cv2.imread(screenshot_file)

        relative_regions, absolute_regions  = self.predict_interest_regions(screenshot_loaded)


    def predict_interest_regions(self, loaded_image, interest_class_index=0, browser_debug=True, cv2_debug = False):
        predictions_relative, predictions_absolute = self.model_handler.predict(loaded_image)

        filtered_relative_regions = list(filter(lambda a: a[0] == interest_class_index, predictions_relative))
        filtered_absolute_regions = list(filter(lambda a: a[0] == interest_class_index, predictions_absolute))

        if len(filtered_relative_regions) and browser_debug:
            cat, rel_x, rel_y, rel_width, rel_height = filtered_relative_regions[0]

            innerWidth, innerHeight = self.driver.execute_script("return window.innerWidth"), self.driver.execute_script(
                "return window.innerHeight")

            x, y, box_width, box_height = convertRelativeToAbsolute(rel_x, rel_y, rel_width, rel_height, innerWidth,
                                                                    innerHeight)

            make_elements_red(self.driver, x, y, x + box_width, y + box_height)

        if cv2_debug:
            show_image_with_labels(loaded_image, predictions_relative, names=["interest_area", "not_interesting"])

        print(predictions_relative, predictions_absolute)

        return filtered_relative_regions, filtered_absolute_regions


if __name__ == "__main__":
    predictor = AdaptivePredictor("/Users/mathew/github/adaptive-web-scraping/models/CoVa-dataset-train-V1.pt")

    predictor.predict_url("https://www.facebook.com/marketplace/item/542220967526408/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks", load_wait=3)