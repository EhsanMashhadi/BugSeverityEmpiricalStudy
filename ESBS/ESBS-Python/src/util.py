import subprocess
import csv

import pandas as pd


class Util:
    def get_java_files(self, base_directory):
        result = subprocess.run(['find', base_directory, "-type", "f", "-name", "*.java"],
                                stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8").strip().split("\n")

    def write_bugs(self, bugs, project_name="all", path="data"):
        bugs.insert(0, ['Project Name', 'Project Version', 'Issue Tracker', 'URL', 'Priority'])
        with open("{}/project_{}.csv".format(path, project_name), "w") as file:
            csv_writer = csv.writer(file, delimiter=",")
            csv_writer.writerows(bugs)

    def read_bugs(self, project_name="all", path="data"):
        return pd.read_csv("{}/project_{}.csv".format(path, project_name))


if __name__ == '__main__':
    util = Util()
    bugs = [['Chart', '1', 'SourceForge', '5'],
            ['Chart', '2', 'SourceForge', 'General (896)'], ['Chart', '3', None, None], ['Chart', '4', None, None],
            ['Chart', '5', 'SourceForge', '9'], ['Chart', '6', None, None], ['Chart', '7', None, None],
            ['Chart', '8', None, None], ['Chart', '9', 'SourceForge', 'General (896)'], ['Chart', '10', None, None],
            ['Chart', '11', 'SourceForge', '5'], ['Chart', '12', 'SourceForge', '5'], ['Chart', '13', None, None],
            ['Chart', '14', None, None]]
    util.write_bugs(bugs)
