from analyzer_utils import *
import json
from config import ROOT_DIR

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


def get_test_filename_by_line_no(program, commit, line_no):
    testcase_history_file_path = (
        "{}/all_commits_all_testcases/{}/{}-{}-tsh.json".format(
            ROOT_DIR, program, program, commit
        )
    )
    testcase_history = json.load(open(testcase_history_file_path))

    # list out keys and values separately
    key_list = list(testcase_history.keys())
    val_list = list(testcase_history.values())

    # print key with matching value
    position = val_list.index(line_no)
    print(key_list[position])

    return key_list[position]
