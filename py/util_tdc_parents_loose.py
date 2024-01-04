# Export whole file test deletion parent commits

import json
from functools import reduce
from helpers import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
)
from math import fsum
import pandas as pd
import os

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]


def export_test_deletion_parent_commits(commits, deleted_testcases_with_whole_file):
    data = {
        "Child Commit Recent Date": [],
        "Parent": [],
        "Total Deleted Testfile": [],
        "Deleted Testfile": [],
        "Total Deleted Tests": [],
        "Deleted Tests": [],
    }
    for commit in commits:
        deleted_tests_df = deleted_testcases_with_whole_file[
            deleted_testcases_with_whole_file["Parent"] == commit
        ]
        datetime = deleted_tests_df["Datetime"].max()
        data["Child Commit Recent Date"].append(datetime)
        data["Parent"].append(commit)
        # deleted testfiles
        deleted_test_files = list(set(deleted_tests_df["Filepath"].values.tolist()))
        data["Total Deleted Testfile"].append(len(deleted_test_files))
        data["Deleted Testfile"].append(deleted_test_files)
        # deleted tests
        deleted_tests = deleted_tests_df["Removed Test Case"].values.tolist()
        data["Total Deleted Tests"].append(len(deleted_tests))
        data["Deleted Tests"].append(deleted_tests)

    df = pd.DataFrame(data)
    df["Child Commit Recent Date"] = pd.to_datetime(
        df["Child Commit Recent Date"], errors="coerce"
    )
    df.sort_values(by=["Child Commit Recent Date"], inplace=True)
    if not os.path.exists("tdc-parents-sample"):
        os.mkdir("tdc-parents-sample")
    df.to_csv(f"tdc-parents-sample/{project}_loose.csv", index=False)


for index, project in enumerate(projects_list):
    print(project)
    print("--------")
    commits_list = get_whole_file_test_deletion_parent_commits(project)
    deleted_testcases_with_whole_file_df = get_deleted_testcases_with_whole_file_df(
        project
    )

    # Look for only redundant and obsolete tests[recent, deleted with whole file, deleted with or without out source code]
    export_test_deletion_parent_commits(
        commits_list, deleted_testcases_with_whole_file_df
    )
