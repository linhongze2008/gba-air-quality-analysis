"""
Notebook 02: Seasonal Patterns Analysis
Shenzhen Air Quality Analysis (2019-2024)

This script analyzes how air pollutants vary across different seasons and months,
and explores the relationship between pollutants and weather conditions (temperature/humidity).

Author: Jayden Lin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# set up plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# 1. Load data and add seasonal features
# ============================================================

df = pd.read_csv('data/shenzhen_daily_aqi_2019_2024.csv', parse_dates=['date'])
df['month'] = df['date'].dt.month

# Define seasons (Shenzhen is subtropical)
# Spring: Mar-May, Summer: Jun-Aug, Autumn: Sep-Nov, Winter: Dec-Feb
def get_season(month):
    if month in [3, 4, 5]: return 'Spring'
    elif month in [6, 7, 8]: return 'Summer'
    elif month in [9, 10, 11]: return 'Autumn'
    else: return 'Winter'

df['season'] = df['month'].apply(get_season)
# Ordered categorical type for correct plotting order
df['season'] = pd.Categorical(df['season'], categories=['Spring', 'Summer', 'Autumn', 'Winter'], ordered=True)

print("Data loaded successfully.")

# ============================================================
# 2. Plot: Monthly variations (Box plots)
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# PM2.5 by month
sns.boxplot(x='month', y='PM2.5', data=df, ax=axes[0], color='#3498db', showfliers=False)
axes[0].set_title('Monthly PM2.5 Distribution (2019-2024)', fontsize=12)
axes[0].set_xlabel('Month')
axes[0].set_ylabel('PM2.5 (μg/m³)')
# Add WHO guideline
axes[0].axhline(y=15, color='red', linestyle='--', alpha=0.5, label='WHO Guideline')
axes[0].legend()

# O3 by month
sns.boxplot(x='month', y='O3_8h_max', data=df, ax=axes[1], color='#9b59b6', showfliers=False)
axes[1].set_title('Monthly Ozone (O3) Distribution (2019-2024)', fontsize=12)
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Ozone (μg/m³)')

plt.tight_layout()
plt.savefig('figures/02_monthly_boxplots.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/02_monthly_boxplots.png")

# ============================================================
# 3. Plot: Seasonal comparison of multiple pollutants
# ============================================================

seasonal_means = df.groupby('season')[['PM2.5', 'NO2', 'O3_8h_max']].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
# melt dataframe for easier plotting with seaborn
melted = pd.melt(seasonal_means, id_vars=['season'], var_name='Pollutant', value_name='Concentration')

sns.barplot(x='season', y='Concentration', hue='Pollutant', data=melted, palette=['#3498db', '#e74c3c', '#9b59b6'])
ax.set_title('Average Pollutant Concentrations by Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Concentration (μg/m³)')
ax.set_xlabel('')

# Add annotations
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3, fontsize=9)

plt.tight_layout()
plt.savefig('figures/02_seasonal_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/02_seasonal_comparison.png")

# ============================================================
# 4. Plot: Weather conditions vs Pollutants (Scatter/Hexbin)
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Temperature vs Ozone
sc1 = axes[0].scatter(df['temperature'], df['O3_8h_max'], c=df['month'], cmap='twilight', alpha=0.6, s=15)
axes[0].set_title('Temperature vs Ozone Concentration', fontsize=12)
axes[0].set_xlabel('Temperature (°C)')
axes[0].set_ylabel('Ozone (μg/m³)')
plt.colorbar(sc1, ax=axes[0], label='Month (1-12)')

# Humidity vs PM2.5
sc2 = axes[1].scatter(df['humidity'], df['PM2.5'], c=df['season'].cat.codes, cmap='viridis', alpha=0.5, s=15)
axes[1].set_title('Humidity vs PM2.5 Concentration', fontsize=12)
axes[1].set_xlabel('Humidity (%)')
axes[1].set_ylabel('PM2.5 (μg/m³)')
cbar = plt.colorbar(sc2, ax=axes[1])
cbar.set_ticks([0, 1, 2, 3])
cbar.set_ticklabels(['Spring', 'Summer', 'Autumn', 'Winter'])

plt.tight_layout()
plt.savefig('figures/02_weather_effects.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/02_weather_effects.png")

# ============================================================
# 5. Quick summary
# ============================================================

print("\n" + "=" * 50)
print("SEASONAL PATTERNS - FINDINGS")
print("=" * 50)
print("""
1. PM2.5 and NO2 show strong winter peaks and summer lows.
   - Chemistry connection: Lower temperatures and less rainfall in winter
     reduce atmospheric mixing and wet deposition (washing out) of pollutants.
   
2. Ozone (O3) peaks differently! It's highest in late summer / early autumn.
   - Chemistry connection: Ground-level ozone is a secondary pollutant formed
     by photochemical reactions between NOx and VOCs under sunlight. Higher
     temperatures and stronger sunlight increase this reaction rate.

3. Weather impacts:
   - Positive correlation between temperature and ozone.
   - PM2.5 tends to be lower during very high humidity days (rainy season).
""")