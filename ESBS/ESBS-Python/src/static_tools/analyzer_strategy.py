import pandas as pd

from defects4j import Defects4j
from static_tools.analyzer_factory import AnalyzerFactory
from utils.git_util import GitUtil


class AnalyzerStrategy:

    def __init__(self):
        self.analyzer_factory = AnalyzerFactory()

    # infer and spotbugs folders are not created automatically!
    def decide_d4j(self, analyzer_name):

        analyzer = self.analyzer_factory.get_analyzer(analyzer_name)
        df = pd.read_csv("../../data/d4j_bugs.csv")
        for index, row in df.iterrows():
            project_name = row["ProjectName"]
            version = row["ProjectVersion"]
            project_folder = "{}{}b".format(project_name, int(version))
            directory = "../../data/projects_repo/{}".format(project_folder)
            priority = row["Priority"]

            if not pd.isna(priority):
                classpath = Defects4j.get_project_classpath(directory)
                # this jar file is added manually since it is not found in the project classpath
                classpath += ":/home/ehsan/Workspace/java/defects4j/defects4j/framework/projects/Math/lib"
                print("Row {} - Working on {}".format(index + 1, project_folder))
                target_dir = analyzer.get_project_target(directory)
                base_path = "home/ehsan/Workspace/java/ESBS/ESBS-Python/data/projects_repo/"
                output_file = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/spotbugs/{}.xml".format(project_folder)

                result = analyzer.analyze(base_path=base_path,
                                          project_name=project_name, project_version=version,
                                          target_dir=target_dir, classpath=classpath,
                                          output_file=output_file, only_analyze=None)
                print(result)
                print("-" * 75)

    # jackrabbit 43 success
    def decide_bugsjar(self, analyzer_name):
        analyzer = self.analyzer_factory.get_analyzer(analyzer_name)
        git_util = GitUtil()
        df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/bugs_jar_bugs.csv")
        failed_build = 0
        for index, row in df.iterrows():
            project_name = row["ProjectName"]
            branch_name = row["BranchName"]
            priority = row["Priority"]
            if not pd.isna(priority) and project_name == "camel":
                print("Row {} - Working on Project: {} - Branch Name: {}".format(index + 1, project_name, branch_name))
                result = git_util.checkout_bugs_jar(project_name, branch_name)
                if result.returncode != 0:
                    print("*" * 75)
                    print("Checkout Problem")
                    print("*" * 75)

                result = git_util.build_project_camel(project_name)
                result_output = result.stdout.decode("utf-8").strip()

                if result.returncode != 0:
                    failed_build += 1
                    print("*" * 75)
                    print("ERROR")
                    print("*" * 75)
                    print(result_output)
                    continue

                print(result_output[result_output.index("Reactor Summary") - 50:])
                assert "BUILD SUCCESS" in result_output
                path = "/home/ehsan/Workspace/java/bugsjar/bugs-dot-jar/" + project_name
                target_dir = "."
                classpath = "/home/ehsan/.m2/" + ":" + path + "/lib"
                base_path = "/home/ehsan/Workspace/java/bugsjar/bugs-dot-jar/"
                output_file = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/spotbugs/bugs_jar/{}_{}.xml".format(
                    project_name, branch_name.replace("/", "_"))
                result = analyzer.analyze(base_path=base_path,
                                          project_name=project_name, project_version=branch_name,
                                          target_dir=target_dir, classpath=classpath,
                                          output_file=output_file, only_analyze=None)

                print(result)
                print("-" * 75)
        print("Failed Builds Count {}".format(failed_build))

    def decide_bugsjar1(self, analyzer_name):
        analyzer = self.analyzer_factory.get_analyzer(analyzer_name)
        df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/bugs_jar_bugs.csv")
        for index, row in df.iterrows():
            project_name = row["ProjectName"]
            branch_name = row["BranchName"]
            branch_name = branch_name[branch_name.rfind("/") + 1:]
            priority = row["Priority"]
            if index < 572:
                continue
            if not pd.isna(priority):
                print("Row {} - Working on Project: {} - Branch Name: {}".format(index + 1, project_name, branch_name))
                path = "/home/ehsan/Workspace/java/bugsjar_somayeh/" + project_name + "/" + branch_name
                target_dir = "."
                classpath = "/home/ehsan/.m2/" + ":" + path + "/lib"
                base_path = "/home/ehsan/Workspace/java/bugsjar_somayeh/"
                output_file = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/spotbugs/bugs_jar/{}_{}.xml".format(
                    project_name, branch_name.replace("/", "_"))
                result = analyzer.analyze(base_path=base_path,
                                          project_name=project_name, project_version=branch_name,
                                          target_dir=target_dir, classpath=classpath,
                                          output_file=output_file, only_analyze=None)

                print(result)
                print("-" * 75)


if __name__ == '__main__':
    strategy = AnalyzerStrategy()
    # strategy.decide("SpotBugs")
    # strategy.decide_d4j("Infer")
    strategy.decide_bugsjar1("SpotBugs")
