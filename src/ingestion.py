"""
Open-Meteo API ingestion utilities.

This module fetches historical daily weather data and 7-day forecast data
for all configured project cities.
"""

from datetime import datetime
import time
from typing import Any

import pandas as pd
import requests

from src.config import (
    ARCHIVE_API_URL,
    FORECAST_API_URL,
    FORECAST_DAYS,
    TIMEZONE,
)


def make_request(
    url: str,
    params: dict[str, Any],
    city_name: str,
    max_retries: int = 5,
    timeout: int = 10,
) -> dict[str, Any]:
    """
    Send an HTTP GET request with retry and rate-limit handling.

    Parameters
    ----------
    url:
        API endpoint URL.
    params:
        Query parameters for the API request.
    city_name:
        City name used in error messages.
    max_retries:
        Maximum number of request attempts.
    timeout:
        Request timeout in seconds.

    Returns
    -------
    dict
        Parsed JSON response from the API.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"[{city_name}] Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            if response.status_code != 200:
                raise RuntimeError(
                    f"HTTP {response.status_code}: {response.text}"
                )

            return response.json()

        except requests.RequestException as exc:
            wait_time = 2 ** attempt
            print(
                f"[{city_name}] Request attempt {attempt + 1} failed: {exc}. "
                f"Retrying in {wait_time}s..."
            )
            time.sleep(wait_time)

        except RuntimeError as exc:
            wait_time = 2 ** attempt
            print(
                f"[{city_name}] API attempt {attempt + 1} failed: {exc}. "
                f"Retrying in {wait_time}s..."
            )
            time.sleep(wait_time)

    raise RuntimeError(
        f"[{city_name}] API request failed after {max_retries} attempts."
    )


def fetch_historical(
    city_name: str,
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    variables: list[str],
) -> pd.DataFrame:
    """
    Fetch historical daily weather data for one city.

    Parameters
    ----------
    city_name:
        City name.
    latitude:
        City latitude.
    longitude:
        City longitude.
    start_date:
        Historical start date in YYYY-MM-DD format.
    end_date:
        Historical end date in YYYY-MM-DD format.
    variables:
        Daily Open-Meteo variables to request.

    Returns
    -------
    pd.DataFrame
        Historical weather data with a city column.
    """
    if start_date >= end_date:
        raise ValueError("start_date must be before end_date.")

    today = datetime.today().strftime("%Y-%m-%d")
    if end_date > today:
        raise ValueError("end_date cannot be in the future.")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(variables),
        "timezone": TIMEZONE,
    }

    data = make_request(
        url=ARCHIVE_API_URL,
        params=params,
        city_name=city_name,
    )

    if "daily" not in data:
        raise ValueError(f"[{city_name}] Historical API response has no 'daily' field.")

    df = pd.DataFrame(data["daily"])

    if df.empty:
        raise ValueError(f"[{city_name}] Historical API returned an empty dataset.")

    df["time"] = pd.to_datetime(df["time"])
    df["city"] = city_name

    return df


def fetch_forecast(
    city_name: str,
    latitude: float,
    longitude: float,
    variables: list[str],
) -> pd.DataFrame:
    """
    Fetch 7-day forecast weather data for one city.

    Parameters
    ----------
    city_name:
        City name.
    latitude:
        City latitude.
    longitude:
        City longitude.
    variables:
        Daily Open-Meteo variables to request.

    Returns
    -------
    pd.DataFrame
        Forecast weather data with a city column.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(variables),
        "forecast_days": FORECAST_DAYS,
        "timezone": TIMEZONE,
    }

    data = make_request(
        url=FORECAST_API_URL,
        params=params,
        city_name=city_name,
    )

    if "daily" not in data:
        raise ValueError(f"[{city_name}] Forecast API response has no 'daily' field.")

    df = pd.DataFrame(data["daily"])

    if df.empty:
        raise ValueError(f"[{city_name}] Forecast API returned an empty dataset.")

    df["time"] = pd.to_datetime(df["time"])
    df["city"] = city_name

    return df


def fetch_all_cities(
    cities_config: list[dict[str, Any]],
    start_date: str,
    end_date: str,
    variables: list[str],
    verbose: bool = True,
) -> dict[str, pd.DataFrame]:
    """
    Fetch historical daily weather data for all configured cities.

    If one city fails, the error message identifies the city that failed.
    """
    historical_data = {}

    if not verbose:
        print(f"Fetching historical data for {len(cities_config)} cities...")

    for city in cities_config:
        city_name = city["name"]

        if verbose:
            print(f"Fetching historical data for {city_name}...")

        try:
            df_city = fetch_historical(
                city_name=city_name,
                latitude=city["latitude"],
                longitude=city["longitude"],
                start_date=start_date,
                end_date=end_date,
                variables=variables,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Historical fetch failed for city '{city_name}': {exc}"
            ) from exc

        historical_data[city_name] = df_city

        if verbose:
            print(f"{city_name}: {len(df_city)} historical rows")

        time.sleep(2)

    if not verbose:
        total_rows = sum(len(df_city) for df_city in historical_data.values())
        print(
            "Historical fetch completed: "
            f"{len(historical_data)} cities, {total_rows} rows"
        )

    return historical_data


def fetch_forecast_all_cities(
    cities_config: list[dict[str, Any]],
    variables: list[str],
    verbose: bool = True,
) -> dict[str, pd.DataFrame]:
    """
    Fetch 7-day forecast weather data for all configured cities.

    If one city fails, the error message identifies the city that failed.
    """
    forecast_data = {}

    if not verbose:
        print(f"Fetching forecast data for {len(cities_config)} cities...")

    for city in cities_config:
        city_name = city["name"]

        if verbose:
            print(f"Fetching forecast data for {city_name}...")

        try:
            df_city = fetch_forecast(
                city_name=city_name,
                latitude=city["latitude"],
                longitude=city["longitude"],
                variables=variables,
            )
        except Exception as exc:
            raise RuntimeError(
                f"Forecast fetch failed for city '{city_name}': {exc}"
            ) from exc

        forecast_data[city_name] = df_city

        if verbose:
            print(f"{city_name}: {len(df_city)} forecast rows")

        time.sleep(2)

    if not verbose:
        total_rows = sum(len(df_city) for df_city in forecast_data.values())
        print(
            "Forecast fetch completed: "
            f"{len(forecast_data)} cities, {total_rows} rows"
        )

    return forecast_data