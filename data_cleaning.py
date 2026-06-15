import pandas as pd
import numpy as np

def fix_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def remove_duplicates(df):
    return df.drop_duplicates()

def handle_missing_values(df):
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())
    return df

def convert_data_types(df):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
    return df

def clean_data(df):
    df = fix_column_names(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = convert_data_types(df)
    # df = remove_outliers(df)
    return df