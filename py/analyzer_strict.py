from analyzer_core import analyzer_main

"""
This file analyzes the [all available - 1 to repetitions ~ 50/commit]reduced test suite and computes the success ratio for all Fast-R algorithms 
comparing with developer reduced test sutie in loose scenario.
"""


projects_list = [
    "commons-lang",
    "gson",
    # "commons-math",
    "jfreechart",
    "joda-time",
    # "pmd",
    #  "cts"
]


for index, prog in enumerate(projects_list):
    analyzer_main(prog, "strict")
