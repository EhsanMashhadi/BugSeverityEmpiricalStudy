import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

pd.set_option("display.precision", 2)

metrics = ["LC", "PI", "MA", "NBD", "ML", "D", "MI", "FO",
           "R", "E"]

# metrics = ["SLOC"]

d4j_bug_unify = {'Critical': 'High', 'High': 'High', 'Medium': 'Low', 'Low': 'Low'}

bugsjar_bug_unify = {'Blocker': 'Critical', 'Critical': 'Critical', 'Major': 'Major', 'Minor': 'Minor',
                     'Trivial': 'Minor'}
ck_method_metrics = ["CBO", "LQ", "CQ", "VQ", "FI", "FO", "WMC", "LOC", "MNB", "NUW"]


def buggy_nonbuggy_boxplot(dataset="d4j", show_outlier=False):
    if dataset == "d4j":
        path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv"
    elif dataset == "bugs.jar":
        path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"
    sc_metrics = pd.read_csv(path)
    fig = plt.figure(figsize=(16, 10))
    i = 1

    for metric in metrics:
        ax1 = fig.add_subplot(4, 3, i)
        ax1.axes.get_xaxis().get_label().set_visible(False)
        ax1.axes.get_yaxis().get_label().set_visible(False)

        [x.set_linewidth(1.5) for x in ax1.spines.values()]

        flatui = ["#71B5A0", "#E89574"]
        sns.boxplot(data=sc_metrics, x=metric, y="IsBuggy", orient="h", showfliers=show_outlier,
                    palette=flatui).set_title(metric, fontsize=26, weight='bold')
        ax1.set_xticklabels(ax1.get_xticks(), size=24, weight='bold')
        ax1.set_yticklabels(ax1.get_yticklabels(), size=24, weight='bold')
        plt.yticks([0, 1], ['nb', 'b'])
        ax1.xaxis.set_major_formatter(FormatStrFormatter('%.5g'))
        ticks = ax1.get_xticks()
        ticks = [x for x in ticks if x > 0] or None
        ax1.set_xticks(ticks[::2])

        i += 1

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.5)
    plt.show()


def buggy_severity_boxplot(dataset="d4j", show_outlier=False, project_name=None):
    if dataset == "d4j":
        path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv"
        bug_unify = d4j_bug_unify
    elif dataset == "bugs.jar":
        path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"
        bug_unify = bugsjar_bug_unify

    sc_metrics = pd.read_csv(path)
    sc_metrics = sc_metrics[sc_metrics["IsBuggy"] == True]

    sc_metrics = sc_metrics[sc_metrics["LC"] > 4]

    if project_name:
        sc_metrics = sc_metrics[sc_metrics["ProjectName"] == project_name]

    sc_metrics['Priority'].replace(bug_unify, inplace=True)
    fig = plt.figure(figsize=(14, 8))

    i = 1
    for metric in metrics:
        ax1 = fig.add_subplot(4, 3, i)
        ax1.axes.get_xaxis().get_label().set_visible(False)
        ax1.axes.get_yaxis().get_label().set_visible(False)
        flatui = ["#71B5A0", "#E89574"]
        flatui = ["#E89574","#71B5A0","#F5F4BB"]

        sns.boxplot(data=sc_metrics, x=metric, y="Priority",
                    showfliers=show_outlier, palette=flatui).set_title(metric, fontsize=26, weight='bold')
        ax1.set_xticklabels(ax1.get_xticks(), size=24, weight='bold')
        ax1.set_yticklabels(ax1.get_yticklabels(), size=24, weight='bold')
        # plt.yticks([0, 1], ['nb', 'b'])
        ax1.xaxis.set_major_formatter(FormatStrFormatter('%.5g'))
        ticks = ax1.get_xticks()
        ticks = [x for x in ticks if x > 0] or None
        ax1.set_xticks(ticks[::2])
        i += 1

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.25, hspace=0.5)
    plt.show()


def buggy_severity_boxplot_ck_method(dataset="d4j"):
    if dataset == "d4j":
        path = "/home/ehsan/Workspace/java/ESBS/ck_method_buggy.csv"
    elif dataset == "bugs.jar":
        path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"
    sc_metrics = pd.read_csv(path)
    # sc_metrics = sc_metrics[sc_metrics["IsBuggy"] == True]
    sc_metrics['Severity'].replace(
        {'critical': 'High', 'high': 'High', 'medium': 'Low', 'low': 'Low'}, inplace=True)
    # sc_metrics = sc_metrics[sc_metrics["SLOC"] > 4]
    # sc_metrics = sc_metrics[sc_metrics["ProjectName"] != 'Closure']

    fig = plt.figure()

    i = 1
    for metric in ck_method_metrics:
        ax1 = fig.add_subplot(3, 4, i)
        x_axis = ax1.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)
        sc_metrics.boxplot(column=metric, by='Severity', ax=ax1, showfliers=False)
        # plt.xticks([1, 2], ['non-buggy', 'buggy'])
        i += 1

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.25, hspace=0.5)
    plt.show()


