import pandas as pd


def clean_race_results(df):
    df = df.copy()

    df["round"] = df["round"].astype(int)
    df["position"] = df["position"].astype(int)
    df["grid"] = df["grid"].astype(int)
    df["laps"] = df["laps"].astype(int)
    df["points"] = df["points"].astype(float)
    df["date"] = pd.to_datetime(df["date"])

    df["positions_gained"] = df["grid"] - df["position"]

    return df


