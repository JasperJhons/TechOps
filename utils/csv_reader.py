import csv

import os


def read_test_data_from_csv(file_name):
    path_to_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_data", file_name))
    with open(path_to_file, "r", encoding="utf-8") as csv_page:
        test_data = []
        reader = csv.reader(csv_page)
        for row in reader:
            test_data.append(row)
        return test_data[1:]
