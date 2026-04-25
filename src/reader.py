# reader.py
# Handles data ingestion and cleaning from CSV or Google Sheets

import pandas as pd

def read_csv(filepath: str) -> pd.DataFrame:
    """Read and clean data from a CSV file."""
    df = pd.read_csv(filepath)
    df.dropna(how="all", inplace=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def preview(df: pd.DataFrame, rows: int = 5) -> str:
    """Return a string preview of the dataframe."""
    return df.head(rows).to_string(index=False)
