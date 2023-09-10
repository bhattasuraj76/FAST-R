import json
from functools import reduce
from experimentBudgetModified import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
    get_deleted_testfiles_in_test_deletion_commit_parent,
    ROOT_DIR,
)



algos = ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]

# def sum(a, b):
#     return a["Total Deleted Testfiles"] + b["Total Deleted Testfiles"]

# total_deleted_testfiles = reduce(sum, algo_analyzer)
# print("Total deleted files:", total_deleted_testfiles)

projects_list = [
    # "commons-lang",
    "gson",
    # "commons-math",
    # "jfreechart",
    # "joda-time",
    # "pmd",
    # "cts",
]
data = [{}, {}, {}, {}, {}, {}, {}]
for index, project in enumerate(projects_list):
    file = open(f"./{project}_analyzer.json")
    algo_analyzer = json.load(file)

    commits_list = get_whole_file_test_deletion_parent_commits(project)
    print("Total whole file test deletion parent commits:", len(commits_list))

    deleted_testcases_with_whole_file = get_deleted_testcases_with_whole_file_df(project)
    print("Total test cases deleted with whole file:", len(deleted_testcases_with_whole_file))
    
    for algo in algos:
        total_detected = 0
        total_failed_to_detect = 0
        for algo_analyzer_commit in algo_analyzer["details"]:
            alog_analyzer_commit_each_algo = algo_analyzer_commit["Algorithm"][algo]
            total_detected += alog_analyzer_commit_each_algo[
                "Total Detected Deleted Testfiles"
            ]
            total_failed_to_detect += alog_analyzer_commit_each_algo[
                "Total Failed To Detect Deleted Testfiles"
            ]

        data[index][algo] = (
            {
                "Total Detected Deleted Testfiles": total_detected,
                "Total Failed To Detect Deleted Testfiles": total_failed_to_detect,
            },
        )

f = open("./final_analyzer.json", "w")
f.write(json.dumps(data))
