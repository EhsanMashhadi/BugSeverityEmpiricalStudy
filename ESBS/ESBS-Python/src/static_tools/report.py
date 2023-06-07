import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score

from codemetrics_analysis.metrics_analyzer import bugsjar_bug_unify


def unify_priorities(df, tool="SpotBugs"):
    if tool == "SpotBugs":
        return unify_priorities_spotbugs(df)
    elif tool == "Infer":
        return unify_priorities_infer(df)


def unify_priorities_spotbugs(report_df):
    ranks = {
        "Critical": [1, 2, 3, 4],
        "High": [5, 6, 7, 8, 9],
        "Medium": [10, 11, 12, 13, 14],
        "Low": [15, 16, 17, 18, 19, 20],
    }
    report_df["Rank"].replace(
        ranks["Critical"], "Critical", inplace=True)
    report_df["Rank"].replace(
        ranks["High"], "Major", inplace=True)
    report_df["Rank"].replace(
        ranks["Medium"], "Medium", inplace=True)
    report_df["Rank"].replace(
        ranks["Low"], "Minor", inplace=True)

    # report_df["Rank"].replace(
    #     ranks["Critical"], "Critical", inplace=True)
    # report_df["Rank"].replace(
    #     ranks["High"], "High", inplace=True)
    # report_df["Rank"].replace(
    #     ranks["Medium"], "Medium", inplace=True)
    # report_df["Rank"].replace(
    #     ranks["Low"], "Low", inplace=True)

    return report_df


def unify_priorities_infer(report_df):
    # | Error ->
    # L.d_error
    # | Warning ->
    # L.d_warning
    # | Info | Advice | Like ->
    # L.d_info
    ranks = {
        "High": ["ERROR"],
        "Medium": ["WARNING"],
        "Low": ["INFO", "ADVICE", "LIKE"],
    }
    report_df["Severity"].replace(
        ranks["High"], "High", inplace=True)
    report_df["Severity"].replace(
        ranks["Medium"], "Medium", inplace=True)
    report_df["Severity"].replace(
        ranks["Low"], "Low", inplace=True)
    return report_df


def descriptive_statistics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='macro')
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    print("Accuracy: {}".format(acc * 100))
    print("F1: {}".format(f1 * 100))
    print("Precision: {}".format(precision * 100))
    print("Recall: {}".format(recall * 100))


def plot_confusion_matrix(y_true, y_pred, labels: [], title: str):
    cm = confusion_matrix(y_true, y_pred)
    cm_df = pd.DataFrame(cm,
                         index=labels,
                         columns=labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_df, annot=True, fmt='g', cmap="Dark2_r", annot_kws={"fontweight": "bold", "fontsize": 18},
                linewidths=0.003)
    plt.ylabel('Actual Values', fontsize=22, fontweight="bold")
    plt.xlabel('Predicted Values', fontsize=22, fontweight="bold")
    plt.xticks(fontsize=18, fontweight="bold")
    plt.yticks(fontsize=18, fontweight="bold")

    plt.suptitle(title, fontsize=18, fontweight="bold")
    plt.show()


def read_report(tool="SpotBugs", dataset="D4J"):
    if tool == "Infer":
        report_path = "/home/ehsan/Workspace/java/ESBS/d4j_infer_found.csv"
    else:
        if dataset == "D4J":
            report_path = "/home/ehsan/Workspace/java/ESBS/d4j_spotbugs_found.csv"
        elif dataset == "Bugs.jar":
            report_path = "/home/ehsan/Workspace/java/ESBS/bugsjar_spotbugs_found.csv"
    return pd.read_csv(report_path)


def read_buggy_methods(dataset="D4J"):
    path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_buggy.csv"
    if dataset == "Bugs.jar":
        path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_buggy.csv"
    return pd.read_csv(path)


# run anlyzer again
# run on bugs.jar

def report_buggy_methods(tool="SpotBugs", dataset="D4J"):
    df = read_report(tool)
    print("Dataset: {}, Tool: {}".format(dataset, tool))
    print("Total bugs found {}".format(len(df)))
    # keep which one? latest? most important?
    df = df.drop_duplicates(['ProjectName', 'ProjectVersion', 'ClassName', 'StartLine', 'EndLine'], keep='last')
    print("Unique bugs found {}".format(len(df)))
    print()


def report_bug_severity(tool="SpotBugs", dataset="D4J"):
    df = read_report(tool, dataset)
    df_non_duplicate = df.drop_duplicates(['ProjectName', 'BranchName', 'ClassName', 'StartLine', 'EndLine'],
                                          keep='last')

    df_buggy_methods = read_buggy_methods(dataset)
    bug_unify = bugsjar_bug_unify
    df_buggy_methods['Priority'].replace(bug_unify, inplace=True)
    df_merged = pd.merge(df_non_duplicate, df_buggy_methods, how="outer",
                         on=["ProjectName","BranchName","ClassName", "StartLine", "EndLine"],
                         suffixes=["_Left", "_Right"])
    # Find duplicated rows to see difference between severity found!

    df_duplicate = df.duplicated(subset=['ProjectName', 'BranchName', 'ClassName', 'StartLine', 'EndLine'],
                                 keep=False)
    df_duplicate_rows = df[df_duplicate]

    df_merged = unify_priorities(df_merged, tool)

    d4j_labels = ['Critical', 'High', 'Low', 'Medium',
                  "N/A"]

    bugs_jar_labels = []

    label = "Rank"
    if tool == "Infer":
        label = "Severity"
    df_merged.fillna('N/A', inplace=True)
    df_merged.to_csv("spotbugs_priority_conflict.csv")
    descriptive_statistics(df_merged["Priority_Right"], df_merged[label])
    plot_confusion_matrix(y_true=df_merged["Priority_Right"], y_pred=df_merged[label],
                          labels=['Critical', 'Major', 'Minor', "N/A"], title=tool)


# Do we need to check the source of bugs (real vs tools output) manually? or is it ok to just trust on method granualarity?
# Build several projects with different build systems and different versions?

if __name__ == '__main__':
    # report_buggy_methods("SpotBugs","Bugs.jar")
    # report_buggy_methods("Infer")
    # report_bug_severity("Infer")
    report_bug_severity("SpotBugs", "Bugs.jar")
#
# 3) identify if the line prediction is correct!

# RQ3:

# RQ4: edge cases
