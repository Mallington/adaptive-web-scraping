import cv2

from src.utils.cv2_utils import draw_bounding_box


class YoloBoxVisualiser:
    def __init__(self, image_file, label_file, relational=True, skip = False):
        self.image_file = image_file
        self.label_file = label_file

        self.labels = []

        self.relational = relational

        with open(label_file, 'r') as file:
            for line in file.readlines():
                if not skip:
                    self.labels.append(list(map(float, line.split(' '))))
                skip = False






    def show_image(self, names=None, window_name="Labels", filter_categories=None):
        image = cv2.imread(self.image_file)

        height, width, _ = image.shape

        for label in self.labels:
            if self.relational:
                category, rel_x, rel_y, rel_width, rel_height = label
                x = int((rel_x- rel_width/2)*width)
                y = int((rel_y- rel_height/2)*height)
                box_width = int(rel_width*width)
                box_height = int(rel_height * height)
            else:
                x, y, box_width, box_height, category = [int(a) for a in label]



            if filter_categories is None or label in filter_categories:
                image = draw_bounding_box(image, (x, y, box_width, box_height, category), names)


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

    id = '0a1ec359-4ae0-4ebc-aa29-d017838ddbd7'
    visualiser = YoloBoxVisualiser(
        f'/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/{id}.png',
        f'/Users/mathew/github/adaptive-web-scraping/data/CoVa-adapted/train/{id}.txt', relational=True)

    visualiser.show_image(window_name=f"Labels", filter_categories=[0])

    cv2.waitKey(0)
    cv2.destroyAllWindows()