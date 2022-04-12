import sys

import cv2
import numpy
from src.utils.bounding_box_utils import get_bounding_rect, rect_inside, get_bounding_boxes, get_margins, rect_inside_list
from src.yolo.cova_dataset_adapter import cluster_desired_features
class YoloBoxVisualiser:
    def __init__(self, image_file, label_file, relational=True):
        self.image_file = image_file
        self.label_file = label_file

        self.labels = []

        self.relational = relational

        skip = True
        with open(label_file, 'r') as file:
            for line in file.readlines():
                if not skip:
                    self.labels.append(list(map(float, line.split(' '))))
                skip = False


    def draw_labelled_box(self, image, rect, text, colour=(255, 255, 00)):
        x, y, box_width, box_height = rect

        image = cv2.rectangle(image, (x, y), (x + box_width, y + box_height), colour, 2)
        return cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


    def draw_bounding_box(self, image, labelled_rect, names, colour=(255, 255, 00)):
        x, y, box_width, box_height, category = labelled_rect
        text = f"{int(category)}-{names[int(category)]}" if names else f"{int(category)}"
        return self.draw_labelled_box(image, (x, y, box_width, box_height), text, colour=colour)






    def show_image(self, names=None, window_name="Labels", filter_categories=None, bounding_box=True):
        image = cv2.imread(self.image_file)

        height, width, _ = image.shape

        list = []

        for label in self.labels:
            if self.relational:
                category, rel_x, rel_y, rel_width, rel_height = label
                x = int((rel_x- rel_width/2)*width)
                y = int((rel_y- rel_height/2)*height)
                box_width = int(rel_width*width)
                box_height = int(rel_height * height)
            else:
                x, y, box_width, box_height, category = [int(a) for a in label]

            list += [(x, y, box_width, box_height, category)]

            if filter_categories is None or label in filter_categories:
                image = self.draw_bounding_box(image, (x, y, box_width, box_height, category), names)


        cv2.imshow(window_name, image)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

if __name__ == "__main__":
    num = 500

    # for i in range(150,160):
    #     try:
    #         visualiser = YoloBoxVisualiser(
    #             f'/Users/mathew/data-store/ML-datasets/CoVA-dataset/imgs/{i}.png',
    #             f'/Users/mathew/data-store/ML-datasets/CoVA-dataset/bboxes/{i}.csv', relational=False)
    #
    #         visualiser.show_image(window_name= f"Labels for {i}", filter_categories=[1,2,3])
    #     except FileNotFoundError as e:
    #         print(f"No {i}", type(e))

    # visualiser = YoloBoxVisualiser(
    #     f'/Users/mathew/data-store/ML-datasets/CoVA-dataset/imgs/{num}.png',
    #     f'/Users/mathew/data-store/ML-datasets/CoVA-dataset/bboxes/{num}.csv')
    #
    # visualiser.show_image()

    id = '0b2ec1d7-3b08-4e8a-bd19-dedc45462185'
    visualiser = YoloBoxVisualiser(
        f'/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/{id}.png',
        f'/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/{id}.txt', relational=True)

    visualiser.show_image(window_name=f"Labels")

    cv2.waitKey(0)
    cv2.destroyAllWindows()