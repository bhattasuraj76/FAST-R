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
from util_budget import get_deleted_testcases_with_whole_file_df

# Redirect console ouput to a file
sys.stdout = open("./stat.txt", "w")


ROOT_DIR = "../cts-analyzer/io/rq3"
VALIDATION_DIR = "../cts-analyzer/io/validationFiles"



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
    unique_tdc_df = deleted_tc_df[["Hash"]].drop_duplicates()
    print("Total test deletion commits deleting whole file: ", len(unique_tdc_df))
    whole_file_test_deletion_parent_commits_df = deleted_tc_df[
        ["Parent"]
    ].drop_duplicates()
    print("Total parent commits: ", len(whole_file_test_deletion_parent_commits_df))



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

    


