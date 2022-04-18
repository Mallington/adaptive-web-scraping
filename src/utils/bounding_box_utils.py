import sys


def get_bounding_boxes(rectangles :list):
    min_x_b, min_y_b, max_x_b, max_y_b = sys.maxsize, sys.maxsize, -sys.maxsize, -sys.maxsize
    for rectangle in rectangles:
        min_x_a, min_y_a, max_x_a, max_y_a = rectangle
        min_x_b, min_y_b, max_x_b, max_y_b = get_bounding_rect(min_x_a, min_y_a, max_x_a, max_y_a, min_x_b, min_y_b, max_x_b, max_y_b)

    if min_x_b >= max_x_b or min_y_b >= max_y_b:
        return None

    return min_x_b, min_y_b, max_x_b, max_y_b
def get_bounding_rect(min_x_a, min_y_a,  max_x_a, max_y_a, min_x_b, min_y_b,  max_x_b, max_y_b):
    return int(min(min_x_a, min_x_b)), int(min(min_y_a, min_y_b)), int(max(max_x_a, max_x_b)), int(max(max_y_a, max_y_b))

def rect_inside(min_x_a, min_y_a,  max_x_a, max_y_a, min_x_b, min_y_b,  max_x_b, max_y_b) -> bool:
    return min_x_a >= min_x_b and min_y_a >= min_y_b and max_x_a <= max_x_b and max_y_a <= max_y_b

def rect_inside_list(rectangles, min_x_b, min_y_b,  max_x_b, max_y_b) -> list:
    list = []
    for rectangle in rectangles:
        min_x_a, min_y_a, max_x_a, max_y_a = rectangle
        if rect_inside(min_x_a, min_y_a, max_x_a, max_y_a, min_x_b, min_y_b,  max_x_b, max_y_b):
            list += [rectangle]
    return list
def get_margins(min_x_a, min_y_a,  max_x_a, max_y_a, min_x_b, min_y_b,  max_x_b, max_y_b) -> list:
    list = []
    upper = min_x_b, min_y_b, max_x_b, min_y_a
    right = max_x_a, min_y_a, max_x_b, max_y_a
    left = min_x_b, min_y_a, min_x_a, max_y_a
    lower = min_x_b, max_y_a, max_x_b, max_y_b

    return [upper, lower, right, left]

def convertRelativeToAbsolute(rel_x , rel_y, rel_width, rel_height, width, height):
    x = int((rel_x - rel_width / 2) * width)
    y = int((rel_y - rel_height / 2) * height)
    box_width = int(rel_width * width)
    box_height = int(rel_height * height)

    return x, y, box_width, box_height

