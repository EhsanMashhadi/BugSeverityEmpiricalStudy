from jira import JIRA

from issue_scraper import IssueScraper


class ScrapeJiraIssues(IssueScraper):

    def get_severity(self, url, issue=None):
        jira = JIRA(server=url)
        issue = jira.issue(issue)
        return issue.fields.priority
