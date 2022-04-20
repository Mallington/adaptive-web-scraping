import os
import json
from selenium import webdriver
import shutil
import uuid
import datetime

class ElementArchiver:
    def __init__(self, data_location, screenshot_prefix="screenshot", html_prefix="styled_html_",index_file="index.json"):
        self.data_location = data_location
        self.screenshot_prefix = screenshot_prefix
        self.html_prefix = html_prefix
        self.index_file = index_file

        # Creates new archive directory if one does not exist
        if not os.path.isdir(data_location):
            print("Creating new archive location")
            os.makedirs(data_location)
            shutil.copy(os.path.join(os.path.dirname(__file__), 'resources/archive_index_stub.json'), os.path.join(self.data_location, self.index_file))

        # Check current index file exists
        if not os.path.isfile(os.path.join(self.data_location, self.index_file)):
            raise FileNotFoundError("Index file could not be found: ", index_file)

        # Load the new json file
        with open(os.path.join(self.data_location, self.index_file)) as json_file:
            self.index_dictionary = json.load(json_file)

        # Double check relevant folders are there
        os.makedirs(os.path.join(self.data_location, self.index_dictionary["configuration"]["screenshotFolder"]), exist_ok=True)
        os.makedirs(os.path.join(self.data_location, self.index_dictionary["configuration"]["htmlFolder"]), exist_ok=True)
        os.makedirs(os.path.join(self.data_location, self.index_dictionary["configuration"]["masterScreenshotFolder"]), exist_ok=True)
        os.makedirs(os.path.join(self.data_location, self.index_dictionary["configuration"]["extraFeatures"]), exist_ok=True)
        pass

    def add_master_snapshot(self, snapshot_details: dict):
        self.index_dictionary["master_snapshots"] += [snapshot_details]

    def add_snapshot(self, driver: webdriver.firefox,  extracted_element: webdriver.firefox, url: str, category: str ,attributes : dict):
        # image = take_screenshot(extracted_element)
        id = uuid.uuid4()


        snapshot_entry = {
            "id": str(id),
            "taken": str(datetime.datetime.now()),
            "page": url,
            "width": extracted_element.size['width'],
            "height": extracted_element.size['height'],
            "attributes": attributes,
            "screenShotFile": f"{self.screenshot_prefix}{id}.png",
            "htmlFile": f"{self.html_prefix}{id}.html",
            "category": category
        }

        #Skip these bits
        # extracted_element.screenshot(
        #     os.path.join(self.data_location, self.index_dictionary["configuration"]["screenshotFolder"],
        #                  snapshot_entry["screenShotFile"]))
        #
        # styled_html = extract_html(driver, extracted_element)
        # with open(os.path.join(self.data_location, self.index_dictionary["configuration"]["htmlFolder"], snapshot_entry["htmlFile"]), "w") as html_file:
        #     html_file.writelines(styled_html)

        self.index_dictionary["snapshots"] += [snapshot_entry]

        if category not in self.index_dictionary["categories"]:
            self.index_dictionary["categories"].append(category)

    def add_snapshot_manually(self, category: str , bounding_rect, doc_width, doc_height, master_screenshot_id):
        # image = take_screenshot(extracted_element)
        id = uuid.uuid4()
        x, y, max_x, max_y = bounding_rect

        width = max_x - x
        height = max_y - y

        attributes = {
            "dimensions": {
                "x": (x + width / 2) / doc_width,
                "y": (y + height / 2) / doc_height,
                "width": width / doc_width,
                "height": height / doc_height
            },
            "master_screenshot_id": master_screenshot_id
        }


        snapshot_entry = {
            "id": str(id),
            "taken": str(datetime.datetime.now()),
            "page": "UnknownPage",
            "width": width,
            "height": height,
            "attributes": attributes,
            "screenShotFile": f"{self.screenshot_prefix}{id}.png",
            "htmlFile": "Not Known",
            "category": category
        }

        #Skip these bits
        # extracted_element.screenshot(
        #     os.path.join(self.data_location, self.index_dictionary["configuration"]["screenshotFolder"],
        #                  snapshot_entry["screenShotFile"]))
        #
        # styled_html = extract_html(driver, extracted_element)
        # with open(os.path.join(self.data_location, self.index_dictionary["configuration"]["htmlFolder"], snapshot_entry["htmlFile"]), "w") as html_file:
        #     html_file.writelines(styled_html)

        self.index_dictionary["snapshots"] += [snapshot_entry]

        if category not in self.index_dictionary["categories"]:
            self.index_dictionary["categories"].append(category)


    def save(self):
        with open(os.path.join(self.data_location, self.index_file), 'w') as fp:
            json.dump(self.index_dictionary, fp)
        pass