def buggy_nonbuggy_descriptive_statistics(dataset="d4j"):
    if dataset == "d4j":
        path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv"
    elif dataset == "bugs.jar":
        path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"
    sc_metrics = pd.read_csv(path)

    buggy = sc_metrics[sc_metrics["IsBuggy"] == True]
    nonbuggy = sc_metrics[sc_metrics["IsBuggy"] == False]

    buggy.drop(['IsBuggy', 'ProjectName', 'ProjectVersion', 'Priority'], axis=1, inplace=True)
    nonbuggy.drop(['IsBuggy', 'ProjectName', 'ProjectVersion', 'Priority'], axis=1, inplace=True)

    # "IC-NC", "MCCABE", "MCCABE-NC", "NBD", "MCCLURE", "DIFF", "MI", "TFO", "UFO",
    # "READABILITY"
    desc_buggy = buggy.describe(include='all').to_latex()
    desc_nonbuggy = nonbuggy.describe(include='all').to_latex()

    print(desc_buggy)
    print(desc_nonbuggy)


def remove_outlier(df, metric):
    df1 = df[np.abs(df[metric] - df[metric].mean()) <= (3 * df[metric].std())]
    return df1


def show_correlation(metric_type="method", code_type="buggy"):
    if metric_type == "method":
        metrics = ["SLOC", "IC", "IC-NC", "MCCABE", "MCCABE-NC", "NBD", "MCCLURE", "DIFF", "MI", "TFO", "UFO",
                   "READABILITY"]
    elif metric_type == "ck_method":
        metrics = ["CBO", "LQ", "CQ", "VQ", "FI", "FO", "WMC", "LOC", "MNB", "NUW"]
    elif metric_type == "ck_class":
        metrics = ["CBO", "DIT", "NOC", "NOF", "NOM", "WMC", "FI", "FO", "LOC", "LCOM(N)", "TCC", "MNB", "NUW"]

    base_path = "/home/ehsan/Workspace/java/ESBS/"
    df = pd.read_csv(base_path + "bugs_jar_metrics_buggy_methods.csv")
    # df = df[df["ProjectName"] != 'Closure']

    if code_type == "buggy":
        df['Severity'].replace(
            {'Critical': '1-c', 'Blocker': '1-c', 'Major': '2-h', 'Trivial': 'l', 'Minor': '3-l'}, inplace=True)
    # my_size = df.groupby(['Severity', 'ProjectName']).size()
    # print(my_size)
    for metric in metrics:
        df = df[df["ProjectName"] == 'wicket']
        corre = df[metric].corr(df["Severity"], method='kendall')
        print("{}:".format(metric))
        print(corre)
        print()

    plt.show()


def boxplot(metric_type="method", code_type="buggy"):
    if metric_type == "method":
        metrics = ["SLOC", "IC", "IC-NC", "MCCABE", "MCCABE-NC", "NBD", "MCCLURE", "DIFF", "MI", "TFO", "UFO",
                   "READABILITY"]
    elif metric_type == "ck_method":
        metrics = ["CBO", "LQ", "CQ", "VQ", "FI", "FO", "WMC", "LOC", "MNB", "NUW"]
    elif metric_type == "ck_class":
        metrics = ["CBO", "DIT", "NOC", "NOF", "NOM", "WMC", "FI", "FO", "LOC", "LCOM(N)", "TCC", "MNB", "NUW"]

    base_path = "/home/ehsan/Workspace/java/ESBS/"
    df = pd.read_csv(base_path + "bugs_jar_metrics_buggy_methods.csv")
    # df = df[df["SLOC"] > 4]
    # df = df[df["ProjectName"] != 'Closure']
    # if code_type == "buggy":
    #     df['Severity'].replace(
    #         {'Critical': 'h', 'High': 'h', 'Medium': 'm', 'Low': 'l'}, inplace=True)

    if code_type == "buggy":
        df['Severity'].replace(
            {'Critical': '1-c', 'Blocker': '1-c', 'Major': '2-h', 'Trivial': '3-l', 'Minor': '3-l'}, inplace=True)
    i = 1
    fig = plt.figure()
    # for project in config.projects:
    for metric in metrics:
        ax1 = fig.add_subplot(3, 4, i)
        x_axis = ax1.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)

        df = df.drop_duplicates()
        if code_type == "buggy":
            ax = df.boxplot(column=metric, by='Severity', ax=ax1, showfliers=False)
            ax.set_title(metric)
        else:
            ax = df.boxplot(column=metric, ax=ax1, showfliers=False)
            # ax.set_title(metric)
        i += 1

    plt.suptitle("Bugs.jar " + code_type)


