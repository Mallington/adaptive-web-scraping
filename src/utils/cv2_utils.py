import cv2


def draw_labelled_box(image, rect, text, colour=(255, 255, 00)):
    x, y, box_width, box_height = rect
    print(text, (x, y), (x + box_width, y + box_height))
    image = cv2.rectangle(image, (x, y), (x + box_width, y + box_height), colour, 2)
    return cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)


def draw_bounding_box(image, labelled_rect, names, colour=(255, 255, 00)):
    x, y, box_width, box_height, category = labelled_rect
    text = f"{int(category)}-{names[int(category)]}" if names else f"{int(category)}"

    return draw_labelled_box(image, (x, y, box_width, box_height), text, colour=colour)