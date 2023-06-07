#
# let d =
# match (severity : IssueType.severity) with
# | Error ->
# L.d_error
# | Warning ->
# L.d_warning
# | Info | Advice | Like ->
# L.d_info

from defects4j import Defects4j
from static_tools.static_analyzer import StaticAnalyzer


class InferAnalyzer(StaticAnalyzer):

    def analyze(self, base_path: str, project_name: str, project_version: str, target_dir: str, classpath: str,
                output_file: str, only_analyze):
        pass

    # flll using commented method

    def get_project_target(self, directory):
        buggy_files = Defects4j.get_buggy_files(directory)
        src_folder = Defects4j.get_src_classes(directory)[0]
        buggy_files = [src_folder + "/" + buggy_file.replace(".", "/") + ".java" for buggy_file in buggy_files]
        return buggy_files

    # def analyze(self, project_folder: str, classpath: str, target):
    #     base_path = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/projects_repo/"
    #     working_directory = base_path + project_folder
    #     output_file = "/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/infer/{}".format(project_folder)
    #
    #     result = subprocess.run(
    #         ["infer", "run", "-o", output_file, "--", "javac", "-cp", classpath,
    #          ] + target, cwd=working_directory,
    #         stdout=subprocess.PIPE)
    #     result = result.stdout.decode("utf-8").strip()
    #     return result
