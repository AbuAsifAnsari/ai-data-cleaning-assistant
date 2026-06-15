import pandas as pd

def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing numeric columns with median
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical columns with mode
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Fix column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    return df


def generate_cleaning_report(original_df, cleaned_df):
    report = f"""
Data Cleaning Report
--------------------
Original Rows: {original_df.shape[0]}
Cleaned Rows: {cleaned_df.shape[0]}
Rows Removed: {original_df.shape[0] - cleaned_df.shape[0]}

Missing Values Before Cleaning:
{original_df.isnull().sum()}

Missing Values After Cleaning:
{cleaned_df.isnull().sum()}

Duplicate Rows Removed:
{original_df.duplicated().sum()}
"""
    return report