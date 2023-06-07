from static_tools.infer_analyzer import InferAnalyzer
from static_tools.spotbugs_analyzer import SpotBugAnalyzer
from static_tools.static_analyzer import StaticAnalyzer


class AnalyzerFactory:
    SPOT_BUG = "SpotBugs"
    INFER = "Infer"

    def __init__(self):
        self.analyzers = {self.SPOT_BUG: SpotBugAnalyzer(), self.INFER: InferAnalyzer()}

    def get_analyzer(self, name) -> StaticAnalyzer:
        return self.analyzers[name]
