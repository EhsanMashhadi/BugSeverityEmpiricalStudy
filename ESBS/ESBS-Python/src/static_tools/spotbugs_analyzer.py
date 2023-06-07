# spotbugs -textui -xml:withMessages -output ehsan.xml -auxclasspath target/classes/ -onlyAnalyze org.apache.commons.codec.net.QuotedPrintableCodec .
# java -jar /home/ehsan/Workspace/thesis/spotbugs/spotbugs-4.5.3/lib/spotbugs.jar -effort:max -output ~/Desktop/temp/spotbugs_result2.xml -xml -progress  target/classes/
import os
import subprocess

from defects4j import Defects4j
from static_tools.static_analyzer import StaticAnalyzer


class SpotBugAnalyzer(StaticAnalyzer):

    def get_project_target(self, directory):
        return Defects4j.get_project_target(directory)

    def analyze(self, base_path: str, project_name: str, project_version: str, target_dir: str, classpath: str,
                output_file: str,
                only_analyze):
        working_directory = base_path + project_name + "/" + project_version
        # check if the folder exist
        if not os.path.isdir(working_directory):
            return "Project {} Does not Exist!".format(working_directory)

        result = subprocess.run(
            ["java", "-jar", "/home/ehsan/Workspace/thesis/spotbugs/spotbugs-4.5.3/lib/spotbugs.jar", "-effort:max",
             # "-onlyAnalyze", only_analyze,
             "-output", output_file, "-xml", "-progress", "-auxclasspath",
             classpath, target_dir], cwd=working_directory,
            stdout=subprocess.PIPE)
        result = result.stdout.decode("utf-8").strip()
        return result
