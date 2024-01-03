"""
This file is modified version of experimentBudget.py to runs all FAST-R algorithms (fastr_adequate.py) 
in the Budget scenario and in all commit state of target project.
"""

import math
import os
import pickle
import sys
import competitors
import fastr
import metric
from pathlib import Path
from utils import strip_commit_url
import json
from config import REPEATS, ROOT_DIR
from helpers import (
    get_whole_file_test_deletion_parent_commits,
    get_no_of_deleted_testfiles_in_test_deletion_commit_parent,
)

# Pre-computed budget for loose setting
import json

all_projects_loose_budget = json.load(open(f"./stat_loose_budget.json"))


def main(prog, setting):
    commits_list = get_whole_file_test_deletion_parent_commits(prog)

    # Strict Scenario
    if setting == "strict":
        for commit in commits_list:
            commit = strip_commit_url(commit)
            directory = "{}/outputBudgetStrict/{}/{}/".format(ROOT_DIR, prog, commit)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(directory + "selections/"):
                os.makedirs(directory + "selections/")
            if not os.path.exists(directory + "measures/"):
                os.makedirs(directory + "measures/")

            # FAST-R parameters
            k, n, r, b = 5, 10, 1, 10
            dim = 10

            # FAST-f sample size
            def all_(x):
                return x

            def sqrt_(x):
                return int(math.sqrt(x)) + 1

            def log_(x):
                return int(math.log(x, 2)) + 1

            def one_(x):
                return 1

            inputFile = "{}/all_commits_all_testcases/{}/{}-{}-ts.txt".format(
                ROOT_DIR, prog, prog, commit
            )
            outpath = "{}/outputBudgetStrict/{}/{}/".format(ROOT_DIR, prog, commit)
            sPath = outpath + "selections/"
            tPath = outpath + "measures/"

            numOfTCS = sum(
                (1 for _ in open(inputFile))
            )  # Total no. of testclass in particular commit history
            no_of_deleted_testfiles = (
                get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
            )
            no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
            print("Total test files: ", numOfTCS)
            print("No. of deleted test files: ", no_of_deleted_testfiles)
            print("No. of preserved test files: ", no_of_preserved_testfiles)

            # Final budget[no. of testcases remaining] in percentage
            # Repetition => [step size i.e increases from 1%-30% in FAST-R]
            repetitions = int(no_of_preserved_testfiles / numOfTCS * 100)
            print("Computed Repetitions: ", repetitions)

            # for reduction in range(1, repetitions+1):
            # Current budget for each step[step size increases from 1%-30%]
            # B = int(numOfTCS * reduction / 100)

            # Budget(actual number of tests preserved) is fixed in loose scenario
            # B = int(numOfTCS * repetitions / 100) # Commenting this because no. of actual tests deleted is not equal to percentage B
            B = no_of_preserved_testfiles
            
            # reduction (percentage of test preserved)
            reduction = repetitions

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST++", reduction, run + 1)
                tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST++", reduction, run + 1)
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fastPlusPlus(inputFile, dim=dim, B=B)
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST++", reduction, pTime, rTime, run)

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-CS", reduction, run + 1)
                tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-CS", reduction, run + 1)
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fastCS(inputFile, dim=dim, B=B)
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST-CS", reduction, pTime, rTime, run)

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-pw", reduction, run + 1)
                tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-pw", reduction, run + 1)
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fast_pw(
                    inputFile, r, b, bbox=True, k=k, memory=True, B=B
                )
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST-pw", reduction, pTime, rTime, run)

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(
                    sPath, "FAST-all", reduction, run + 1
                )
                tOut = "{}/{}-{}-{}.pickle".format(
                    tPath, "FAST-all", reduction, run + 1
                )
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fast_(
                    inputFile, all_, r=r, b=b, bbox=True, k=k, memory=True, B=B
                )
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST-all", reduction, pTime, rTime, run)

    # Loose Scenario
    if setting == "loose":
        # Budget for loose scenario
        MIN_PERCENTAGE_OF_TEST_PRESERVED = all_projects_loose_budget[prog]["Min Budget"]

        for commit in commits_list:
            commit = strip_commit_url(commit)
            directory = "{}/outputBudgetLoose/{}/{}/".format(ROOT_DIR, prog, commit)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(directory + "selections/"):
                os.makedirs(directory + "selections/")
            if not os.path.exists(directory + "measures/"):
                os.makedirs(directory + "measures/")

            # FAST-R parameters
            k, n, r, b = 5, 10, 1, 10
            dim = 10

            # FAST-f sample size
            def all_(x):
                return x

            def sqrt_(x):
                return int(math.sqrt(x)) + 1

            def log_(x):
                return int(math.log(x, 2)) + 1

            def one_(x):
                return 1

            inputFile = "{}/all_commits_all_testcases/{}/{}-{}-ts.txt".format(
                ROOT_DIR, prog, prog, commit
            )
            outpath = "{}/outputBudgetLoose/{}/{}/".format(ROOT_DIR, prog, commit)
            sPath = outpath + "selections/"
            tPath = outpath + "measures/"

            numOfTCS = sum(
                (1 for _ in open(inputFile))
            )  # Total no. of testclass in particular commit history
            no_of_deleted_testfiles = (
                get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
            )
            no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
            print("Total test files: ", numOfTCS)
            print("No. of deleted test files: ", no_of_deleted_testfiles)
            print("No. of preserved test files: ", no_of_preserved_testfiles)

            # Final budget[no. of testcases remaining] in percentage; # STRICT SCENARIO
            repetitions = int(no_of_preserved_testfiles / numOfTCS * 100)
            print("Computed Repetitions: ", repetitions)

            # Budget(actual number of tests preserved) is fixed in loose scenario
            B = int(numOfTCS * MIN_PERCENTAGE_OF_TEST_PRESERVED / 100)
            # reduction (percentage of test preserved)
            reduction = MIN_PERCENTAGE_OF_TEST_PRESERVED

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST++", reduction, run + 1)
                tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST++", reduction, run + 1)
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fastPlusPlus(inputFile, dim=dim, B=B)
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST++", reduction, pTime, rTime)

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-CS", reduction, run + 1)
                tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-CS", reduction, run + 1)
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fastCS(inputFile, dim=dim, B=B)
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST-CS", reduction, pTime, rTime)

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-pw", reduction, run + 1)
                tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-pw", reduction, run + 1)
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fast_pw(
                    inputFile, r, b, bbox=True, k=k, memory=True, B=B
                )
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST-pw", reduction, pTime, rTime)

            for run in range(REPEATS):
                sOut = "{}/{}-{}-{}.pickle".format(
                    sPath, "FAST-all", reduction, run + 1
                )
                tOut = "{}/{}-{}-{}.pickle".format(
                    tPath, "FAST-all", reduction, run + 1
                )
                if os.path.exists(sOut) and os.path.exists(tOut):
                    continue
                pTime, rTime, sel = fastr.fast_(
                    inputFile, all_, r=r, b=b, bbox=True, k=k, memory=True, B=B
                )
                pickle.dump(sel, open(sOut, "wb"))
                pickle.dump((pTime, rTime), open(tOut, "wb"))
                print("FAST-all", reduction, pTime, rTime)
