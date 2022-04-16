import os
import shutil

import cv2

from src.scraping.yolo_config_generator import YoloConfigGenerator
from src.yolo.cova_dataset_adapter import CovaDatasetAdapter
from src.yolo.yolo_box_visualiser import YoloBoxVisualiser

if __name__ =="__main__":
    destination = '/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/'

    if os.path.isdir(destination):
        shutil.rmtree(destination)

    adapter = CovaDatasetAdapter(destination)

    adapter.process_dataset('/Users/mathew/data-store/ML-datasets/CoVA-dataset/imgs/',
                            '/Users/mathew/data-store/ML-datasets/CoVA-dataset/bboxes/', filter_categories=[1,2,3])
    adapter.save()

    generator = YoloConfigGenerator(destination)
    generator.generate_configuration()

    folder = '/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/'
    ids = list(set([".".join(f.split(".")[:-1]) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]))

    visualiser = YoloBoxVisualiser(
        f'/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/{ids[0]}.png',
        f'/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/{ids[0]}.txt', relational=True)

    visualiser.show_image(window_name=f"Labels for {ids[0]}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()