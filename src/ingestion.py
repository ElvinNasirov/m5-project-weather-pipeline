import requests
import pandas as pd
import time
from datetime import datetime


# -------------------------------
# Request with retry + rate limit handling
# -------------------------------
def make_request(url, params, city_name):
    for attempt in range(5):
        try:
            response = requests.get(url, params=params, timeout=10)

            # 🔥 Rate limit handling
            if response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"[{city_name}] Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            return response.json()

        except Exception as e:
            print(f"[{city_name}] Attempt {attempt+1} failed: {e}")
            time.sleep(2 ** attempt)

    raise Exception(f"[{city_name}] API request failed after retries")


# -------------------------------
# Fetch Historical Data
# -------------------------------
def fetch_historical(city_name, latitude, longitude, start_date, end_date, variables):

    # ✅ Validation
    if start_date >= end_date:
        raise ValueError("start_date must be before end_date")

    today = datetime.today().strftime("%Y-%m-%d")
    if end_date > today:
        raise ValueError("end_date cannot be in the future")

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(variables)
    }

    data = make_request(url, params, city_name)

    if "daily" not in data:
        raise ValueError(f"[{city_name}] Malformed API response")

    df = pd.DataFrame(data["daily"])

    if df.empty:
        raise ValueError(f"[{city_name}] Empty dataset")

    df["time"] = pd.to_datetime(df["time"])
    df["city"] = city_name

    return df


# -------------------------------
# Fetch Forecast Data
# -------------------------------
def fetch_forecast(city_name, latitude, longitude, variables):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(variables)
    }

    data = make_request(url, params, city_name)

    if "daily" not in data:
        raise ValueError(f"[{city_name}] Malformed forecast response")

    df = pd.DataFrame(data["daily"])

    if df.empty:
        raise ValueError(f"[{city_name}] Empty forecast data")

    df["time"] = pd.to_datetime(df["time"])
    df["city"] = city_name

    return df


# -------------------------------
# Fetch All Cities
# -------------------------------
def fetch_all_cities(cities_config, start_date, end_date, variables):

    all_data = {}

    for city in cities_config:
        name = city["name"]

        print(f"Fetching {name}...")

        df = fetch_historical(
            name,
            city["latitude"],
            city["longitude"],
            start_date,
            end_date,
            variables
        )

        all_data[name] = df

        print(f"{name}: {len(df)} rows")

        time.sleep(2)  # 🔥 важно — защита от rate limit

    return all_data