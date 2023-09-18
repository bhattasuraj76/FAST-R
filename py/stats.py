"""
This is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this source.  If not, see <http://www.gnu.org/licenses/>.
"""


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
import numpy as np

# Redirect console ouput to a file
sys.stdout = open("./stat.txt", "w")


ROOT_DIR = "../cts-analyzer/io/rq3"
VALIDATION_DIR = "../cts-analyzer/io/validationFiles"


def get_deleted_testcases_with_whole_file_df(project):
    validated_tests_file_path = Path(f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv")
    if not os.path.exists(f"{validated_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            validated_tests_file_path,
        )
        exit()

    df = pd.read_csv(validated_tests_file_path)
    deleted_tc_with_whole_file_df = df[df["Deleted With Whole File"] == "yes"]
    return deleted_tc_with_whole_file_df


def print_stats(project):
    deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
    print("Total deleted testcases with whole file: ", len(deleted_tc_df))
    unique_deleted_testcases_df = deleted_tc_df[
        ["Parent", "Filepath", "Removed Test Case"]
    ].drop_duplicates()
    print(
        "Total Unique testcases deleted with whole file: ",
        len(unique_deleted_testcases_df),
    )

    # Condensed formula; useful in future
    # unique_deleted_testcase_with_whole_file_df = deleted_tc_df.loc[
    #     deleted_tc_df["Deleted With Whole File"] == "yes",
    #     ["Parent", "Filepath", "Removed Test Case"],
    # ].drop_duplicates()
    # print( "Total Unique testcases deleted with whole file: ", len(unique_deleted_testcase_with_whole_file_df))

    unique_deleted_testfile_df = deleted_tc_df[["Parent", "Filepath"]].drop_duplicates()
    print("Total Unique testclass files deleted: ", len(unique_deleted_testfile_df))
    whole_file_test_deletion_parent_commits_df = deleted_tc_df[
        ["Parent"]
    ].drop_duplicates()
    print("Total parent commits: ", len(whole_file_test_deletion_parent_commits_df))


def get_whole_file_test_deletion_parent_commits(project):
    deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
    commits_list = list(set(list(deleted_tc_df["Parent"])))
    return commits_list


def get_deleted_testfiles_in_test_deletion_commit_parent(project, parent_commit):
    deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
    parsed_commit = parse_commit_as_hyperlink_by_project(project, parent_commit)
    deleted_tc_in_commit_df = deleted_tc_df[deleted_tc_df["Parent"] == parsed_commit]
    classes_deleted = list(set(list(deleted_tc_in_commit_df["Filepath"])))
    return classes_deleted


def get_no_of_deleted_testfiles_in_test_deletion_commit_parent(project, parent_commit):
    classes_deleted = get_deleted_testfiles_in_test_deletion_commit_parent(
        project, parent_commit
    )
    return len(classes_deleted)


LOOSE_BUDGET = {}
projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

for index, prog in enumerate(projects_list):
    print(prog)
    print_stats(prog)
    print("-----------------------")
    commits_list = get_whole_file_test_deletion_parent_commits(prog)

    # Strict Scenario
    MIN_PERCENTAGE_OF_TEST_PRESERVED = 100
    MIN_PERCENTAGE_OF_TEST_PRESERVED_HASH = ''
    ALL_BUDGETS= []
    for commit in commits_list:
        commit = strip_commit_url(commit)
        inputFile = "{}/all_commits_all_testcases/{}/{}-{}-ts.txt".format(
            ROOT_DIR, prog, prog, commit
        )

        numOfTCS = sum(
            (1 for _ in open(inputFile))
        )  # Total no. of testclass in particular commit history
        no_of_deleted_testfiles = (
            get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
        )
        no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
        # print("Total test files: ", numOfTCS)
        # print("No. of deleted test files: ", no_of_deleted_testfiles)
        # print("No. of preserved test files: ", no_of_preserved_testfiles)
        repetitions = int(
            no_of_preserved_testfiles / numOfTCS * 100
        )  # Final budget in percentage[no. of testcases remaining]
        # print("Computed Repetitions(% budget): ", repetitions)

        if repetitions < MIN_PERCENTAGE_OF_TEST_PRESERVED:
            MIN_PERCENTAGE_OF_TEST_PRESERVED = repetitions
            MIN_PERCENTAGE_OF_TEST_PRESERVED_HASH = commit
        ALL_BUDGETS.append(repetitions)
    # Loose Scenario
    if MIN_PERCENTAGE_OF_TEST_PRESERVED < 100:
        # print("Budget:" , MIN_PERCENTAGE_OF_TEST_PRESERVED)
        LOOSE_BUDGET[prog] = {
            "Min Budget": MIN_PERCENTAGE_OF_TEST_PRESERVED,
            "Min Budget Hash " : MIN_PERCENTAGE_OF_TEST_PRESERVED_HASH,
            "No. of test class files": numOfTCS,
            "No. of deleted testfiles": no_of_deleted_testfiles,
            "Max Budget": int(np.max(ALL_BUDGETS)),
            "Average Budget": int(np.mean(ALL_BUDGETS))
        }

    print("================================================================")


f = open(f"./stat_loose_budget.json", "w")
f.write(json.dumps(LOOSE_BUDGET, indent=2))
