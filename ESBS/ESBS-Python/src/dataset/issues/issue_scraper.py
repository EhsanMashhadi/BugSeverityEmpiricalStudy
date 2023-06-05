from abc import abstractmethod, ABC


class IssueScraper(ABC):

    @abstractmethod
    def get_severity(self, url, issue=None):
        pass
