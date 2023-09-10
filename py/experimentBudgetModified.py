'''
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
'''

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

"""
This file runs all FAST-R algorithms (fastr_adequate.py) 
in the Budget scenario and in all commit state of target project.
"""


usage = """USAGE: python3 py/experimentBudget.py <program> 
OPTIONS:
  <program>: the target project.
    options: commons-lang, gson, commons-math, jfreechart, joda-time, cts
  """

ROOT_DIR = "../cts-analyzer/io/rq3"
VALIDATION_DIR = "../cts-analyzer/io/validationFiles"

def get_deleted_testcases_with_whole_file_df(project):
    validated_tests_file_path = Path(
        f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv"
    )
    if not os.path.exists(
        f"{validated_tests_file_path}"
    ):
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
    print("Total parent commits:", len(commits_list))
    return commits_list

def get_deleted_testfiles_in_test_deletion_commit_parent(project, parent_commit):
    deleted_tc_df = get_deleted_testcases_with_whole_file_df(project)
    parsed_commit = parse_commit_as_hyperlink_by_project(project, parent_commit)
    deleted_tc_in_commit_df = deleted_tc_df[deleted_tc_df["Parent"] == parsed_commit]
    classes_deleted = list(set(list(deleted_tc_in_commit_df["Filepath"])))
    return classes_deleted

def get_no_of_deleted_testfiles_in_test_deletion_commit_parent(project, parent_commit):
    classes_deleted = get_deleted_testfiles_in_test_deletion_commit_parent(project, commit)
    return len(classes_deleted)
   
if __name__ == "__main__":
    script, prog = sys.argv
    print(script, prog)
    
    #repeats = 50 # No. of times the computation step is repeated; 50 to ensure better predictability
    repeats = 1
    commits_list = get_whole_file_test_deletion_parent_commits(prog)
    for commit in commits_list:
        commit = strip_commit_url(commit)
        directory = "{}/outputBudget/{}/{}/".format(ROOT_DIR, prog, commit)
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
        def all_(x): return x
        def sqrt_(x): return int(math.sqrt(x)) + 1
        def log_(x): return int(math.log(x, 2)) + 1
        def one_(x): return 1

        inputFile = "{}/all_commits_all_testcases/{}/{}-{}-ts.txt".format(ROOT_DIR, prog, prog, commit)
        outpath = "{}/outputBudget/{}/{}/".format(ROOT_DIR, prog, commit)
        sPath = outpath + "selections/"
        tPath = outpath + "measures/"

        numOfTCS = sum((1 for _ in open(inputFile))) # Total no. of testclass in particular commit history
        no_of_deleted_testfiles = get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
        no_of_preserved_testfiles = (numOfTCS-no_of_deleted_testfiles)
        print("Total test files: ", numOfTCS)
        print("No. of deleted test files: ", no_of_deleted_testfiles)
        print("No. of preserved test files: ", no_of_preserved_testfiles)
        repetitions = int(no_of_preserved_testfiles/numOfTCS * 100 ) # Final budget[no. of testcases remaining] in percentage
        print("Computed Repetitions: ", repetitions)

        # for reduction in range(1, repetitions+1):
        # B = int(numOfTCS * reduction / 100) # Current budget for each step
        B= int(numOfTCS * repetitions / 100)
        reduction = repetitions

        for run in range(repeats):
            pTime, rTime, sel = fastr.fastPlusPlus(inputFile, dim=dim, B=B)
            print("FAST++", sel)
            # if reduction == repetitions and run == repeats-1:
            #     print("Final FAST++", sel)
            
            sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST++", reduction, run+1)
            pickle.dump(sel, open(sOut, "wb"))
            tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST++", reduction, run+1)
            pickle.dump((pTime, rTime), open(tOut, "wb"))
            print("FAST++", reduction, pTime, rTime)

        for run in range(repeats):
            pTime, rTime, sel = fastr.fastCS(inputFile, dim=dim, B=B)
            print("FAST-CS", sel)
            sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-CS", reduction, run+1)
            pickle.dump(sel, open(sOut, "wb"))
            tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-CS", reduction, run+1)
            pickle.dump((pTime, rTime), open(tOut, "wb"))
            print("FAST-CS", reduction, pTime, rTime)


        for run in range(repeats):
            pTime, rTime, sel = fastr.fast_pw(inputFile, r, b, bbox=True, k=k, memory=True, B=B)
            print("FAST-pw:", sel)
            sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-pw", reduction, run+1)
            pickle.dump(sel, open(sOut, "wb"))
            tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-pw", reduction, run+1)
            pickle.dump((pTime, rTime), open(tOut, "wb"))
            print("FAST-pw", reduction, pTime, rTime)


        for run in range(repeats):
            pTime, rTime, sel = fastr.fast_(inputFile, all_, r=r, b=b, bbox=True, k=k, memory=True, B=B)
            print("FAST-all:", sel)
            sOut = "{}/{}-{}-{}.pickle".format(sPath, "FAST-all", reduction, run+1)
            pickle.dump(sel, open(sOut, "wb"))
            tOut = "{}/{}-{}-{}.pickle".format(tPath, "FAST-all", reduction, run+1)
            pickle.dump((pTime, rTime), open(tOut, "wb"))
            print("FAST-all", reduction, pTime, rTime)

