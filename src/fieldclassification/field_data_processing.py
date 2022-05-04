import os.path
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.fieldclassification.model_train_result import ModelTrainResult
from sklearn.neural_network import MLPClassifier

from sklearn import svm
from sklearn.metrics import mean_squared_error, accuracy_score

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

import random

def load_csv(csv_file):
    imported_frame = pd.read_csv(csv_file)
    imported_frame = imported_frame[imported_frame.category != 3]  # [ (imported_frame.category != 4)]
    return extract_category_features(imported_frame), imported_frame[TARGET_FEATURE], imported_frame['intersected_region']

def load_csv_split(csv_file):
    X,Y, region_mask = load_csv(csv_file)

    return train_test_split( X,Y, region_mask, test_size=0.33,
                     random_state=42, stratify=Y)


def predict_masked(model, X, intersected_mask):
    y_predict = model.predict(X)
    y_predict_region_filtered = [el if intersected_mask[idx] else 4 for idx, el in enumerate(y_predict)]

    return y_predict, y_predict_region_filtered

def train_models(model_dictionary : dict, csv_file, holdout_csv_file):
    # model = make_random_forest()
    X_train, X_test, y_train, y_test, intersected_region_train, intersected_region_test = load_csv_split(csv_file)

    # X_train = X_train[y_train != 4]
    # y_train = y_train[y_train!=4]

    ### Hold out
    X_test, y_test, intersected_region_test = load_csv(holdout_csv_file)


    oversample = SMOTE()
    X_train, y_train = oversample.fit_resample(X_train, y_train)

    training_results = {}

    intersected_region_test_bool = np.array(intersected_region_test).astype(bool)
    # y_test_region_filtered = np.array(y_test)[intersected_region_test_bool]

    for key in model_dictionary.keys():
        print(key, model_dictionary[key])
        model = model_dictionary[key]
        model.fit(X_train, y_train)

        training_results[key] = ModelTrainResult(model, 0.99)

        y_predict, y_predict_region_filtered = predict_masked(model, X_test, intersected_region_test_bool)

        mse = mean_squared_error(y_test,y_predict)

        mse_filtered = mean_squared_error(y_test, y_predict_region_filtered)
        print(f"----- Model {key} -----")
        print("MSE", mse, mse_filtered)

        accuracy = accuracy_score(y_test, y_predict)

        accuracy_filtered = accuracy_score(y_test, y_predict_region_filtered)

        print("Accuracy", accuracy, accuracy_filtered)
    return training_results


models = {
    # 'RandomForestClassifier': MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(50, 20), random_state=1)  #make_random_forest() #svm.SVC(probability=True)
    # 'MLPClassifier' :
    'rfs': make_random_forest(),
    'SVM': svm.SVC(probability=True),
}

if __name__ == '__main__':
    part_1_data = '/Users/mathew/github/adaptive-web-scraping/data/retail-individual-fields-dataset/extra-features/merged.csv'
    part_2_data = "/Users/mathew/github/adaptive-web-scraping/data/extra-features-csv/extra-features-part2-merge.csv"

    holdout_test_data = "/Users/mathew/github/adaptive-web-scraping/data/retail-holdout-validation-set/extra-features/extra-features.csv"

    result = train_models(models, part_2_data, holdout_test_data)

    save_directory = '/Users/mathew/github/adaptive-web-scraping/models/testing-306/'

    for model_key in result:
        save_path = os.path.join(save_directory, f"{model_key}-model.pkl")
        pd.to_pickle(result[model_key].model, open(save_path, 'wb'))