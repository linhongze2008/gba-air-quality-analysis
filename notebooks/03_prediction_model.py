"""
Notebook 03: Correlation and Prediction Model
Shenzhen Air Quality Analysis (2019-2024)

This script analyzes the correlations between different pollutants and weather conditions,
and builds a simple linear regression model to predict PM2.5 levels.

Author: Jayden Lin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# set up plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================
# 1. Load data
# ============================================================
df = pd.read_csv('data/shenzhen_daily_aqi_2019_2024.csv', parse_dates=['date'])
print("Data loaded. Exploring correlations...")

# ============================================================
# 2. Correlation Analysis (Heatmap)
# ============================================================
features_to_correlate = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3_8h_max', 'temperature', 'humidity', 'wind_speed']
corr_matrix = df[features_to_correlate].corr()

fig, ax = plt.subplots(figsize=(10, 8))
# Draw heatmap
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', 
            vmax=1.0, vmin=-1.0, square=True, linewidths=.5, ax=ax)
ax.set_title('Correlation Matrix of Pollutants and Weather Variables', fontsize=14, pad=20)

plt.tight_layout()
plt.savefig('figures/03_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/03_correlation_heatmap.png")

# ============================================================
# 3. Simple Machine Learning Model: Predicting PM2.5
# ============================================================
print("\nBuilding Linear Regression Model for PM2.5 Prediction...")

# We will try to predict PM2.5 using other factors.
# NOTE: In reality, PM10 and PM2.5 are highly correlated because PM2.5 is a subset of PM10.
# We will EXCLUDE PM10 and AQI to make the model more meaningful based on external factors.

# Feature selection
X = df[['NO2', 'SO2', 'CO', 'temperature', 'humidity', 'wind_speed']]
y = df['PM2.5']

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance:")
print(f"RMSE: {rmse:.2f} μg/m³ (Root Mean Squared Error)")
print(f"R-squared: {r2:.2f} (How much variance the model explains)")

# Get feature importance (coefficients)
coefficients = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_
})
coefficients = coefficients.sort_values(by='Coefficient', key=abs, ascending=False)
print("\nFeature Coefficients (Impact on PM2.5):")
print(coefficients.to_string(index=False))

# ============================================================
# 4. Plot: Actual vs Predicted PM2.5
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

# Plot a scatter of actual vs predicted
ax.scatter(y_test, y_pred, alpha=0.5, color='#3498db')
# Plot perfect prediction line (y=x)
max_val = max(y_test.max(), y_pred.max())
min_val = min(y_test.min(), y_pred.min())
ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction (y=x)')

ax.set_title('Linear Regression Model: Actual vs Predicted PM2.5', fontsize=14)
ax.set_xlabel('Actual PM2.5 Concentration (μg/m³)')
ax.set_ylabel('Predicted PM2.5 Concentration (μg/m³)')
ax.legend()

# Add text box with metrics
textstr = f'R² = {r2:.2f}\nRMSE = {rmse:.2f}'
props = dict(boxstyle='round', facecolor='white', alpha=0.8)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('figures/03_model_prediction.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: figures/03_model_prediction.png")

# ============================================================
# 5. Quick summary
# ============================================================

print("\n" + "=" * 50)
print("PREDICTION MODEL - FINDINGS")
print("=" * 50)
print("""
1. Correlations:
   - Strongest positive correlation for PM2.5 is with PM10 (obviously) and NO2.
   - PM2.5 is negatively correlated with temperature (higher temp = lower PM2.5).

2. Model Performance:
   - The R-squared value shows how well simple linear regression works.
   - The coefficients show that NO2 has the highest positive impact on PM2.5 in this model,
     while temperature and wind speed have negative impacts (helping clear the air).

3. Reflection (For the report):
   - Linear regression is very basic. Air pollution is highly non-linear and depends
     on complex atmospheric chemistry and geography.
   - If I had more time, I would try Random Forest or a time-series model like ARIMA,
     and include spatial data (wind direction, neighboring city data).
""")