import json
from functools import reduce
from experimentBudgetModified import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
)

algos = ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]
projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]
data = {"Strict": {}, "Loose": {}}

for index, project in enumerate(projects_list):
    loose_file = open(f"./output-loose/{project}_analyzer.json")
    strict_file = open(f"./output-strict/{project}_analyzer.json")
    algo_analyzer_strict = json.load(strict_file)
    algo_analyzer_loose = json.load(loose_file)

    commits_list = get_whole_file_test_deletion_parent_commits(project)
    print("Total whole file test deletion parent commits:", len(commits_list))

    deleted_testcases_with_whole_file = get_deleted_testcases_with_whole_file_df(
        project
    )
    print(
        "Total test cases deleted with whole file:",
        len(deleted_testcases_with_whole_file),
    )

    for algo in algos:
        total_detected = 0
        total_failed_to_detect = 0
        for algo_analyzer_commit in algo_analyzer_strict["details"]:
            alog_analyzer_commit_each_algo = algo_analyzer_commit["Algorithm"][algo]
            total_detected += alog_analyzer_commit_each_algo[
                "Total Detected Deleted Testfiles"
            ]
            total_failed_to_detect += alog_analyzer_commit_each_algo[
                "Total Failed To Detect Deleted Testfiles"
            ]

        if project not in data["Strict"]:
            data["Strict"][project] = {}
        data["Strict"][project][algo] = (
            {
                "Total Detected Deleted Testfiles": total_detected,
                "Total Failed To Detect Deleted Testfiles": total_failed_to_detect,
            },
        )

        total_detected = 0
        total_failed_to_detect = 0
        for algo_analyzer_commit in algo_analyzer_loose["details"]:
            alog_analyzer_commit_each_algo = algo_analyzer_commit["Algorithm"][algo]
            total_detected += alog_analyzer_commit_each_algo[
                "Total Detected Deleted Testfiles"
            ]
            total_failed_to_detect += alog_analyzer_commit_each_algo[
                "Total Failed To Detect Deleted Testfiles"
            ]

        if project not in data["Loose"]:
            data["Loose"][project] = {}

        data["Loose"][project][algo] = (
            {
                "Total Detected Deleted Testfiles": total_detected,
                "Total Failed To Detect Deleted Testfiles": total_failed_to_detect,
            },
        )

f = open("./final_analyzer.json", "w")
f.write(json.dumps(data, indent=2))
