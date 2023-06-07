import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config
from util import Util


class DistributionAnalyzer:
    def boxplot(self):

        util = Util()
        count = 1
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('D4J Projects Bug Severity Types')

        fig.subplots_adjust(wspace=0.3, hspace=0.4)

        for project in config.d4j_projects:
            df = util.read_bugs(project, "data")
            priority = df['Priority']
            if not priority.isnull().all():
                plt.subplot(3, 4, count)
                plt.title('{}'.format(project))
                my_box = sns.boxplot(x=priority, aspect=1.2)
                plt.grid(visible=None)
                count += 1
            else:
                print("This {} is null".format(project))
        plt.show()

    def hist_per_project(self):
        util = Util()
        count = 1
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('D4J Projects Bug Severity Types')

        fig.subplots_adjust(wspace=0.3, hspace=0.4)

        for project in config.d4j_projects:
            df = util.read_bugs(project, "../data/projects")
            priority = df['Priority']
            if not priority.isnull().all():
                plt.subplot(3, 4, count)
                plt.title('{}'.format(project))
                my_hist = priority.hist()
                for p in my_hist.patches:
                    if p.get_height() > 0:
                        my_hist.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()))
                plt.grid(visible=None)
                count += 1
            else:
                print("This {} is null".format(project))
        plt.show()

    def hist_per_project_method(self):
        util = Util()
        count = 1
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('D4J Projects Bug Severity Types')

        fig.subplots_adjust(wspace=0.3, hspace=0.4)
        base_path = "/home/ehsan/Workspace/java/ESBS/"
        bugs = ["source_critical", "source_high", "source_low", "source_medium"]
        for file in bugs:
            df = pd.read_csv(base_path + file + ".csv")
            # df = df[df["Project Name"] != "Cli"]
            # df = df[df["Project Name"] != "Compress"]

            df.to_csv(base_path + "{}_new.csv".format(file))
            project_name = df['Project Name']
            plt.subplot(2, 2, count)
            plt.title('{}'.format(file))
            my_hist = project_name.hist()
            for p in my_hist.patches:
                if p.get_height() > 0:
                    my_hist.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()))
            plt.grid(visible=None)
            count += 1

        plt.show()


def pie_per_project(self):
    util = Util()
    count = 1
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('D4J Projects Bug Severity Types')
    fig.subplots_adjust(wspace=0.3, hspace=0.4)

    for project in config.d4j_projects:
        df = util.read_bugs(project, "data")
        priority = df['Priority']
        if not priority.isnull().all():
            plt.subplot(3, 4, count)
            plt.title('{}'.format(project))
            labels = priority.dropna().unique()
            data = priority.value_counts()
            # create pie chart
            plt.pie(data, labels=labels, autopct='%.0f%%')
            count += 1
        else:
            print("This {} is null".format(project))
    plt.show()


def hist_all(self):
    util = Util()
    df = util.read_bugs("all_manually", "data")
    priority = df['Priority']
    priority.hist()
    plt.show()


# finding numeric and alphabetic values
# priority_alpha = priority[priority.astype(str).str.isalpha()]
# priority_numeric = priority[priority.astype(str).str.isdigit()]
# plt1 = priority_alpha.hist()
# plt2 = priority_numeric.hist()


# <Confidence> This element matches warnings with a particular bug confidence. The value attribute should be an
# integer value: 1 to match high-confidence warnings, 2 to match normal-confidence warnings, or 3 to match
# low-confidence warnings. <Confidence> replaced <Priority> in 2.0.0 release.

# <Priority>
# Same as <Confidence>, exists for backward compatibility.

# <Rank> This element matches warnings having at least a specified bug rank. The value attribute should be an integer
# value between 1 and 20, where 1 to 4 are scariest, 5 to 9 scary, 10 to 14 troubling, and 15 to 20 of concern bugs.


if __name__ == '__main__':
    # dist = DistributionAnalyzer()
    # dist.hist_per_project_method()
    # df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/bugs_jar_source_codes.csv")
    # print(len(df))
    # df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/d4j_source_codes.csv")
    # print(len(df))
    #
    # df1 = pd.read_csv("/home/ehsan/Workspace/java/ESBS/d4j_spotbugs_found_backup.csv")

    df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/ESBS-Python/data/d4j_bugs.csv")
    print(df)