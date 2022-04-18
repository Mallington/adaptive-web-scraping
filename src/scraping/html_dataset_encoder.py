from selenium.webdriver.firefox import webdriver


class HtmlDatasetEncoder:
    def __init__(self, output_file_destination, categories):
        self.cat_dict ={}
        i=0
        for category in categories:
            self.cat_dict[category] = i
            i=+1
        pass


    def encode_element(self, dom: webdriver.Firefox,  category : str):

        print(category)