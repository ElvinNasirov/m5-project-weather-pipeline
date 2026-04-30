"""
Project configuration for the Weather Intelligence Pipeline.

This module stores API endpoints, city coordinates, date settings,
weather variables, and raw data storage configuration.
"""

from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"


CITIES = [
    {"name": "Baku", "latitude": 40.41, "longitude": 49.87},
    {"name": "Lankaran", "latitude": 38.75, "longitude": 48.85},
    {"name": "Guba", "latitude": 41.36, "longitude": 48.51},
    {"name": "Gabala", "latitude": 40.58, "longitude": 47.50},
    {"name": "Shaki", "latitude": 41.11, "longitude": 47.10},
]


HISTORICAL_YEARS = 6

END_DATE_DT = date.today() - timedelta(days=1)
START_DATE_DT = END_DATE_DT - relativedelta(years=HISTORICAL_YEARS)

START_DATE = START_DATE_DT.strftime("%Y-%m-%d")
END_DATE = END_DATE_DT.strftime("%Y-%m-%d")


TARGET_VARIABLES = [
    "temperature_2m_max",
    "precipitation_sum",
    "wind_speed_10m_max",
    "relative_humidity_2m_mean",
    "cloud_cover_mean",
]


EXTRA_WEATHER_VARIABLES = [
    "apparent_temperature_max",
    "sunshine_duration",
]


DAILY_VARIABLES = TARGET_VARIABLES + EXTRA_WEATHER_VARIABLES


DATA_DIR = "data/raw"
HISTORICAL_SUBDIR = "historical"
FORECAST_SUBDIR = "forecast"

RAW_FILE_FORMAT = "parquet"

FORECAST_DAYS = 7
TIMEZONE = "auto"