## 🧪 Team Project Plan

### Problem Statement
Can we predict which cities in Azerbaijan will have good weather conditions for tourism during May–June?

The model will classify each day as suitable or not suitable for travel, allowing users to compare cities and choose the best destination without manually checking forecasts.

---

### Data Sources
We use the Open-Meteo API:

- Historical data:
https://archive-api.open-meteo.com/v1/archive

- Forecast data:
https://api.open-meteo.com/v1/forecast

Parameters:
- latitude, longitude
- start_date, end_date
- daily weather variables

Additionally, we may incorporate tourism-related data to better align weather conditions with real travel patterns.

---

### Dataset Characteristics

- History length: At least 5 years of historical data per city  
- Granularity: Daily observations (one row per day)  

---

### Cities / Locations
- Baku, Azerbaijan (40.41, 49.87)
- Lankaran, Azerbaijan (38.75, 48.85)
- Guba, Azerbaijan (41.36, 48.51)
- Gabala, Azerbaijan (40.58, 47.50)
- Shaki, Azerbaijan (41.11, 47.10)

---

### Weather Variables

| Variable Name              | Unit  | Why it is relevant |
|---------------------------|------|-------------------|
| precipitation_sum         | mm   | Rainfall directly affects outdoor plans such as sightseeing, city tours, hiking, and beach activities; even small amounts can reduce comfort and limit time spent outside |
| wind_speed_10m_max        | m/s  | Strong winds can make walking uncomfortable and negatively impact activities like beach visits, boat trips, and outdoor dining |
| apparent_temperature_max  | °C   | Represents how hot it actually feels (includes humidity effects); crucial for determining comfort during activities like walking, exploring, and sightseeing |
| relative_humidity_2m_mean | %    | High humidity increases discomfort and fatigue, especially during physical activities like hiking or long walks |
| temperature_2m_max        | °C   | Indicates peak daytime temperature, which determines whether conditions are ideal or too hot for outdoor activities |
| weather_code              | —    | Encodes general weather conditions (e.g., clear, cloudy, rain); helps quickly identify if the day is suitable for outdoor activities without analyzing multiple variables |

---

### Target Variable

The target variable is a binary classification:
- 1 → Good travel day  
- 0 → Poor travel day  

Since this variable is not directly available in the dataset, it will be defined based on domain rules:

- Comfortable apparent temperature range  
- No or minimal precipitation  
- Acceptable wind conditions  
- Favorable weather conditions (based on weather_code)  

---

### Methodology Outline

Week 1:
- Collect historical and forecast weather data
- Store data in DuckDB
- Clean and prepare dataset
- Perform feature engineering

Week 2:
- Conduct exploratory data analysis
- Perform statistical tests
- Build classification model
- Evaluate model performance

---

### Prediction Horizon

The prediction horizon is long-term (>1 month), focusing on identifying seasonal patterns for May–June.

This approach allows us to provide early travel recommendations rather than relying on short-term forecasts, which are already widely available.

---

### Success Criteria

- Pipeline successfully collects and stores weather data
- Clean and structured dataset
- Meaningful visualizations and analysis
- Model correctly classifies good vs bad travel days
- Clear and interpretable results
