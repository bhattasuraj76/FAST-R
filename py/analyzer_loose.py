import math
import os
import pickle
import sys

import competitors
import fastr
import metric
from pathlib import Path
import pandas as pd
from utils import *
import json

all_projects_loose_budget = json.load(open(f'./stat_loose_budget.json')) 


from experimentBudgetModified import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
    get_deleted_testfiles_in_test_deletion_commit_parent,
    ROOT_DIR, REPEATS
)

"""
This file analyzes the reduced test suite and computes the success ratio for all Fast-R algorithms 
comparing with developer reduced test sutie in loose scenario.
"""


def get_line_no_history_deleted_testfiles(program, commit, deleted_testfiles):
    testcase_history_file_path = (
        "{}/all_commits_all_testcases/{}/{}-{}-tsh.json".format(
            ROOT_DIR, program, program, commit
        )
    )
    testcase_history = json.load(open(testcase_history_file_path))
    # print(testcase_history)
    line_no = []
    for deleted_testfile in deleted_testfiles:
        testfilepath = "./" + deleted_testfile
        
        if testfilepath in testcase_history:
            line_no.append(testcase_history[testfilepath])
        else:
            print("deleted file not found in TSH JSON")
            print(deleted_testfile, testfilepath, program, commit)
    return line_no


projects_list = [
     "commons-lang",
     "gson",
     "commons-math",
     "jfreechart",
     "joda-time",
     "pmd",
     "cts" 
]


for index, prog in enumerate(projects_list):
    if prog == "cts":
        REPEATS = 1
    analyzer_data = {}

    commits_list = get_whole_file_test_deletion_parent_commits(prog)
    print("Total whole file test deletion parent commits:", len(commits_list))
    analyzer_data["Total test deletion parent commits:"] = len(commits_list)
    
    deleted_testcases_with_whole_file = get_deleted_testcases_with_whole_file_df(prog)
    print("Total test cases deleted with whole file:", len(deleted_testcases_with_whole_file))
    analyzer_data["Total test cases deleted with whole file:"] = len(deleted_testcases_with_whole_file)
    
    analyzer_data["details"] = []
    for index, commit in enumerate(commits_list):
        commit = strip_commit_url(commit)
        directory = "{}/outputBudgetLoose/{}/{}/".format(ROOT_DIR, prog, commit)
        selection_dir = directory + "selections"
        measurement_dir = directory + "measures"

        testcase_history_file = "{}/all_commits_all_testcases/{}/{}-{}-tsh.txt".format(
            ROOT_DIR, prog, prog, commit
        )
        testcase_file = "{}/all_commits_all_testcases/{}/{}-{}-ts.txt".format(
            ROOT_DIR, prog, prog, commit
        )

        numOfTCS = sum(
            (1 for _ in open(testcase_file))
        )  # Total no. of testclass in particular parent_commit history
        print("Total test files: ", numOfTCS)

        deleted_testfiles = get_deleted_testfiles_in_test_deletion_commit_parent(
            prog, commit
        )
        no_of_deleted_testfiles = len(deleted_testfiles)
        print("Total no. of deleted test files: ", no_of_deleted_testfiles)

        deleted_testfiles_line_no_history = get_line_no_history_deleted_testfiles(
            prog, commit, deleted_testfiles
        )
        no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
        print("No. of preserved test files: ", no_of_preserved_testfiles)
        FINAL_BUDGET = all_projects_loose_budget[prog]["Min Budget"] # Final budget[no. of testcases remaining] in percentage is fixed for loose scenario
        print("Computed Final Budget: ", FINAL_BUDGET)
        
        algo_data = {}
        for algo in ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]:
            selection_path = "{}/{}-{}-{}.pickle".format(
                selection_dir, algo, FINAL_BUDGET, REPEATS
            )
            measurement_path = "{}/{}-{}-{}.pickle".format(
                measurement_dir, algo, FINAL_BUDGET, REPEATS
            )
            with open(selection_path, "rb") as pickle_file:
                reduced_testfiles_line_no = pickle.load(pickle_file)

            # Check if removed testfile from parent commit exists in reduced testsuite
            # Increase no. of detected deleted testfiles if does not exist
            no_of_detected_deleted_testfiles = 0
            detected_deleted_testfiles_line_no = []
            for deleted_each_testfiles_line_no in deleted_testfiles_line_no_history:
                if deleted_each_testfiles_line_no not in reduced_testfiles_line_no:
                    no_of_detected_deleted_testfiles += 1
                    detected_deleted_testfiles_line_no.append(deleted_each_testfiles_line_no)
            no_of_failed_to_detect_deleted_testfiles = (
                no_of_deleted_testfiles - no_of_detected_deleted_testfiles
            )

            reduction_info = {
                "Total Detected Deleted Testfiles": no_of_detected_deleted_testfiles,
                "Total Failed To Detect Deleted Testfiles": no_of_failed_to_detect_deleted_testfiles,
                "Detected Testfiles Line No": detected_deleted_testfiles_line_no
            }
            algo_data[algo] = reduction_info

        analyzer_data["details"].append(
            {
                "Parent": commit,
                "Total Testfiles": numOfTCS,
                "Total Deleted Testfiles": no_of_deleted_testfiles,
                "Total Preserved Testfiles": no_of_preserved_testfiles,
                "Computed Final Budget": FINAL_BUDGET,
                "Algorithm": algo_data,
            }
        )

        f = open(f"./output-loose/{prog}_analyzer.json", "w")
        f.write(json.dumps(analyzer_data,  indent=2))
