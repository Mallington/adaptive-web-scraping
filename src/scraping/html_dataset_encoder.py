import os.path

from selenium.webdriver.firefox import webdriver
import re
import src.utils.currency_symbols

from selenium import webdriver
import csv
import pandas as pd
CURRENCIES_LIST = list(src.utils.currency_symbols.CURRENCY_SYMBOLS_MAP.values())

interesting_tags = ["h1",	"img", "span"	, "a"	, "div"	, "p"	, "iframe"	, "h2"	, "strong"	, "canvas"	, "h3"]
TAG_PREFIX="tag_"
PARENT_SUFFIX="_parent_"


FONT_SIZE="font_size"
CONTAINS_CURRENCY = "contains_currency"
RATIO="ratio"
OTHER_TAG="other_tag"
NO_TAG="no_tag"
WORD_COUNT = "word_count"

CONTAINS_NUMBER = "contains_number"

CATEGORY = "category"


class HtmlDatasetEncoder:
    def __init__(self, categories=None, output_file_destination= None):
        self.output_file_destination = output_file_destination

        if categories is not None:
            self.cat_dict ={}
            i=0
            for category in categories:
                self.cat_dict[category] = i
                i+=1
            pass
        else:
            self.cat_dict = None

    def find_interesting_tags(self, extracted_element: webdriver.Firefox, dict, suffix=""):
        found = False
        for tag in interesting_tags:
            isTag = False if extracted_element is None else (extracted_element.tag_name.lower() == tag.lower())
            found = found or isTag
            dict[f"{TAG_PREFIX}{tag}{suffix}"] = int(isTag)

        dict[f"{OTHER_TAG}{suffix}"] = int(not found and (extracted_element is not None)) # No recognisable tage
        dict[f"{NO_TAG}{suffix}"] = int(extracted_element is None)

    def try_get_parent(self, extracted_element: webdriver.Firefox):
        try:
            return extracted_element.find_element_by_xpath("./..")
        except:
            return None

    def append_to_file(self, row : dict):
        exists_already = os.path.exists(self.output_file_destination)
        with open(self.output_file_destination, 'a+') as file:
            writer = csv.writer(file)
            if not exists_already:
                writer.writerows([list(row.keys())])
            writer.writerows([list(row.values())])


    def encode_element(self, extracted_element: webdriver.Firefox,  category : str = None, parent_depth=3, additional_features={}):
        features = {
            FONT_SIZE: int(re.sub('[^\d]','', extracted_element.value_of_css_property('font-size'))),
            CONTAINS_CURRENCY : int(any(map(extracted_element.text.__contains__, CURRENCIES_LIST))),
            RATIO : extracted_element.size['width']/extracted_element.size['height'],
            CONTAINS_NUMBER: int(any(map(extracted_element.text.__contains__, ["0","1","2","3","4","5","6","7","8","9"]))),
            WORD_COUNT: len(extracted_element.text.split(" "))
        }

        self.find_interesting_tags(extracted_element, features)

        current_parent = self.try_get_parent(extracted_element)
        for i in range(parent_depth):
            self.find_interesting_tags(current_parent, features, f"{PARENT_SUFFIX}{i}")

            current_parent = None if current_parent is None else self.try_get_parent(current_parent)

        feature_sum = {**features, **additional_features}

        category_dict = {CATEGORY: self.cat_dict[category] if self.cat_dict is not None else category}
        if category is not None:
            feature_sum = {**category_dict, **feature_sum}

        if self.output_file_destination is not None:
            self.append_to_file(feature_sum)


        return feature_sum

    def encode_element_pd(self, extracted_element: webdriver.Firefox, category: str = None, parent_depth=3, additional_features={}):
        return pd.DataFrame(self.encode_element(extracted_element, category, parent_depth, additional_features), index=[0])