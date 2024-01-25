import json
from functools import reduce
from helpers import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
)
from math import fsum
import pandas as pd
import os
from datetime import timedelta

algos = ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]
projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]
data = {"strict": {}, "loose": {}}


for index, project in enumerate(projects_list):
    loose_file = open(f"./output-loose/{project}_analyzer.json")
    strict_file = open(f"./output-strict/{project}_analyzer.json")
    algo_analyzer_strict = json.load(strict_file)
    algo_analyzer_loose = json.load(loose_file)

    commits_list = get_whole_file_test_deletion_parent_commits(project)
    print("Total whole file test deletion parent commits:", len(commits_list))

    deleted_testcases_with_whole_file = get_deleted_testcases_with_whole_file_df(
        project
    )
    print(
        "Total test cases deleted with whole file:",
        len(deleted_testcases_with_whole_file),
    )

    for index, algo in enumerate(algos):

        def parse_results(setting):
            data_to_look = (
                algo_analyzer_strict if setting == "strict" else algo_analyzer_loose
            )

            total_detected = 0
            total_failed_to_detect = 0
            total_execution_time = 0
            total_preparation_time = 0
            total_preparation_time_arr = []
            total_execution_time_arr = []
            for algo_analyzer_commit in data_to_look["details"]:
                alog_analyzer_commit_each_algo = algo_analyzer_commit["Algorithm"][algo]
                total_detected += alog_analyzer_commit_each_algo[
                    "Total Detected Deleted Testfiles"
                ]
                total_failed_to_detect += alog_analyzer_commit_each_algo[
                    "Total Failed To Detect Deleted Testfiles"
                ]

                # if index == 0:
                #     total_preparation_time = timedelta(seconds = alog_analyzer_commit_each_algo["Total preparation time"])
                #     total_execution_time = timedelta(seconds = alog_analyzer_commit_each_algo["Total execution time"])
                # else:
                #     total_preparation_time = total_preparation_time + timedelta(seconds = alog_analyzer_commit_each_algo["Total preparation time"])
                #     total_preparation_time = total_preparation_time + timedelta(seconds = alog_analyzer_commit_each_algo["Total execution time"])

                total_preparation_time_arr.append(
                    round(alog_analyzer_commit_each_algo["Total preparation time"], 3)
                )
                total_execution_time_arr.append(
                    round(alog_analyzer_commit_each_algo["Total execution time"], 3)
                )
                
            # try:
            #     total_preparation_time = str(timedelta(seconds=total_preparation_time))
            #     total_execution_time = str(timedelta(seconds=total_execution_time))
            # except:
            #     pass
                
            total_preparation_time = fsum(
                total_preparation_time_arr,
            )
            total_execution_time = fsum(
                total_execution_time_arr,
            )
            print("Total Preparation Time")
            print(total_preparation_time)
            print("Total Execution Time")
            print(total_execution_time)

            if project not in data[setting]:
                data[setting][project] = {}

         

            data[setting][project][algo] = (
                {
                    "Total Detected Deleted Testfiles": total_detected,
                    "Total Failed To Detect Deleted Testfiles": total_failed_to_detect,
                    "Total Preparation Time": str(timedelta(seconds=total_preparation_time)),
                    "Total Execution Time": str(timedelta(seconds=total_execution_time)),
                },
            )

        # Handle strict scenario
        parse_results("loose")
        # Handle loose scenario
        parse_results("strict")


f = open("./output-final/final_analyzer.json", "w")
f.write(json.dumps(data, indent=2))
