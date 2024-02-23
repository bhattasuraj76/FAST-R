"""
Computes budget statistics for all the projects
"""
from utils import *
import json
import numpy as np

from config import ROOT_DIR
from helpers import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
    get_deleted_testfiles_in_test_deletion_commit_parent,
    get_no_of_deleted_testfiles_in_test_deletion_commit_parent,
)

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

if __name__ == "__main__":
    for index, prog in enumerate(projects_list):
        commits_list = get_whole_file_test_deletion_parent_commits(prog)

        # Strict Scenario
        MIN_PERCENTAGE_OF_TEST_PRESERVED = 100
        MIN_PERCENTAGE_OF_TEST_PRESERVED_F = 100.00
        ALL_BUDGETS = []
        ALL_BUDGETS_F = []
        for commit in commits_list:
            commit = strip_commit_url(commit)
            # IGNORE 100% TEST DELETION CASE OF COMMONS-MATH FROM STUDY
            if (
                prog == "commons-math"
                and commit == "e389289e779612c5930d7c292bbbc94027695ae5"
            ):
                continue

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
            repetitionsF = float(
                no_of_preserved_testfiles / numOfTCS * 100
            )  # Final budget in percentage[no. of testcases remaining]
            # print("Computed Repetitions(% budget): ", repetitions)

            if repetitions <= MIN_PERCENTAGE_OF_TEST_PRESERVED:
                MIN_PERCENTAGE_OF_TEST_PRESERVED = repetitions
                MIN_PERCENTAGE_OF_TEST_PRESERVED_F = repetitionsF
                min_data = {
                    "numOfTCS": numOfTCS,
                    "no_of_deleted_testfiles": no_of_deleted_testfiles,
                    "hash": commit,
                }
            ALL_BUDGETS.append(repetitions)
            ALL_BUDGETS_F.append(repetitionsF)

        # Loose Scenario
        if MIN_PERCENTAGE_OF_TEST_PRESERVED <= 100:
            # print("Budget:" , MIN_PERCENTAGE_OF_TEST_PRESERVED)
            LOOSE_BUDGET[prog] = {
                "Min Budget": MIN_PERCENTAGE_OF_TEST_PRESERVED,
                "Min Budget F": MIN_PERCENTAGE_OF_TEST_PRESERVED_F,
                "Min data": min_data,
                "Max Budget": int(np.max(ALL_BUDGETS)),
                "Max Budget F": float(np.max(ALL_BUDGETS_F)),
                "Average Budget": int(np.mean(ALL_BUDGETS)),
                "Average Budget F": float(np.mean(ALL_BUDGETS_F)),
            }

        print("================================================================")

    f = open(f"./stat_loose_budget.json", "w")
    f.write(json.dumps(LOOSE_BUDGET, indent=2))
