""" Prints stats ignore the 100 percent test deletion commit in commons-math"""
import sys
from pathlib import Path
import pandas as pd
from utils import *

import numpy as np
from util_budget import get_deleted_testcases_with_whole_file_df

# Redirect console ouput to a file
sys.stdout = open("./stats_refine_log.txt", "w")


def print_stats(project):
    deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
    
    if project == "commons-math":
        parsed_hash = parse_commit_as_hyperlink_by_project(project, "e389289e779612c5930d7c292bbbc94027695ae5")
        deleted_tc_df = deleted_tc_df[deleted_tc_df["Hash"] != parsed_hash]
        
    print("Total deleted testcases with whole file: ", len(deleted_tc_df))
    unique_deleted_testcases_df = deleted_tc_df[
        ["Hash", "Filepath", "Removed Test Case"]
    ].drop_duplicates()
    print(
        "Total Unique testcases deleted with whole file: ",
        len(unique_deleted_testcases_df),
    )
    
    # To get parent TDC with multiple children TDC [sorting]
    # df = deleted_tc_df.drop_duplicates(subset=['Parent', 'Hash'], keep='first')
    # df = df.groupby(['Parent']).size().sort_values(ascending=False)
    # print(df)

    # Condensed formula; useful in future
    # unique_deleted_testcase_with_whole_file_df = deleted_tc_df.loc[
    #     deleted_tc_df["Deleted With Whole File"] == "yes",
    #     ["Hash", "Filepath", "Removed Test Case"],
    # ].drop_duplicates()
    # print( "Total Unique testcases deleted with whole file: ", len(unique_deleted_testcase_with_whole_file_df))

    unique_deleted_testfile_df = deleted_tc_df[["Hash", "Filepath"]].drop_duplicates()
    print("Total Unique testclass files deleted: ", len(unique_deleted_testfile_df))
    unique_whole_file_tdc_df = deleted_tc_df[["Hash"]].drop_duplicates()
    print("Total test deletion commits deleting whole file: ", len(unique_whole_file_tdc_df))
    unique_whole_file_test_deletion_parent_commits_df = deleted_tc_df[
        ["Parent"]
    ].drop_duplicates()
    total = len(unique_whole_file_test_deletion_parent_commits_df)
    commits_list = list(unique_whole_file_test_deletion_parent_commits_df["Parent"])
    print("Total parent commits: ", total)
    print("Parent commit 2%: ", commits_list[round(0.02*total)])
    print("Parent commit 5%: ", commits_list[round(0.05*total)])
    print("Parent commit 10%: ", commits_list[round(0.1*total)])
    print("Parent commit 15%: ", commits_list[round(0.15*total)])
    print("Parent commit 25%: ", commits_list[round(0.25*total)])
    print("Parent commit 50%: ", commits_list[round(0.5*total)])
    print("Parent commit 75%: ", commits_list[round(0.75*total)])
    print("Parent commit 100%: ", commits_list[-1])
    
    
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

    


