import os.path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.fieldclassification.model_train_result import ModelTrainResult

from sklearn import svm

TARGET_FEATURE = 'category'
DEFAULT_FEATURES = ['font_size', 'contains_currency', 'ratio',
       'contains_number', 'word_count', 'tag_h1', 'tag_img', 'tag_span',
       'tag_a', 'tag_div', 'tag_p', 'tag_iframe', 'tag_h2', 'tag_strong',
       'tag_canvas', 'tag_h3', 'other_tag', 'no_tag', 'tag_h1_parent_0',
       'tag_img_parent_0', 'tag_span_parent_0', 'tag_a_parent_0',
       'tag_div_parent_0', 'tag_p_parent_0', 'tag_iframe_parent_0',
       'tag_h2_parent_0', 'tag_strong_parent_0', 'tag_canvas_parent_0',
       'tag_h3_parent_0', 'other_tag_parent_0', 'no_tag_parent_0',
       'tag_h1_parent_1', 'tag_img_parent_1', 'tag_span_parent_1',
       'tag_a_parent_1', 'tag_div_parent_1', 'tag_p_parent_1',
       'tag_iframe_parent_1', 'tag_h2_parent_1', 'tag_strong_parent_1',
       'tag_canvas_parent_1', 'tag_h3_parent_1', 'other_tag_parent_1',
       'no_tag_parent_1', 'tag_h1_parent_2', 'tag_img_parent_2',
       'tag_span_parent_2', 'tag_a_parent_2', 'tag_div_parent_2',
       'tag_p_parent_2', 'tag_iframe_parent_2', 'tag_h2_parent_2',
       'tag_strong_parent_2', 'tag_canvas_parent_2', 'tag_h3_parent_2',
       'other_tag_parent_2', 'no_tag_parent_2']


def make_random_forest() -> RandomForestClassifier:
    random_forest = RandomForestClassifier(max_depth=2, random_state=0)
    return random_forest

def extract_category_features(data_frame):
    return data_frame.loc[:, DEFAULT_FEATURES]

def load_csv(csv_file):
    imported_frame = pd.read_csv(csv_file)
    imported_frame = imported_frame[imported_frame.category != 4][imported_frame.category != 3]

    return train_test_split(extract_category_features(imported_frame), imported_frame[TARGET_FEATURE], test_size=0.33,
                     random_state=42)


def train_models(model_dictionary : dict, csv_file):
    # model = make_random_forest()
    X_train, X_test, y_train, y_test = load_csv(csv_file)

    training_results = {}

    for key in model_dictionary.keys():
        print(key, model_dictionary[key])
        model = model_dictionary[key]
        model.fit(X_train, y_train)

        training_results[key] = ModelTrainResult(model, 0.99)

        model.predict(X_test)





    return training_results


models = {
    'RandomForestClassifier': svm.SVC(probability=True)
}

if __name__ == '__main__':

    result = train_models(models, '/Users/mathew/github/adaptive-web-scraping/data/retail-individual-fields-dataset/extra-features/merged.csv')

    save_directory = '/Users/mathew/github/adaptive-web-scraping/models'

    for model_key in result:
        save_path = os.path.join(save_directory, f"{model_key}-model.pkl")
        pd.to_pickle(result[model_key].model, open(save_path, 'wb'))