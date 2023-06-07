import pandas as pd
from sklearn.preprocessing import RobustScaler


def check_contradiction():
    scaler = RobustScaler()
    df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv")
    df_buggy = df[(df["IsBuggy"] == True) & (df["SLOC"] > 4)]
    df_buggy[["SLOC", "IC", "MCCABE", "NBD", "MCCLURE", "DIFF", "MI", "TFO",
              "READABILITY", "EFFORT"]] = scaler.fit_transform(
        df_buggy[["SLOC", "IC", "MCCABE", "NBD", "MCCLURE", "DIFF", "MI", "TFO",
                  "READABILITY", "EFFORT"]])
    df_buggy['average_sum'] = df_buggy[["SLOC", "IC", "MCCABE", "NBD", "MCCLURE", "DIFF", "MI", "TFO",
                                        "EFFORT"]].sum(axis=1)

    nsmallest = df_buggy.nlargest(n=200, columns=["average_sum"], keep='all')
    low_sloc = nsmallest.nsmallest(n=200, columns=["SLOC"], keep="all")
    nsmallest.to_csv("highest_sum.csv")
    low_sloc.to_csv("low_sloc.csv")


def check_critical():
    df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/d4j_methods_buggy.csv")
    df_buggy_critical = df[df["Priority"] == "Critical"]
    df_buggy_critical.to_csv("critical_bugs.csv")


def check_priority_conflict():
    df = pd.read_csv("/home/ehsan/Workspace/java/ESBS/ESBS-Python/src/static_tools/spotbugs_priority_conflict.csv")
    df = df[df["Rank"] == "Low"]
    df = df[df["Priority_Right"] == "Critical"]
    print(df)


def categorize():
    d4j_buggy = calc_average("d4j")
    bugsjar_buggy = calc_average("bugs.jar")

    df_buggy_critical_d4j, df_buggy_noncritical_d4j = unify_severity(df=d4j_buggy, dataset="d4j")
    df_buggy_critical_bugsjar, df_buggy_noncritical_bugsjar = unify_severity(df=bugsjar_buggy, dataset="bugs.jar")

    critical_sample_d4j, noncritical_sample_d4j = sample_severity(df_buggy_critical_d4j, df_buggy_noncritical_d4j)
    critical_sample_bugsjar, noncritical_sample_busjar = sample_severity(df_buggy_critical_bugsjar,
                                                                         df_buggy_noncritical_bugsjar)
    d4j_sample = pd.concat([critical_sample_d4j, noncritical_sample_d4j], ignore_index=True)
    bugs_jar_sample = pd.concat([critical_sample_bugsjar, noncritical_sample_busjar], ignore_index=True)

    d4j_fixed = pd.read_csv("/home/ehsan/Workspace/java/ESBS/d4j_methods_fixed.csv")
    bugsjar_fixed = pd.read_csv("/home/ehsan/Workspace/java/ESBS/bugsjar_methods_fixed.csv")

    d4j_sample.to_csv("samples_d4j.csv")
    bugs_jar_sample.to_csv("samples_bugsjar.csv")
    d4j_fixed.to_csv("d4j_fixed.csv")
    bugsjar_fixed.to_csv("bugsjar_fixed.csv")


def sample_severity(df_buggy_critical, df_buggy_noncritical):
    nsmallest_critical = df_buggy_critical.nsmallest(n=60, columns=["average_sum"], keep='all').sample(n=15)
    nlargest_noncritical = df_buggy_noncritical.nlargest(n=60, columns=["average_sum"], keep='all').sample(n=15)
    return nsmallest_critical, nlargest_noncritical


def calc_average(dataset="d4j"):
    path = "/home/ehsan/Workspace/java/ESBS/d4j_methods_sc_metrics.csv"
    if dataset == "bugs.jar":
        path = "/home/ehsan/Workspace/java/ESBS/bugsjar_methods_sc_metrics.csv"
    df = pd.read_csv(path)
    scaler = RobustScaler()
    df_buggy = df[(df["IsBuggy"] == True) & (df["LC"] > 4)]
    # df_buggy[["LC", "PI", "MA", "NBD", "ML", "D", "MI", "FO",
    #           "R", "E"]] = scaler.fit_transform(
    #     df_buggy[["LC", "PI", "MA", "NBD", "ML", "D", "MI", "FO",
    #               "R", "E"]])
    # df_buggy[["LC_R", "PI_R", "MA_R", "NBD_R", "ML_R", "D_R", "MI_R", "FO_R",
    #           "R_R", "E_R"]] = scaler.fit_transform(
    #     df_buggy[["LC", "PI", "MA", "NBD", "ML", "D", "MI", "FO",
    #               "R", "E"]])
    # x = df_buggy.copy()
    df_buggy["LC_R"] = ""
    df_buggy["PI_R"] = ""
    df_buggy["MA_R"] = ""
    df_buggy["NBD_R"] = ""
    df_buggy["ML_R"] = ""
    df_buggy["D_R"] = ""
    df_buggy["FO_R"] = ""
    df_buggy["R_R"] = ""
    df_buggy["E_R"] = ""
    df_buggy["MI_R"] = ""

    df_buggy["R"] = -1 * df_buggy["R"]
    df_buggy["MI"] = -1 * df_buggy["MI"]

    df_buggy[["LC_R", "PI_R", "MA_R", "NBD_R", "ML_R", "D_R", "FO_R", "E_R", "R_R", "MI_R"]] = scaler.fit_transform(
        df_buggy[["LC", "PI", "MA", "NBD", "ML", "D", "FO", "E", "R", "MI"]])

    df_buggy['average_sum'] = df_buggy[["LC_R", "PI_R", "MA_R", "NBD_R", "ML_R", "D_R", "FO_R",
                                        "E_R", "R_R", "MI_R"]].sum(axis=1)
    df_buggy['average_sum_raw'] = df_buggy[["LC", "PI", "MA", "NBD", "ML", "D", "FO",
                                            "E", "R", "MI"]].sum(axis=1)
    return df_buggy


def unify_severity(df, dataset="d4j"):
    if dataset == "d4j":
        df_buggy_critical = df.loc[(df['Priority'] == 'High') | (df['Priority'] == 'Critical')]
        df_buggy_noncritical = df.loc[(df['Priority'] == 'Low') | (df['Priority'] == 'Medium')]
    elif dataset == "bugs.jar":
        df_buggy_critical = df.loc[
            (df['Priority'] == 'Major') | (df['Priority'] == 'Critical') | (df['Priority'] == 'Blocker')]
        df_buggy_noncritical = df.loc[(df['Priority'] == 'Trivial') | (df['Priority'] == 'Minor')]

    return df_buggy_critical, df_buggy_noncritical


if __name__ == '__main__':
    # check_contradiction()
    categorize()
