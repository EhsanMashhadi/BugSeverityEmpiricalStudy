import json
from urllib.request import urlopen

from issue_scraper import IssueScraper


class ScrapeGoogleCodeIssues(IssueScraper):

    def get_severity(self, url, issue=None):
        json_url = urlopen(url)
        text = json.loads(json_url.read())
        return text["labels"]
