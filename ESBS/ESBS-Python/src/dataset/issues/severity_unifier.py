import os.path

import pandas as pd

import config


def unify_d4j():
    df = pd.read_csv(os.path.join(config.DATA_DIR, config.D4J_FILE))
    df['Severity'].replace(
        config.d4j_severity_groups["low"], "Low", inplace=True)
    df['Severity'].replace(
        config.d4j_severity_groups["medium"], "Medium", inplace=True)
    df['Severity'].replace(
        config.d4j_severity_groups["high"], "High", inplace=True)
    df['Severity'].replace(
        config.d4j_severity_groups["critical"], "Critical", inplace=True)
    df['Severity'].replace(
        config.d4j_severity_groups["not_valid"], "", inplace=True)
    return df
