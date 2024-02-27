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
    deleted_tc_with_whole_file_df = df[df["Deleted With Whole File"] == "yes"]
    return deleted_tc_with_whole_file_df


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


def get_deleted_obsolete_and_redundant_testcases_by_project_and_removedfilepath(project, commit, filepath):
    validated_tests_file_path = Path(f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv")
    if not os.path.exists(f"{validated_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            validated_tests_file_path,
        )

    df = pd.read_csv(validated_tests_file_path)
    parsed_commit = parse_commit_as_hyperlink_by_project(project, commit)
    
    deleted_tc_commit_df = df[df["Parent"] == parsed_commit]
    filepath_csv = filepath[2:] #remove "./" from filepath to match records in csv file
    deleted_tc_with_whole_file_df = deleted_tc_commit_df[deleted_tc_commit_df["Filepath"] == filepath_csv]
    deleted_tc_with_source_df = deleted_tc_with_whole_file_df[deleted_tc_with_whole_file_df["Deleted With Source Code"] == "yes"]
    deleted_tc_without_source_df = deleted_tc_with_whole_file_df[deleted_tc_with_whole_file_df["Deleted With Source Code"] == "no"]
    return deleted_tc_with_source_df, deleted_tc_without_source_df