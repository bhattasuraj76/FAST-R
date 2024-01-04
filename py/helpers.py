import os
from pathlib import Path
import pandas as pd
from utils import *
import json
import logging
from timeit import default_timer as timer
from datetime import timedelta
from config import VALIDATION_DIR

def get_deleted_testcases_with_whole_file_df(project):
    validated_tests_file_path = Path(f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv")
    if not os.path.exists(f"{validated_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            validated_tests_file_path,
        )
        exit()

    df = pd.read_csv(validated_tests_file_path)
    print("Total deleted testcases", len(df))
    deleted_tc_with_whole_file_df = df[df["Deleted With Whole File"] == "yes"]
    print("Total deleted testcases with whole file", len(deleted_tc_with_whole_file_df))
    return deleted_tc_with_whole_file_df


def get_whole_file_test_deletion_parent_commits(project):
    deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
    commits_list = list(set(list(deleted_tc_df["Parent"])))
    print("Total whole file test deletion parent commits:", len(commits_list))
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



# import os
# from pathlib import Path
# import pandas as pd
# from utils import *
# import json
# import logging
# from timeit import default_timer as timer
# from datetime import timedelta
# from config import VALIDATION_DIR

# def get_deleted_testcases_df(project):
#     validated_tests_file_path = Path(f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv")
#     if not os.path.exists(f"{validated_tests_file_path}"):
#         print(
#             "Error: path does not exit -> ",
#             validated_tests_file_path,
#         )
#         exit()

#     df = pd.read_csv(validated_tests_file_path)
#     print("Total deleted testcases", len(df))
#     return df


# def get_whole_file_test_deletion_parent_commits(project):
#     commits_list = get_test_deletion_parent_commits_list(project, deleted_with_whole_file=True)
#     return commits_list

# def get_test_deletion_parent_commits_list(project, deleted_with_whole_file=None, deleted_with_source_code=None):
#     deleted_tc_df = get_deleted_testcases_df(project)
    
#     if deleted_with_whole_file == True:
#         deleted_tc_df = deleted_tc_df[deleted_tc_df["Deleted With Whole File"] == "yes"]
        
#     if deleted_with_source_code == True:
#         deleted_tc_df = deleted_tc_df[deleted_tc_df["Deleted With Source Code"] == "yes"]

#     commits_list = list(set(list(deleted_tc_df["Parent"])))
#     print("Total parent commits:", len(commits_list))
#     return commits_list

# def get_deleted_testfiles_in_test_deletion_commit_parent(project, parent_commit):
#     deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
#     parsed_commit = parse_commit_as_hyperlink_by_project(project, parent_commit)
#     deleted_tc_in_commit_df = deleted_tc_df[deleted_tc_df["Parent"] == parsed_commit]
#     classes_deleted = list(set(list(deleted_tc_in_commit_df["Filepath"])))
#     return classes_deleted


# def get_no_of_deleted_testfiles_in_test_deletion_commit_parent(project, parent_commit):
#     classes_deleted = get_deleted_testfiles_in_test_deletion_commit_parent(
#         project, parent_commit
#     )
#     return len(classes_deleted)
