from selenium import webdriver
import os
def take_screenshot(driver: webdriver.Firefox):
    pass

def run_script(driver: webdriver.Firefox, path: str):
    with open(path) as f:
        driver.execute_script(f.read())
    pass

def extract_html(driver: webdriver.Firefox, element: webdriver.Firefox):
    run_script(driver, os.path.join(os.path.dirname(__file__), 'resources/common.js'))
    driver.execute_script("window.insertStyleForAllElementsIn(arguments[0]);", element)
    return element.get_attribute("outerHTML")
