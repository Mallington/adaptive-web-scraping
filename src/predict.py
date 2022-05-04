import cv2
from pandas import DataFrame

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.bounding_box_utils import convertRelativeToAbsolute, convertRelativeToWebpage
from src.utils.rcnn_utils import checkForIntersection
from src.utils.rectangle import Rect
from src.utils.web_driver_utils import mark_elements_with_colour
from src.yolo.yolo_box_visualiser import show_image_with_labels
from src.yolo.yolo_model_handler import Model_Handler
import tempfile
from time import sleep
from src.scraping.html_dataset_encoder import HtmlDatasetEncoder
from src.utils.web_driver_utils import get_text_nodes
from src.fieldclassification.field_data_processing import extract_category_features
import pandas as pd

class AdaptivePredictor:
    def __init__(self, rccn_model_location, field_classifier_location=None, driver: webdriver = None):
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver._web_element_cls = WebElement

        self.model_handler = Model_Handler(rccn_model_location,
                                      [640, 640])

        self.html_encoder = HtmlDatasetEncoder()

        if  field_classifier_location is not None:
            self.field_classifier = pd.read_pickle(open(field_classifier_location, 'rb'))

    def predict_url(self, url, load_wait =0):
        self.driver.get(url)
        sleep(5)

        screenshot_file = tempfile.mktemp()
        self.driver.save_screenshot(screenshot_file)
        screenshot_loaded = cv2.imread(screenshot_file)

        relative_regions, absolute_regions  = self.predict_interest_regions(screenshot_loaded)

        df = self.predict_labels()

        intersected = []

        for element in df['element']:
            intersected += [checkForIntersection(relative_regions, self.driver, element, debug=True)]

        df['intersected'] = intersected

        highest_classes = pd.DataFrame()
        for class_number in self.field_classifier.classes_:
            individual_class = df.loc[df['highest_class'] == int(class_number)]
            only_intersected = individual_class.loc[individual_class['intersected']]
            highest = only_intersected.loc[only_intersected['probability'].idxmax()]
            highest_classes = pd.concat([highest_classes, highest], ignore_index=True)
            print(f"Class {class_number} : {highest.element.text}, Prob: {highest['probability']}")

    def predict_interest_regions(self, loaded_image, interest_class_index=0, browser_debug=True, cv2_debug = False):
        predictions_relative, predictions_absolute = self.model_handler.predict(loaded_image)

        filtered_relative_regions = list(filter(lambda a: a[0] == interest_class_index, predictions_relative))
        filtered_absolute_regions = list(filter(lambda a: a[0] == interest_class_index, predictions_absolute))


        if len(filtered_relative_regions) and browser_debug:
            cat, rel_x, rel_y, rel_width, rel_height = filtered_relative_regions[0]

            x, y, box_width, box_height = convertRelativeToWebpage(rel_x, rel_y, rel_width, rel_height, self.driver)
            mark_elements_with_colour(self.driver, x, y, x + box_width, y + box_height)

        if cv2_debug:
            show_image_with_labels(loaded_image, predictions_relative, names=["interest_area", "not_interesting"])

        return filtered_relative_regions, filtered_absolute_regions


    def predict_labels_from_df(self, data_frame : DataFrame):
        data_frame_essential = extract_category_features(data_frame)

        data_frame["highest_class"] = self.field_classifier.predict(data_frame_essential)
        data_frame["probability"] = [item[data_frame["highest_class"][index]] for index, item in enumerate(self.field_classifier.predict_proba(data_frame_essential))]

        return data_frame


    def predict_labels(self):
        elements = get_text_nodes(self.driver)
        i=0
        elements_list = []
        data = None
        for element in elements:
            try:
                features = self.html_encoder.encode_element_pd(element)
                data = features if data is None else pd.concat([data, features], ignore_index=True)
                elements_list += [element]
            except Exception as e:
                print(f"Element {i} not processed", e)
            i += 1

        data['element'] = elements_list

        return self.predict_labels_from_df(data)

if __name__ == "__main__":
    predictor = AdaptivePredictor("/Users/mathew/github/adaptive-web-scraping/models/CoVa-dataset-train-V1.pt", "/Users/mathew/github/adaptive-web-scraping/models/RandomForestClassifier-model.pkl")
    url = "file:///Users/mathew/github/dissertation-documents/acm-paper/tex/problem-definition/diagram/scraper.html"
    predictor.predict_url(url, load_wait=10)