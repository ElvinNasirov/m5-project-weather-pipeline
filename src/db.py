"""
DuckDB utilities for the Weather Intelligence Pipeline.

This module manages the local DuckDB database connection,
schema creation, raw parquet loading, and SQL query execution.
"""

from pathlib import Path

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "data" / "weather.duckdb"

RAW_HISTORICAL_PATH = PROJECT_ROOT / "data" / "raw" / "historical"
RAW_FORECAST_PATH = PROJECT_ROOT / "data" / "raw" / "forecast"


def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Create and return a DuckDB connection.

    The database directory is created automatically if it does not exist.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))


def create_schemas() -> None:
    """
    Create project schemas if they do not already exist.
    """
    with get_connection() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        conn.execute("CREATE SCHEMA IF NOT EXISTS staging;")
        conn.execute("CREATE SCHEMA IF NOT EXISTS analytics;")


def _ensure_parquet_files_exist(directory: Path, label: str) -> None:
    """
    Validate that a raw parquet directory contains parquet files.
    """
    parquet_files = list(directory.glob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(
            f"No parquet files found for {label} data in: {directory}"
        )


def load_raw_data() -> None:
    """
    Load raw historical and forecast parquet files into DuckDB.

    Output tables:
    - raw.historical
    - raw.forecast
    """
    historical_glob = RAW_HISTORICAL_PATH / "*.parquet"
    forecast_glob = RAW_FORECAST_PATH / "*.parquet"

    _ensure_parquet_files_exist(RAW_HISTORICAL_PATH, "historical")
    _ensure_parquet_files_exist(RAW_FORECAST_PATH, "forecast")

    with get_connection() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")

        conn.execute(f"""
            CREATE OR REPLACE TABLE raw.historical AS
            SELECT *
            FROM read_parquet('{historical_glob.as_posix()}');
        """)

        conn.execute(f"""
            CREATE OR REPLACE TABLE raw.forecast AS
            SELECT *
            FROM read_parquet('{forecast_glob.as_posix()}');
        """)


def run_query(query: str) -> pd.DataFrame:
    """
    Execute a SQL query against the DuckDB database and return a DataFrame.
    """
    with get_connection() as conn:
        return conn.execute(query).df()