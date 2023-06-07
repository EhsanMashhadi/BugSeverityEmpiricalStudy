import pandas as pd

import defects4j


class ProjectHandler(object):
    #
    def build_projects(self):
        df = pd.read_csv("../../data/d4j_bugs.csv")
        for index, row in df.iterrows():
            project = row["ProjectName"]
            version = row["ProjectVersion"]
            directory = "../../data/projects_repo/{}{}b".format(project, int(version))
            priority = row["Priority"]

            if not pd.isna(priority):
                result = defects4j.checkout_project(project_name=project, version="{}b".format(version),
                                                    output=directory)
                assert result == 0
                result = defects4j.compile_project(directory)
                assert result == 0

    # def get_project_src(self, project_name):
    #     defects4j = Defects4j()
    #     src_path = defects4j.get_src_classes("../data/projects_repo/{}".format(project_name))
    #     return src_path


if __name__ == '__main__':
    project_handler = ProjectHandler()
    project_handler.build_projects()
    # path = project_handler.get_project_src("Chart2b")
    # print(path[0])
