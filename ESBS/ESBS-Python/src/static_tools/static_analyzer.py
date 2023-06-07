from abc import ABC, abstractmethod


class StaticAnalyzer(ABC):
    @abstractmethod
    def get_project_target(self, directory):
        pass

    @abstractmethod
    def analyze(self, base_path: str, project_name: str, project_version: str, target_dir: str, classpath: str,
                output_file: str,
                only_analyze):
        pass
