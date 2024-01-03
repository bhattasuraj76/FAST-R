""" 
Converts analyzer files for individual projects in both strict and loose setting to csv
"""

import json
import csv


def flatten_json(nested_json):
    flattened_json = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        else:
            flattened_json[name[:-1]] = x

    flatten(nested_json)
    return flattened_json


def handle_io(input_file, output_file):
    # Opening JSON file and loading the data
    # into the variable data
    with open(input_file) as json_file:
        data = json.load(json_file)

    analyzer_detail_data = map(lambda x: flatten_json(x), data["details"])

    # now we will open a file for writing
    data_file = open(output_file, "w")

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for each in analyzer_detail_data:
        if count == 0:
            # Writing headers of CSV file
            header = each.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(each.values())

    data_file.close()


projects_list = [
    "commons-lang",
    "gson",
    # "commons-math",
    "jfreechart",
    "joda-time",
    # "pmd",
    #  "cts",
]

for setting in ["output-loose", "output-strict"]:
    for project in projects_list:
        input_file = setting + "/" + project + "_analyzer.json"
        output_file = setting + "/" + project + "_analyzer.csv"
        handle_io(input_file, output_file)
