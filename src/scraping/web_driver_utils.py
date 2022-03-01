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
    run_script(driver, os.path.join(os.path.dirname(__file__), 'resources/common.js'))
    driver.execute_script("window.insertStyleForAllElementsIn(arguments[0]);", element)
    return element.get_attribute("outerHTML")
