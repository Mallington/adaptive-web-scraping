import cv2
from pandas import DataFrame

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.bounding_box_utils import convertRelativeToAbsolute, convertRelativeToWebpage
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
    def __init__(self, rccn_model_location, field_classifier_location, driver: webdriver = None):
        self.driver = webdriver.Firefox() if driver is None else driver
        self.driver._web_element_cls = WebElement

        self.model_handler = Model_Handler(rccn_model_location,
                                      [640, 640])

        self.html_encoder = HtmlDatasetEncoder()

        self.field_classifier = pd.read_pickle(open(field_classifier_location, 'rb'))


    def predict_url(self, url, load_wait =0):
        self.driver.get(url)
        sleep(load_wait)

        screenshot_file = tempfile.mktemp()
        self.driver.save_screenshot(screenshot_file)
        screenshot_loaded = cv2.imread(screenshot_file)

        relative_regions, absolute_regions  = self.predict_interest_regions(screenshot_loaded)

        self.predict_labels()



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

        print(predictions_relative, predictions_absolute)

        return filtered_relative_regions, filtered_absolute_regions


    def predict_labels_from_df(self, data_frame : DataFrame, threshold):
        inferences = pd.DataFrame(columns=["highest_class", "probability"])
        for index, row in data_frame.iterrows():
            extracted_features = extract_category_features(row)
            result = self.field_classifier.predict(extracted_features)
            proba = self.field_classifier.predict_proba(extracted_features)

            inferences = inferences.append({"highest_class": result, "probability" : proba[result]}, ignore_index=True)



    def predict_labels(self, feature_names = ["title", "price", "description"]):
        elements = get_text_nodes(self.driver)
        i=0

        data = None
        for element in elements:
            try:
                features = self.html_encoder.encode_element_pd(element)

                data = features if data is None else data.append(features)

                extracted_features = extract_category_features(features)
                result =  self.field_classifier.predict(extracted_features)
                proba = self.field_classifier.predict_proba(extracted_features)



            except Exception as e:
                print(f"Element {i} not processed", e)
            i += 1
        print(f"Encoded {i} elements")

if __name__ == "__main__":
    predictor = AdaptivePredictor("/Users/mathew/github/adaptive-web-scraping/models/CoVa-dataset-train-V1.pt", "/Users/mathew/github/adaptive-web-scraping/models/RandomForestClassifier-model.pkl")

    predictor.predict_url("https://www.ebay.co.uk/itm/144515066654?_trkparms=amclksrc%3DITM%26aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D20160908105057%26meid%3D73cfdb26d37641f6bb4b824a37bec5cc%26pid%3D100675%26rk%3D3%26rkt%3D15%26sd%3D304316815116%26itm%3D144515066654%26pmt%3D0%26noa%3D1%26pg%3D2380057%26brand%3DCanon&_trksid=p2380057.c100675.m4236&_trkparms=pageci%3Ac37bf8bd-c5ca-11ec-87da-76d0252d30be%7Cparentrq%3A68ab9ee41800a0f0d64a3621fffac4c2%7Ciid%3A14", load_wait=3)