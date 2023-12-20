# Ported utils helper function from main project
def strip_commit_url(repo_url):
    if repo_url:
        return (
            repo_url.split(",")[-1].replace('"', "").replace(")", "").replace(" ", "")
        )
    else:
        return None


def get_full_commit_url_by_project(project: str, hash: str) -> str:
    if project == "commons-lang":
        project_url = "https://github.com/apache/commons-lang/commit/"
    elif project == "joda-time":
        project_url = "https://github.com/JodaOrg/joda-time/commit/"
    elif project == "pmd":
        project_url = "https://github.com/pmd/pmd/commit/"
    elif project == "gson":
        project_url = "https://github.com/google/gson/commit/"
    elif project == "commons-math":
        project_url = "https://github.com/apache/commons-math/commit/"
    elif project == "jfreechart":
        project_url = "https://github.com/jfree/jfreechart/commit/"
    elif project == "cts":
        project_url = "https://android.googlesource.com/platform/cts/+/"
    return project_url + hash


def parse_commit_as_hyperlink_by_project(project: str, hash: str):
    return parse_commit_as_hyperlink(
        get_full_commit_url_by_project(project, hash), hash
    )


# Parse commit hash as hyperlink
def parse_commit_as_hyperlink(url: str, label: str) -> str:
    return f'=HYPERLINK("{url}", "{label}")'
