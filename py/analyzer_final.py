import json
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
parent_commits = {
    "commons-lang": 38,
    "gson": 23,
    "commons-math": 104,
    "jfreechart": 9,
    "joda-time": 7,
    "pmd": 137,
    "cts": 423,
}
data = {"strict": {}, "loose": {}}


for index, project in enumerate(projects_list):
    loose_file = open(f"./output-loose/{project}_analyzer.json")
    strict_file = open(f"./output-strict/{project}_analyzer.json")
    algo_analyzer_strict = json.load(strict_file)
    algo_analyzer_loose = json.load(loose_file)

    for index, algo in enumerate(algos):

        def parse_results(setting):
            data_to_look = (
                algo_analyzer_strict if setting == "strict" else algo_analyzer_loose
            )

            total_detected = 0
            total_failed_to_detect = 0
            total_detected_deleted_and_redundant_tests = 0
            total_detected_obsolete_and_redundant_tests = 0

            # Takes into account all the 50 iterations for reducing test suite
            total_preparation_time = 0
            total_execution_time = 0
            total_avg_preparation_time = 0
            total_avg_execution_time = 0
            total_preparation_time_arr = []
            total_execution_time_arr = []

            # Takes into account only 1(optimal) iteration for reducing test suite
            total_optimal_preparation_time = 0
            total_optimal_execution_time = 0
            total_avg_optimal_preparation_time = 0
            total_avg_optimal_execution_time = 0
            total_optimal_preparation_time_arr = []
            total_optimal_execution_time_arr = []

            for algo_analyzer_commit in data_to_look["details"]:
                alog_analyzer_commit_each_algo = algo_analyzer_commit["Algorithm"][algo]
                total_detected += alog_analyzer_commit_each_algo[
                    "Total Detected Deleted Testfiles"
                ]
                total_failed_to_detect += alog_analyzer_commit_each_algo[
                    "Total Failed To Detect Deleted Testfiles"
                ]

                # Takes into account all the 50 iterations for reducing test suite
                total_preparation_time_arr.append(
                    round(alog_analyzer_commit_each_algo["Total preparation time"], 3)
                )
                total_execution_time_arr.append(
                    round(alog_analyzer_commit_each_algo["Total execution time"], 3)
                )

                # Takes into account only 1(optimal) iteration for reducing test suite
                total_optimal_preparation_time_arr.append(
                    round(alog_analyzer_commit_each_algo["Optimal preparation time"], 3)
                )
                total_optimal_execution_time_arr.append(
                    round(alog_analyzer_commit_each_algo["Optimal execution time"], 3)
                )

                total_failed_to_detect += alog_analyzer_commit_each_algo[
                    "Total Failed To Detect Deleted Testfiles"
                ]

                
                # Total detected deleted obsolete and redundant tests
                total_detected_obsolete_and_redundant_tests += (
                    alog_analyzer_commit_each_algo[
                        "Total Detected Deleted And Obsolete Tests"
                    ]
                )
                total_detected_deleted_and_redundant_tests += (
                    alog_analyzer_commit_each_algo[
                        "Total Detected Deleted And Redundant Tests"
                    ]
                )
                

            # Takes into account all the 50 iterations for reducing test suite
            total_preparation_time = fsum(
                total_preparation_time_arr,
            )
            total_execution_time = fsum(
                total_execution_time_arr,
            )
            total_avg_preparation_time = total_preparation_time / (
                parent_commits[project] * 50
            )
            total_avg_execution_time = total_execution_time / (
                parent_commits[project] * 50
            )

            print("Total Preparation Time")
            print(total_preparation_time)
            print("Total Execution Time")
            print(total_execution_time)

            # Takes into account only 1(optimal) iteration for reducing test suite
            total_optimal_preparation_time = fsum(
                total_optimal_preparation_time_arr,
            )
            total_optimal_execution_time = fsum(
                total_optimal_execution_time_arr,
            )
            total_avg_optimal_preparation_time = total_optimal_preparation_time / (
                parent_commits[project]
            )
            total_avg_optimal_execution_time = total_optimal_execution_time / (
                parent_commits[project]
            )

            print("Total Optimal Preparation Time")
            print(total_optimal_preparation_time)
            print("Total Optimal Execution Time")
            print(total_optimal_execution_time)

            if project not in data[setting]:
                data[setting][project] = {}

            data[setting][project][algo] = (
                {
                    "Total Detected Deleted Testfiles": total_detected,
                    "Total Failed To Detect Deleted Testfiles": total_failed_to_detect,
                    "Total Detected Deleted And Redundant Tests": total_detected_deleted_and_redundant_tests,
                    "Total Detected Obsolete And Redundant Tests": total_detected_obsolete_and_redundant_tests,
                    "Total Preparation Time": str(
                        timedelta(seconds=total_preparation_time)
                    ),
                    "Total Execution Time": str(
                        timedelta(seconds=total_execution_time)
                    ),
                    "Total Avg Preparation Time": str(
                        timedelta(seconds=total_avg_preparation_time)
                    ),
                    "Total Avg Execution Time": str(
                        timedelta(seconds=total_avg_execution_time)
                    ),
                    "Total Optimal Preparation Time": str(
                        timedelta(seconds=total_preparation_time)
                    ),
                    "Total Optimal Execution Time": str(
                        timedelta(seconds=total_execution_time)
                    ),
                    "Total Avg Optimal Preparation Time": str(
                        timedelta(seconds=total_avg_optimal_preparation_time)
                    ),
                    "Total Avg Optimal Execution Time": str(
                        timedelta(seconds=total_avg_optimal_execution_time)
                    ),
                    "Total Avg Optimal Preparation Time(U)": str(
                        timedelta(
                            seconds=total_avg_optimal_preparation_time
                        ).microseconds
                    ),
                    "Total Avg Optimal Execution Time(U)": str(
                        timedelta(seconds=total_avg_optimal_execution_time).microseconds
                    ),
                    "Total Avg Optimal Time(U)": str(
                        timedelta(
                            seconds=(
                                total_avg_optimal_preparation_time
                                + total_avg_optimal_execution_time
                            )
                        ).microseconds
                    ),
                },
            )

        # Handle strict scenario
        parse_results("loose")
        # Handle loose scenario
        parse_results("strict")


f = open("./output-final/final_analyzer.json", "w")
f.write(json.dumps(data, indent=2))
