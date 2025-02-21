import csv
import os
import pandas as pd


def read_csv(file_path):
    if os.path.exists(file_path) and file_path.endswith(".csv"):
        try:
            df = pd.read_csv(file_path, index_col=0)
            # datetime型に変換
            df.incex = pd.to_datetime(df.index)
            return df
        except Exception as e:
            print(e)
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def save_csv(df, file_path):
    if not file_path.endswith(".csv"):
        file_path += ".csv"
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    try:
        df.to_csv(file_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    pass