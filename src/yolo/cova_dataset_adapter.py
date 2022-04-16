from src.scraping.element_archiver import ElementArchiver
from src.utils.bounding_box_utils import get_bounding_rect, rect_inside, get_bounding_boxes, get_margins, rect_inside_list
import uuid
import cv2
import os
import shutil

import cv2

from src.utils.cv2_utils import draw_labelled_box


def filter_labels(labels:list, filter_categories:list):
    filtered_labels = []
    other_labels = []

    for label in labels:

        x, y, box_width, box_height, category = [int(a) for a in label]

        if filter_categories is None or category in filter_categories:
            filtered_labels += [(x, y, x + box_width, y + box_height)]
        else:
            other_labels += [(x, y, x + box_width, y + box_height)]

    return filtered_labels, other_labels


def bounding_box_filtered_features(filtered_labels, other_labels, width, height):
    filtered_rect = get_bounding_boxes(filtered_labels)

    clustered_other_labels = []

    for margin in get_margins(filtered_rect[0], filtered_rect[1], filtered_rect[2], filtered_rect[3], 0, 0, width,
                              height):

        inside = rect_inside_list(other_labels, margin[0], margin[1], margin[2], margin[3])
        shrunk_margin = get_bounding_boxes(inside)

        if shrunk_margin is not None:
            clustered_other_labels += [shrunk_margin]

    return filtered_rect, clustered_other_labels

def cluster_desired_features(labels:list, filter_categories:list, width:int, height:int):
    filtered_labels, other_labels = filter_labels(labels, filter_categories)

    return bounding_box_filtered_features(filtered_labels, other_labels, width, height)


class CovaDatasetAdapter():

    def __init__(self, output_data_location):
        self.element_archiver = ElementArchiver(output_data_location)


    def import_labels(self, label_file):
        labels = []

        skip = True
        with open(label_file, 'r') as file:
            for line in file.readlines():
                if not skip:
                    labels.append(list(map(float, line.split(','))))
                skip = False

        return labels
    def process_set(self, image_file, label_file, filter_categories=[1,2,3]):

        image = cv2.imread(image_file)
        labels = self.import_labels(label_file)

        height, width, _ = image.shape

        list = []

        for label in labels:
            x, y, box_width, box_height, category = [int(a) for a in label]

            list += [(x, y, box_width, box_height, category)]

        filtered_rect, clustered_other_labels = cluster_desired_features(list, filter_categories, width, height)


        master_screenshot_id = str(uuid.uuid4())
        master_screenshot_location = f"{master_screenshot_id}.png"
        master_image_path = os.path.join(self.element_archiver.data_location,
                         self.element_archiver.index_dictionary["configuration"]["masterScreenshotFolder"],
                         master_screenshot_location)

        shutil.copy2(image_file, master_image_path)

        self.element_archiver.add_master_snapshot({
            "id": master_screenshot_id,
            "master_screenshot_file": master_screenshot_location
        })

        self.element_archiver.add_snapshot_manually("interest_area", filtered_rect, width, height, master_screenshot_id)

        for clustered_other_label in clustered_other_labels:
            self.element_archiver.add_snapshot_manually("not_interesting", clustered_other_label, width, height, master_screenshot_id)

        image = draw_labelled_box(image, filtered_rect, "Filtered rec")

        cv2.imshow( f"Debug {image_file} filtered rect", image)

    def __list_viable_ids(self, folder):
        return [".".join(f.split(".")[:-1]) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]

    def process_dataset(self, image_folder, labels_folder, filter_categories=[1,2,3]):
        ids = self.__list_viable_ids(image_folder)

        i  =0
        for id in ids:
            image_file = os.path.join(image_folder, f"{id}.png")
            labels_file = os.path.join(labels_folder, f"{id}.csv")

            try:
                self.process_set(image_file, labels_file, filter_categories=filter_categories)
            except FileNotFoundError as e:
                print(f"Processing {id} failed because {e}")
            i+=1

            if i % 10 ==0:
                print(f"Done: {(i/len(ids))*100}%")

    def save(self):
        self.element_archiver.save()


if __name__ == "__main__":
    adapter = CovaDatasetAdapter('/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted')
    adapter.process_dataset('/Users/mathew/data-store/ML-datasets/CoVA-dataset/imgs/',
                            '/Users/mathew/data-store/ML-datasets/CoVA-dataset/bboxes/')
    adapter.save()

