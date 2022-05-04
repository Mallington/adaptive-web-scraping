from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.bounding_box_utils import convertRelativeToWebpage
from src.utils.rectangle import Rect
from src.utils.web_driver_utils import mark_elements_with_colour


def checkForIntersection(interestList, driver, extracted_element: webdriver.Firefox, debug=False):
    try:
        element_rect = Rect(extracted_element.rect['x'], extracted_element.rect['y'], extracted_element.rect['width'],
                            extracted_element.rect['height'])
        any_intersected = False
    except AssertionError as e:
        return False

    for interestRegion in interestList:
        cat, rel_x, rel_y, rel_width, rel_height = interestRegion
        x, y, box_width, box_height = convertRelativeToWebpage(rel_x, rel_y, rel_width, rel_height, driver)
        interest_rect = Rect(x, y, box_width, box_height)
        any_intersected = any_intersected or interest_rect.overlaps_with(element_rect)

    if debug:
        colour = "rgba(0, 255, 0, 0.4)" if any_intersected else "rgba(0, 0, 255, 0.4)"
        mark_elements_with_colour(driver, element_rect.l_top.x, element_rect.l_top.y,
                                                             element_rect.r_bot.x, element_rect.r_bot.y, colour=colour)
    return any_intersected
