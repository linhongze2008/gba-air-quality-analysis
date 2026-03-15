"""
Notebook 01: Data Exploration
Shenzhen Air Quality Analysis (2019-2024)

This script explores the basic structure and statistics of the dataset,
and creates initial visualizations to understand overall trends.

Author: Jayden Lin
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# set up plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# 1. Load and inspect the data
# ============================================================

df = pd.read_csv('data/shenzhen_daily_aqi_2019_2024.csv', parse_dates=['date'])

print("=" * 50)
print("SHENZHEN AIR QUALITY DATA - OVERVIEW")
print("=" * 50)
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"\nColumns: {list(df.columns)}")

print("\n--- Basic Statistics ---")
print(df.describe().round(2))

# check for missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# ============================================================
# 2. Annual average pollutant concentrations
# ============================================================

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

annual_means = df.groupby('year')[['AQI', 'PM2.5', 'PM10', 'NO2', 'SO2', 'O3_8h_max']].mean().round(1)
print("\n--- Annual Average Concentrations (ug/m3) ---")
print(annual_means)

# ============================================================
# 3. Plot: Overall PM2.5 trend over 6 years
# ============================================================

fig, ax = plt.subplots(figsize=(12, 5))

# daily values (light color) + 30-day rolling average (bold)
ax.plot(df['date'], df['PM2.5'], alpha=0.2, color='steelblue', linewidth=0.5, label='Daily PM2.5')
rolling_avg = df['PM2.5'].rolling(window=30).mean()
ax.plot(df['date'], rolling_avg, color='darkblue', linewidth=1.5, label='30-day Rolling Average')

# WHO guideline
ax.axhline(y=15, color='red', linestyle='--', alpha=0.7, label='WHO Guideline (15 μg/m³)')
# China national standard
ax.axhline(y=35, color='orange', linestyle='--', alpha=0.7, label='China Standard (35 μg/m³)')

ax.set_xlabel('Date')
ax.set_ylabel('PM2.5 Concentration (μg/m³)')
ax.set_title('Daily PM2.5 Levels in Shenzhen (2019-2024)')
ax.legend(loc='upper right')
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.tight_layout()
plt.savefig('figures/01_pm25_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved: figures/01_pm25_trend.png")

# ============================================================
# 4. Plot: Annual average bar chart for all pollutants
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3_8h_max', 'AQI']
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']

for idx, (pollutant, color) in enumerate(zip(pollutants, colors)):
    ax = axes[idx // 3, idx % 3]
    yearly = df.groupby('year')[pollutant].mean()
    ax.bar(yearly.index.astype(str), yearly.values, color=color, alpha=0.8)
    ax.set_title(f'{pollutant} Annual Mean')
    ax.set_ylabel('μg/m³' if pollutant != 'AQI' else 'Index')
    
    # add value labels on bars
    for i, v in enumerate(yearly.values):
        ax.text(i, v + 0.5, f'{v:.1f}', ha='center', fontsize=8)

plt.suptitle('Annual Average Pollutant Levels in Shenzhen (2019-2024)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/01_annual_averages.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/01_annual_averages.png")

# ============================================================
# 5. Plot: Distribution of AQI categories
# ============================================================

def aqi_category(aqi):
    """Classify AQI into standard categories"""
    if aqi <= 50:
        return 'Good (0-50)'
    elif aqi <= 100:
        return 'Moderate (51-100)'
    elif aqi <= 150:
        return 'Unhealthy for Sensitive (101-150)'
    elif aqi <= 200:
        return 'Unhealthy (151-200)'
    else:
        return 'Very Unhealthy (200+)'

df['AQI_category'] = df['AQI'].apply(aqi_category)

# count by year and category
cat_order = ['Good (0-50)', 'Moderate (51-100)', 'Unhealthy for Sensitive (101-150)', 
             'Unhealthy (151-200)', 'Very Unhealthy (200+)']
cat_colors = ['#27ae60', '#f1c40f', '#e67e22', '#e74c3c', '#8e44ad']

fig, ax = plt.subplots(figsize=(10, 5))
cat_counts = df.groupby(['year', 'AQI_category']).size().unstack(fill_value=0)
# reorder columns
cat_counts = cat_counts.reindex(columns=cat_order, fill_value=0)
cat_counts.plot(kind='bar', stacked=True, color=cat_colors, ax=ax, alpha=0.85)

ax.set_xlabel('Year')
ax.set_ylabel('Number of Days')
ax.set_title('Distribution of AQI Categories by Year')
ax.legend(title='AQI Category', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
ax.set_xticklabels(cat_counts.index, rotation=0)

plt.tight_layout()
plt.savefig('figures/01_aqi_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/01_aqi_distribution.png")

# ============================================================
# 6. Quick summary
# ============================================================

print("\n" + "=" * 50)
print("INITIAL FINDINGS")
print("=" * 50)
print(f"""
1. PM2.5 shows a clear decreasing trend:
   - 2019 average: {annual_means.loc[2019, 'PM2.5']} μg/m³
   - 2024 average: {annual_means.loc[2024, 'PM2.5']} μg/m³
   - That's a {((annual_means.loc[2019, 'PM2.5'] - annual_means.loc[2024, 'PM2.5']) / annual_means.loc[2019, 'PM2.5'] * 100):.1f}% decrease!

2. O3 (ozone) does NOT show the same improvement - it's actually
   slightly increasing, which is a concern.

3. Most days fall in the 'Good' or 'Moderate' AQI categories,
   showing Shenzhen has relatively good air quality compared to
   other major Chinese cities.

4. Next step: Look at seasonal patterns to understand WHY these
   trends exist (notebook 02).
""")