def boxplot_d4j(metric_type="method", code_type="buggy"):
    if metric_type == "method":
        metrics = ["SLOC", "IC", "IC-NC", "MCCABE", "MCCABE-NC", "NBD", "MCCLURE", "DIFF", "MI", "TFO", "UFO",
                   "READABILITY"]
        metrics = ["SLOC", "IC", "MCCABE", "NBD", "MCCLURE", "MI", "DIFF", "TFO",
                   "READABILITY"]
    elif metric_type == "ck_method":
        metrics = ["CBO", "LQ", "CQ", "VQ", "FI", "FO", "WMC", "LOC", "MNB", "NUW"]
    elif metric_type == "ck_class":
        metrics = ["CBO", "DIT", "NOC", "NOF", "NOM", "WMC", "FI", "FO", "LOC", "LCOM(N)", "TCC", "MNB", "NUW"]

    base_path = "/home/ehsan/Workspace/java/ESBS/"
    df = pd.read_csv(base_path + "d4j_methods_buggy_sc_metrics.csv")
    # df = pd.read_csv(base_path + "bugs_jar_metrics_buggy_methods.csv")

    df = df[df["SLOC"] > 4]
    df = df[df["ProjectName"] != 'Closure']
    if code_type == "buggy":
        df['Severity'].replace(
            {'Critical': 'Major', 'High': 'Major', 'Medium': 'Low', 'Low': 'Low'}, inplace=True)
        # df['Severity'].replace(
        #     {'Critical': 'Critical', 'Blocker': 'Critical', 'Major': 'Major', 'Trivial': 'Minor', 'Minor': 'Minor'},
        #     inplace=True)

    i = 1
    fig = plt.figure()
    # for project in config.projects:
    for metric in metrics:
        ax1 = fig.add_subplot(3, 3, i)

        x_axis = ax1.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)

        df = df.drop_duplicates()
        boxprops = dict(linestyle='-', linewidth=1.5, color='g')

        if code_type == "buggy":
            ax = df.boxplot(column=metric, by='Severity', ax=ax1, showfliers=False, boxprops=boxprops,
                            return_type='dict')
            colors = ['pink', 'lightblue', 'lightgreen']
            [[item.set_linewidth(1.5) for item in ax[key]['fliers']] for key in ax.keys()]
            [[item.set_linewidth(1.5) for item in ax[key]['medians']] for key in ax.keys()]
            [[item.set_linewidth(1.5) for item in ax[key]['means']] for key in ax.keys()]
            [[item.set_linewidth(1.5) for item in ax[key]['whiskers']] for key in ax.keys()]
            [[item.set_linewidth(1.5) for item in ax[key]['caps']] for key in ax.keys()]
            [[item.set_color('r') for item in ax[key]['boxes']] for key in ax.keys()]
            [[item.set_color('b') for item in ax[key]['medians']] for key in ax.keys()]

            # ax.set_title(metric)

        else:
            ax = df.boxplot(column=metric, ax=ax1, showfliers=False)
            # ax.set_title(metric)
        i += 1
    fig.tight_layout()
    plt.suptitle("D4J " + code_type)
    plt.suptitle("Bugs.jar Dataset")


def boxplot_groups(metric_type="method", code_type="buggy"):
    if metric_type == "method":
        metrics = ["MCCABE"]
    elif metric_type == "ck_method":
        metrics = ["CBO", "LQ", "CQ", "VQ", "FI", "FO", "WMC", "LOC", "MNB", "NUW"]
    elif metric_type == "ck_class":
        metrics = ["CBO", "DIT", "NOC", "NOF", "NOM", "WMC", "FI", "FO", "LOC", "LCOM(N)", "TCC", "MNB", "NUW"]

    base_path = "/home/ehsan/Workspace/java/ESBS/"
    df = pd.read_csv(base_path + "{}_{}.csv".format(metric_type, code_type))
    df = df[df["SLOC"] > 3]
    df = df[df["ProjectName"] != 'Closure']
    if code_type == "buggy":
        df['Severity'].replace(
            {'critical': 'h', 'high': 'h', 'medium': 'l', 'low': 'l'}, inplace=True)
    i = 1
    fig = plt.figure()
    my_size = df.groupby(['Severity', 'ProjectName']).size()
    print(my_size)
    for metric in metrics:
        ax1 = fig.add_subplot(4, 4, i)
        x_axis = ax1.axes.get_xaxis()
        x_label = x_axis.get_label()
        x_label.set_visible(False)

        df = df.drop_duplicates()

        if code_type == "buggy":
            ax = df.boxplot(column=metric, by=['Severity', 'ProjectName'], showfliers=False)
            ax.set_title(metric)
        else:
            ax = df.boxplot(column=metric, ax=ax1, showfliers=False)
            # ax.set_title(metric)
        i += 1

    plt.suptitle(code_type)


if __name__ == '__main__':
    # buggy_nonbuggy_boxplot("bugs.jar", False)
    # buggy_nonbuggy_descriptive_statistics("bugs.jar")
    #
    # buggy_severity_boxplot("bugs.jar", False,"jackrabbit-oak")
    # buggy_severity_boxplot("bugs.jar", False,"maven")
    buggy_severity_boxplot("bugs.jar", False)

    # buggy_nonbuggy_boxplot("bugs.jar")
    # buggy_severity_boxplot_ck_method()
    # show_correlation()
    # boxplot_groups("method", "buggy")
    # boxplot_d4j("method", "buggy")
    # boxplot("method", "buggy")
    # boxplot_groups_bugsjar("method", "buggy")
    # show_correlation("method", "buggy")
    plt.show()
