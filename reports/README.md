## 🌍 Tourism Weather Risk & Activity Suitability Platform

### 📌 Project Overview

This project provides data-driven weather insights to support tourism planning and decision-making. It helps travel agencies and tour operators evaluate the feasibility of outdoor activities based on both historical patterns and forecasted conditions.

The main objectives are:

- Minimize cancellation risks for tour operators
- Enhance customer satisfaction by recommending optimal dates for specific activities
- Provide AI-driven explanations for weather-based travel recommendations

---

### 👥 Team & Responsibilities

- **Jala (Data Engineer):** Ingestion pipeline, DuckDB management, and automation
- **Roya (Team Manager & Data Quality):** Task coordination, data validation, and cleaning logic
- **Sema (Data Analyst):** Exploratory Data Analysis (EDA), statistical testing, and tourism insights
- **Elvin (ML Engineer):** Feature engineering, model training, and AI suitability logic

---

### ⚙️ Technical Specifications

### 1. Dataset History Length

We use **5+ years of historical daily weather data (2020 up to the most recent available date)** to capture long-term seasonal patterns and climate variability across Azerbaijan.

### 2. Dataset Granularity

The data is processed at a **daily granularity**, where each record represents a 24-hour summary of weather conditions for a specific city.

### 3. Prediction Horizon

The project targets **medium-range forecasting (up to 28 days)**, aligning with typical tourism planning and booking cycles.
This horizon provides a balance between practical usability and forecasting reliability, as prediction accuracy tends to decrease beyond this range.

---

## 🎯 Targets

We use a **multi-output regression model** to predict key weather variables required for activity suitability decisions.

- **temperature_2m_max**
    
    Predicts peak daily temperature, which is critical for outdoor comfort and heat-related constraints.
    
- **precipitation_sum**
    
    Measures total daily rainfall, the most important factor for determining whether outdoor activities are feasible.
    
- **wind_speed_10m_max**
    
    Captures maximum wind conditions, essential for safety-sensitive activities such as cable car and boating.
    
- **relative_humidity_2m_mean**
    
    Represents average humidity, which affects perceived temperature and overall comfort.
    
- **cloud_cover_mean**
    
    Indicates sky conditions and visibility, useful for assessing atmosphere (e.g., sunny vs gloomy) and fog likelihood.
    

---

## 🧠 Features

### Core & Derived Weather Features

- **apparent_temperature_max**
    
    Represents perceived temperature (“feels like”), providing additional context for human comfort.
    
- **sunshine_duration**
    
    Reflects how sunny a day is, providing additional context for outdoor activity quality and user experience.
    
- **city (encoded)**
    
    Captures location-specific climate patterns across regions (Baku, Lankaran, Guba, Gabala, Shaki).
    

---

### Calendar Features

- **month**
    
    Helps the model capture seasonal patterns within the May–June period.
    
- **day_of_month**
    
    Provides finer time progression within each month, allowing the model to learn gradual weather changes.
    

---

### Lag Features (Previous Day Signals)

- **temperature_lag_1**
    
    Yesterday’s temperature, used to model short-term continuity in temperature trends.
    
- **precipitation_lag_1**
    
    Previous day’s rainfall, helping capture ongoing rain patterns.
    
- **wind_lag_1**
    
    Yesterday’s wind speed, useful for modeling wind persistence.
    
- **humidity_lag_1**
    
    Previous day’s humidity, supporting short-term atmospheric continuity.
    

---

### Rolling Features (Short-Term Trends)

- **temperature_3d_avg**
    
    3-day average temperature, capturing recent warming or cooling trends.
    
- **precipitation_7d_sum**
    
    Total rainfall over the past 7 days, indicating prolonged wet conditions.
    
- **wind_3d_avg**
    
    3-day average wind speed, smoothing short-term fluctuations.
    
- **humidity_7d_avg**
    
    7-day average humidity, reflecting persistent atmospheric conditions.
    

---

## 🧾 Feature Table

| Source | Feature Name | Unit | Description |
| --- | --- | --- | --- |
| Open-Meteo | apparent_temperature_max | °C | perceived temperature |
| Open-Meteo | sunshine_duration | sec | total daily sunlight |
| Derived | city (encoded) | — | location identifier |
| Derived | month | — | month of observation |
| Derived | day_of_month | — | day within month |
| Derived | temperature_lag_1 | °C | previous day temperature |
| Derived | precipitation_lag_1 | mm | previous day rainfall |
| Derived | wind_lag_1 | m/s | previous day wind |
| Derived | humidity_lag_1 | % | previous day humidity |
| Derived | temperature_3d_avg | °C | 3-day rolling avg temp |
| Derived | precipitation_7d_sum | mm | 7-day rainfall sum |
| Derived | wind_3d_avg | m/s | 3-day rolling avg wind |
| Derived | humidity_7d_avg | % | 7-day rolling avg humidity |

---

## ⚙️ Model Approach

We use historical data for model training and evaluation, applying a time-based split to ensure realistic performance assessment.

Additionally, we integrate **7-day forecast data from the API** for short-term activity suitability decisions.

For medium-range predictions, we use a **multi-output regression model (Random Forest Regressor)** to predict all target variables simultaneously.

This approach allows us to:

- maintain a clean and unified forecasting pipeline
- capture relationships between multiple weather variables
- generate consistent inputs for downstream activity suitability decisions

---

## 🔄 System Flow

Historical Weather Data (Open-Meteo API)
+
7-Day Forecast Data (API)
↓
Data Cleaning & Validation
↓
Feature Engineering
(lag features, rolling averages, calendar features)
↓
Multi-output Regression Model
(Random Forest Regressor)
↓
Predicted Weather Variables
(temperature, precipitation, wind, humidity, cloud cover)
↓
AI Agent (Activity Suitability Layer)
↓
Final Output:

- Activity suitability (Suitable / Risky / Not Suitable)
- Natural language explanation
