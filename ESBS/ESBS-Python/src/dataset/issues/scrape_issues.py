import csv
import os

import config
import defects4j
from config import DATA_DIR
from dataset.issues import severity_unifier
from dataset.issues.scrape_google_code_issues import ScrapeGoogleCodeIssues
from dataset.issues.scrape_jira_issues import ScrapeJiraIssues
from dataset.issues.scrape_source_forge_issues import ScrapeSourceForgeIssues
from utils import git_util


def scrape_d4j_issues():
    source_forge_issues = ScrapeSourceForgeIssues()
    jira_scraper = ScrapeJiraIssues()
    google_issues = ScrapeGoogleCodeIssues()

    total_label_count = 0

    bugs = [[config.PROJECT_NAME_CSV_COL, config.PROJECT_VERSION_CSV_COL, config.PROJECT_IssueTracker_CSV_COL,
             config.PROJECT_URL_CSV_COL,
             config.PROJECT_Severity_CSV_COL]]

    for project in config.d4j_projects:
        sfg_ids = 0
        google_ids = 0
        jira_ids = 0
        urls = defects4j.get_project_urls(project)
        for id_url in urls:
            project_id = id_url.split(",")[0]
            project_url = id_url.split(",")[1]
            severity = None
            issue_tracker = None

            if config.SOURCE_FORGE_URL in project_url:
                sfg_ids += 1
                issue_tracker = config.SOURCE_FORGE_URL
                severity = source_forge_issues.get_severity(project_url)
            elif config.GOOGLE_URL in project_url:
                google_ids += 1
                severity = google_issues.get_severity(project_url)
                issue_tracker = config.GOOGLE_URL
            elif config.JIRA_URL in project_url:
                jira_ids += 1
                severity = jira_scraper.get_severity(project_url.rsplit("/", 2)[0],
                                                     project_url.rsplit("/", 2)[2])
                issue_tracker = config.JIRA_URL

            if severity is not None:
                total_label_count += 1

            bugs.append([project, project_id, issue_tracker, project_url, severity])

    with open(os.path.join(DATA_DIR, config.D4J_FILE), "w") as file:
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerows(bugs)


def unify_d4j_issues():
    df = severity_unifier.unify_d4j()
    df.to_csv(os.path.join(config.DATA_DIR, config.D4J_FILE), index=False)


def scrape_bugs_jar_issues():
    jira_issue = ScrapeJiraIssues()
    bugs = [[config.PROJECT_NAME_CSV_COL, config.PROJECT_VERSION_CSV_COL, config.PROJECT_Severity_CSV_COL]]
    for project_name in config.bugs_jar_projects:
        branches_name = git_util.get_bugs_jar_all_branches(project_name=project_name)
        for branch_name in branches_name:
            issue_id = branch_name.split("_")[1]
            severity = jira_issue.get_severity(url="https://issues.apache.org/jira", issue=issue_id)
            bugs.append([project_name, branch_name, severity])
    with open(os.path.join(config.DATA_DIR, config.BUGS_JAR_FILE), "w") as file:
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerows(bugs)


if __name__ == '__main__':
    # scrape_d4j_issues()
    # unify_d4j_issues()
    scrape_bugs_jar_issues()
