import os

def merge_cova_features(extra_features_directory, bboxes_directory):
    first_ever_line = True
    files_list = list(filter(lambda file: file.endswith(".csv"), os.listdir(extra_features_directory)))
    with open(os.path.join(extra_features_directory, "merged.csv"), "a") as csv_destination:
        for file in files_list:
            first_line_of_file = True
            with open(os.path.join(bboxes_directory, file),
                      "r") as csv_reader_box:
                with open(os.path.join(extra_features_directory, file), "r") as csv_reader_feat:
                    csv_reader_box_lines = csv_reader_box.readlines()
                    csv_reader_feat_lines = csv_reader_feat.readlines()
                    for i in range(len(csv_reader_box_lines)):
                        if not first_line_of_file or first_ever_line:
                            str_app = f"{csv_reader_box_lines[i].rstrip()},{csv_reader_feat_lines[i]}"
                            print(str_app)
                            csv_destination.writelines([str_app])
                        first_line_of_file = False
                        first_ever_line = False