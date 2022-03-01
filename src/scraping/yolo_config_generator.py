import os
import json
import yaml
import shutil

class YoloConfigGenerator:
    def __init__(self, data_location, index_file="index.json"):
        self.data_location = data_location
        self.index_file = index_file

        # Check current index file exists
        if not os.path.isfile(os.path.join(self.data_location, self.index_file)):
            raise FileNotFoundError("Index file could not be found: ", index_file)

        # Load the new json file
        with open(os.path.join(self.data_location, self.index_file)) as json_file:
            self.index_dictionary = json.load(json_file)

    def generate_configuration(self, yolo_config_file="yolo-config.yaml", train_path="train/", val_path="val/", test_proportion=0.2):
        self.yolo_config = {
            "path": "./",
            "train": os.path.join(self.data_location, train_path),
            "val":  os.path.join(self.data_location, val_path),
            "nc": len(self.index_dictionary['categories']),
            "names": self.index_dictionary['categories']
        }

        category_indexes = {}
        for i in range(len(self.index_dictionary["categories"])):
            category_indexes[self.index_dictionary["categories"][i]] = i

        shutil.rmtree(os.path.join(self.data_location, train_path), ignore_errors=True)
        os.makedirs(os.path.join(self.data_location, train_path))

        shutil.rmtree(os.path.join(self.data_location, val_path), ignore_errors=True)
        os.makedirs(os.path.join(self.data_location, val_path))

        cutoff = test_proportion*len(self.index_dictionary["snapshots"])
        for index, snapshot in enumerate(self.index_dictionary["snapshots"]):
            path = os.path.join(self.data_location, train_path) if index>cutoff else os.path.join(self.data_location, val_path)
            label_path = os.path.join(path, f"{snapshot['attributes']['master_screenshot_id']}.txt")
            with open(label_path, 'a+') as f:
                dimensions = snapshot['attributes']['dimensions']
                f.write(f"{category_indexes[snapshot['category']]} {dimensions['x']} {dimensions['y']} {dimensions['width']} {dimensions['height']}\n")

            screenshot_path = os.path.join(self.data_location, self.index_dictionary["configuration"]["masterScreenshotFolder"], f"{snapshot['attributes']['master_screenshot_id']}.png")
            screenshot_dst_path = os.path.join(path, f"{snapshot['attributes']['master_screenshot_id']}.png")
            shutil.copy(screenshot_path, screenshot_dst_path)

        with open(os.path.join(self.data_location, yolo_config_file), 'w') as yaml_file:
            yaml.dump(self.yolo_config, yaml_file, default_flow_style=False)
if __name__ == "__main__":
    generator = YoloConfigGenerator("/Users/mathew/github/adaptive-web-scraping/archive-test")
    generator.generate_configuration()