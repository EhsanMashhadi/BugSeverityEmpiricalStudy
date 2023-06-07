import itertools
from collections import defaultdict

import pandas as pd
from cliffs_delta import cliffs_delta
from hyperframe.frame import DataFrame
from scipy.stats import mannwhitneyu
from scipy.stats import shapiro

import config
from codemetrics_analysis.metrics_analyzer import d4j_bug_unify, bugsjar_bug_unify, metrics


class Result:

    def __init__(self, project_name, is_rejected, cliff_result):
        self.project_name = project_name
        self.is_rejected = is_rejected
        self.cliff_result = cliff_result


class HypothesisTest:
    count = 0
    my_map = defaultdict(list)

    # camle and maven looks to have large effect in some severity differences
    def calculate_ranksum_severity(self, dataset="d4j", project_name=None):

        if dataset == "d4j":
            path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv"
            bug_unify = d4j_bug_unify
        elif dataset == "bugs.jar":
            path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"
            bug_unify = bugsjar_bug_unify

        sc_metrics = pd.read_csv(path)
        sc_metrics = sc_metrics[(sc_metrics["IsBuggy"] == True)]
        sc_metrics = sc_metrics[sc_metrics["LC"] > 4]
        if project_name:
            sc_metrics = sc_metrics[sc_metrics["ProjectName"] == project_name]
        sc_metrics['Priority'].replace(bug_unify, inplace=True)

        c = set(itertools.combinations(set(bug_unify.values()), 2))
        # c = {('Minor', 'Major')}
        for val in c:
            sc_metrics_first = sc_metrics[sc_metrics["Priority"] == val[0]]
            sc_metrics_second = sc_metrics[sc_metrics["Priority"] == val[1]]

            if len(sc_metrics_first) == 0 or len(sc_metrics_second) == 0:
                return
            for metric in metrics:
                print("Project {} Metric: {} Between {}-{}".format(project_name, metric, val[0], val[1]))
                result = self.calculate_ransum(sc_metrics_first[metric], sc_metrics_second[metric])
                cliff_size = self.clif_delta(sc_metrics_first[metric], sc_metrics_second[metric])
                # self.my_map[metric + str(val) + str(cliff_size)] += result
                metric_band = "{} - {} {}".format(metric, val[0], val[1])
                self.my_map[metric_band].append(Result(project_name, result, cliff_size))

                print()

    def calculate_ranksum_buggy_nonbuggy(self, dataset="d4j", project_name=None):
        if dataset == "d4j":
            path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv"

        elif dataset == "bugs.jar":
            path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"

        sc_metrics = pd.read_csv(path)
        sc_metrics = sc_metrics[sc_metrics["LC"] > 4]

        if project_name:
            sc_metrics = sc_metrics[sc_metrics["ProjectName"] == project_name]

        buggy_methods_metrics = sc_metrics[(sc_metrics["IsBuggy"] == True)]
        nonbuggy_methods_metrics = sc_metrics[(sc_metrics["IsBuggy"] == False)]

        if len(buggy_methods_metrics) == 0 or len(nonbuggy_methods_metrics) == 0:
            return
        for metric in metrics:
            print("Metric: {}".format(metric))
            is_rejected = self.calculate_ransum(buggy_methods_metrics[metric], nonbuggy_methods_metrics[metric])
            cliff_result = self.clif_delta(buggy_methods_metrics[metric], nonbuggy_methods_metrics[metric])
            self.my_map[metric].append(Result(project_name, is_rejected, cliff_result))
            print()

    def check_normal_distributin(self, df):
        alpha = 0.05
        stat, p = shapiro(df)
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        if p > alpha:
            print('Sample looks Gaussian (fail to reject H0)')
        else:
            print('Sample does not look Gaussian (reject H0)')

    def calculate_ransum(self, df1, df2):
        alpha = 0.05
        # stat, p = ranksums(df1, df2)
        stat, p = mannwhitneyu(df1, df2)
        print("Ranksum Test Statistics={:.2f}, p={:.2f}".format(stat, p))
        if p > alpha:
            print('Same distribution (fail to reject H0)')
            return 0
        else:
            print('Different distribution (reject H0)')
            return 1

    def clif_delta(self, df1, df2):
        d, size = cliffs_delta(df1.values.tolist(),
                               df2.values.tolist())
        print("Cliff Delta: d={}, res={}".format(d, size))
        return size


if __name__ == '__main__':
    hypotest = HypothesisTest()
    for proj in config.bugs_jar_projects:
        print("Poj {}".format(proj))
        hypotest.calculate_ranksum_severity("bugs.jar", proj)
        print("-" * 15)
        print("Statistical Test Result")
    for metric in hypotest.my_map.keys():
        negligible = 0
        small = 0
        medium = 0
        large = 0
        rejected = 0
        size = len(hypotest.my_map[metric])

        for result in hypotest.my_map[metric]:
            rejected += result.is_rejected
            if result.cliff_result == 'negligible':
                negligible += 1
            elif result.cliff_result == 'small':
                small += 1
            elif result.cliff_result == 'medium':
                medium += 1
            elif result.cliff_result == 'large':
                large += 1
        print(
            "Metric: {}, Rejected: {}, Negligible: {}, Small: {}, Medium: {}, Large: {}".format(metric,                                                                                                             rejected / size,
                                                                                                             negligible / size,
                                                                                                             small / size,
                                                                                                             medium / size,
                                                                                                             large / size))

    # for proj in config.bugs_jar_sub_projects:
    #     print("Poj {}".format(proj))
    #     hypotest.calculate_ranksum_severity("bugs.jar", proj)
    # print(my_map)
    # print(len(my_map))
    # print(sum(my_map.values()))

    # print("-" * 15)
    # hypotest.calculate_ranksum_severity("bugs.jar")

    # for proj in config.d4j_projects:
    #     print("Poj {}".format(proj))
    #     hypotest.calculate_ranksum_severity("d4j")
    # print("-" * 15)
    # hypotest.calculate_ranksum_buggy_nonbuggy("bugs.jar")
    # hypotest.calculate_ranksum_severity("bugs.jar","maven")
    # hypotest.calculate_ranksum_severity("bugs.jar")
    # for proj in config.bugs_jar_projects:
    #     print("Poj {}".format(proj))
    #     hypotest.calculate_ranksum_severity("bugs.jar")
    #     print("-" * 15)
    # hypotest.calculate_shabiro()
