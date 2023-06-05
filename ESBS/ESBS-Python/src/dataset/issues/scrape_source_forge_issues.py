import requests
from bs4 import BeautifulSoup

from issue_scraper import IssueScraper


class ScrapeSourceForgeIssues(IssueScraper):

    def get_severity(self, url, issue=None):
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        candidates = (soup.findAll("div", attrs={"class": "grid-4"}))
        for i in range(len(candidates)):
            if "Priority" in candidates[i].text:
                return candidates[i].text.strip().split("\n")[1].strip()
