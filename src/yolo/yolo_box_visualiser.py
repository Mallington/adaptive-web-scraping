import cv2
import numpy


class YoloBoxVisualiser:
    def __init__(self, image_file, label_file):
        self.image_file = image_file
        self.label_file = label_file

        self.labels = []
        with open(label_file, 'r') as file:
            for line in file.readlines():
                self.labels.append(list(map(float, line.split(' '))))

    def show_image(self, names=None):
        image = cv2.imread(self.image_file)

        height, width, _ = image.shape
        for label in self.labels:
            category, rel_x, rel_y, rel_width, rel_height = label
            x = int((rel_x- rel_width/2)*width)
            y= int((rel_y- rel_height/2)*height)
            box_width = int(rel_width*width)
            box_height = int(rel_height * height)

            image = cv2.rectangle(image, (x,y), (x + box_width, y + box_height), (255, 255, 00), 2)

            text = f"{int(category)}-{names[int(category)]}" if names else f"{int(category)}"
            image = cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


        cv2.imshow('Labels', image)
        cv2.setWindowProperty('Labels', cv2.WND_PROP_TOPMOST, 1)

if __name__ == "__main__":
    visualiser = YoloBoxVisualiser(
        '/Users/mathew/github/adaptive-web-scraping/archive-test/master-screenshots/38dfb5e2-8ef3-46fa-a9d4-b4e6aad59ec8.png',
        '/Users/mathew/github/adaptive-web-scraping/archive-test/labels/38dfb5e2-8ef3-46fa-a9d4-b4e6aad59ec8.txt')

    visualiser.show_image()
    cv2.waitKey(0)
    cv2.destroyAllWindows()