"""
Generate realistic Shenzhen air quality daily data (2019-2024)
Based on real statistical patterns from official sources:
- PM2.5 annual mean: ~19-24 ug/m3 (decreasing trend)
- O3 increasing trend (primary pollutant since 2016)
- Seasonal pattern: PM2.5 higher in autumn/winter, O3 higher in summer
- Source: Shenzhen Ecological Environment Bureau, aqistudy.cn
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)  # for reproducibility

# date range: 2019-01-01 to 2024-12-31
start_date = datetime(2019, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start_date, end_date, freq='D')
n = len(dates)

# helper: seasonal component (month-based)
months = np.array([d.month for d in dates])
years = np.array([d.year for d in dates])

# PM2.5: annual means roughly 24(2019), 22(2020), 20(2021), 18(2022), 17(2023), 16(2024)
# Seasonal: higher in Oct-Jan (dry season), lower in Jun-Aug (wet season)
pm25_annual_base = {2019: 24, 2020: 22, 2021: 20, 2022: 18, 2023: 17, 2024: 16}
pm25_seasonal = {1: 1.4, 2: 1.2, 3: 1.0, 4: 0.85, 5: 0.75, 6: 0.7,
                 7: 0.65, 8: 0.7, 9: 0.85, 10: 1.1, 11: 1.3, 12: 1.5}

pm25 = []
for i in range(n):
    base = pm25_annual_base[years[i]]
    seasonal = pm25_seasonal[months[i]]
    value = base * seasonal + np.random.normal(0, 5)
    pm25.append(max(3, round(value, 1)))  # minimum 3

# PM10: roughly 1.5-2x PM2.5 with some noise
pm10 = [round(p * np.random.uniform(1.4, 2.0) + np.random.normal(0, 3), 1) for p in pm25]
pm10 = [max(5, x) for x in pm10]

# NO2: annual means roughly 28-32, decreasing slightly
no2_annual_base = {2019: 32, 2020: 28, 2021: 30, 2022: 27, 2023: 26, 2024: 25}
no2_seasonal = {1: 1.3, 2: 1.2, 3: 1.0, 4: 0.9, 5: 0.85, 6: 0.8,
                7: 0.75, 8: 0.8, 9: 0.9, 10: 1.1, 11: 1.25, 12: 1.35}

no2 = []
for i in range(n):
    base = no2_annual_base[years[i]]
    seasonal = no2_seasonal[months[i]]
    value = base * seasonal + np.random.normal(0, 6)
    no2.append(max(3, round(value, 1)))

# O3 (8-hour max): increasing trend, higher in summer/autumn
o3_annual_base = {2019: 52, 2020: 50, 2021: 54, 2022: 56, 2023: 58, 2024: 55}
o3_seasonal = {1: 0.6, 2: 0.65, 3: 0.8, 4: 0.95, 5: 1.1, 6: 1.2,
               7: 1.3, 8: 1.25, 9: 1.15, 10: 1.1, 11: 0.8, 12: 0.6}

o3 = []
for i in range(n):
    base = o3_annual_base[years[i]]
    seasonal = o3_seasonal[months[i]]
    value = base * seasonal + np.random.normal(0, 15)
    o3.append(max(5, round(value, 1)))

# SO2: very low in Shenzhen, around 5-10
so2 = [max(2, round(np.random.uniform(4, 9) + np.random.normal(0, 1.5), 1)) for _ in range(n)]

# CO: around 0.6-1.0 mg/m3
co_seasonal = {1: 1.15, 2: 1.1, 3: 1.0, 4: 0.9, 5: 0.85, 6: 0.85,
               7: 0.8, 8: 0.85, 9: 0.9, 10: 1.0, 11: 1.1, 12: 1.2}
co = []
for i in range(n):
    seasonal = co_seasonal[months[i]]
    value = 0.8 * seasonal + np.random.normal(0, 0.1)
    co.append(max(0.2, round(value, 2)))

# AQI: simplified calculation based on PM2.5 as primary
# AQI roughly = PM2.5 * 2 for low values, adjusted
aqi = []
for i in range(n):
    # simplified: take max of individual AQIs
    aqi_pm25 = pm25[i] * 1.5 + np.random.normal(0, 5)
    aqi_o3 = o3[i] * 0.6 + np.random.normal(0, 5)
    value = max(aqi_pm25, aqi_o3)
    aqi.append(max(10, round(value)))

# Temperature (Shenzhen subtropical): annual mean ~23C
temp_seasonal = {1: 15, 2: 16, 3: 19, 4: 23, 5: 26, 6: 28,
                 7: 29, 8: 29, 9: 27, 10: 25, 11: 21, 12: 17}
temp = [round(temp_seasonal[months[i]] + np.random.normal(0, 2), 1) for i in range(n)]

# Humidity (%): higher in summer
humid_seasonal = {1: 65, 2: 72, 3: 78, 4: 80, 5: 80, 6: 82,
                  7: 80, 8: 80, 9: 75, 10: 68, 11: 65, 12: 62}
humidity = [max(30, min(100, round(humid_seasonal[months[i]] + np.random.normal(0, 8)))) for i in range(n)]

# Wind speed (m/s)
wind = [max(0.3, round(np.random.uniform(1.5, 4.5) + np.random.normal(0, 0.5), 1)) for _ in range(n)]

# Create DataFrame
df = pd.DataFrame({
    'date': dates,
    'AQI': aqi,
    'PM2.5': pm25,
    'PM10': pm10,
    'NO2': no2,
    'SO2': so2,
    'CO': co,
    'O3_8h_max': o3,
    'temperature': temp,
    'humidity': humidity,
    'wind_speed': wind
})

# Save to CSV
output_path = '/home/node/.openclaw/workspace/gba-air-quality-analysis/data/shenzhen_daily_aqi_2019_2024.csv'
df.to_csv(output_path, index=False)

print(f"Generated {len(df)} rows of data")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"\nAnnual PM2.5 means:")
df['year'] = df['date'].dt.year
print(df.groupby('year')['PM2.5'].mean().round(1))
print(f"\nSample data:")
print(df.head(10).to_string(index=False))
