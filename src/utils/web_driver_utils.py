from selenium import webdriver
import os
def take_screenshot(driver: webdriver.Firefox):
    pass

def run_script(driver: webdriver.Firefox, *path: str):
    script = ""
    for path_sub in path:
        with open(path_sub) as f:
            script += f.read()
        pass
    driver.execute_script(script)

def extract_html(driver: webdriver.Firefox, element: webdriver.Firefox):
    run_script(driver, os.path.join(os.path.dirname(__file__), '../scraping/resources/common.js'))
    driver.execute_script("window.insertStyleForAllElementsIn(arguments[0]);", element)
    return element.get_attribute("outerHTML")

def make_elements_red(driver: webdriver.Firefox, x0, y0, x1, y1):
    run_script(driver, os.path.join(os.path.dirname(__file__), '../scraping/resources/boundingboxlib.js'))
    print(x0, y0, x1, y1)
    driver.execute_script("window.make_elements_red_within(arguments[0],arguments[1],arguments[2],arguments[3])", x0, y0, x1, y1)