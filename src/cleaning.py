"""
Data cleaning utilities for the Weather Intelligence Pipeline.

This module prepares raw weather data for feature engineering by:
- parsing date columns
- converting weather variables to numeric types
- removing duplicate records
- enforcing one row per city-date
- ensuring continuous daily records per city
- filling missing numeric values within each city time series
"""

import pandas as pd


def convert_datetime(
    df: pd.DataFrame,
    date_col: str = "time",
) -> pd.DataFrame:
    """
    Convert a date column to pandas datetime.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    return df


def fix_numeric_types(
    df: pd.DataFrame,
    exclude_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Convert non-excluded columns to numeric where possible.

    Parameters
    ----------
    df:
        Input DataFrame.
    exclude_cols:
        Columns that should not be converted to numeric.
    """
    df = df.copy()

    if exclude_cols is None:
        exclude_cols = ["time", "city"]

    candidate_cols = [
        col for col in df.columns
        if col not in exclude_cols
    ]

    for col in candidate_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove fully duplicated rows.
    """
    return df.drop_duplicates().copy()


def remove_duplicate_city_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep one record per city-date pair.

    If duplicates exist, the first record is kept.
    """
    return (
        df.drop_duplicates(subset=["city", "time"], keep="first")
        .copy()
    )


def ensure_continuous_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure that each city has a continuous daily date range.

    Missing city-date rows are inserted and later filled by
    handle_missing_values().
    """
    df = df.copy()
    df = convert_datetime(df)
    df = df.sort_values(["city", "time"])

    city_frames = []

    for city, city_df in df.groupby("city"):
        start_date = city_df["time"].min()
        end_date = city_df["time"].max()

        full_date_range = pd.date_range(
            start=start_date,
            end=end_date,
            freq="D",
        )

        city_df = (
            city_df.set_index("time")
            .reindex(full_date_range)
            .rename_axis("time")
            .reset_index()
        )

        city_df["city"] = city
        city_frames.append(city_df)

    return (
        pd.concat(city_frames, ignore_index=True)
        .sort_values(["city", "time"])
        .reset_index(drop=True)
    )


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing numeric values within each city time series.

    Forward fill is applied first, followed by backward fill to handle
    possible missing values at the beginning of a city time series.
    """
    df = df.copy()
    df = df.sort_values(["city", "time"])

    numeric_cols = df.select_dtypes(include="number").columns

    df[numeric_cols] = (
        df.groupby("city")[numeric_cols]
        .ffill()
        .bfill()
    )

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full cleaning pipeline.
    """
    df = convert_datetime(df)
    df = fix_numeric_types(df)
    df = remove_duplicates(df)
    df = remove_duplicate_city_dates(df)
    df = ensure_continuous_dates(df)
    df = handle_missing_values(df)

    return df