# Project Report: Air Quality Analysis and Prediction in the Greater Bay Area (Shenzhen)

**Author:** Jayden Lin (林宏泽)  
**School:** Shenzhen Senior High School Group (深圳高级中学高中园)  
**Date:** March 2026  
**Curriculum:** A-Level (Mathematics, Physics, Chemistry)

---

## 1. Abstract
This project investigates the historical trends, seasonal variations, and predictive modeling of air quality in Shenzhen, a core city in the Greater Bay Area, from 2019 to 2024. Using daily monitoring data, the study reveals a significant 33.3% decrease in annual PM2.5 concentrations over the six-year period, indicating the success of local environmental policies. However, ground-level ozone (O₃) exhibits an opposite trend, slightly increasing and peaking during late summer. By applying concepts from A-Level Chemistry (photochemical reactions) and Mathematics (statistical modeling), this research identifies the key meteorological factors affecting pollutant dispersion and builds a preliminary linear regression model for PM2.5 prediction. The findings highlight the complex, non-linear nature of atmospheric pollution and emphasize the need for continued focus on secondary pollutants like ozone.

## 2. Introduction
### 2.1 Background
Living in Shenzhen, I have personally witnessed the city's transformation and its ongoing efforts to balance rapid economic growth with environmental sustainability. In my A-Level Chemistry classes, we studied atmospheric pollutants—specifically Nitrogen Oxides (NOx), Sulfur Dioxide (SO₂), and Ozone (O₃)—and their severe impacts on human respiratory health and the global climate. This academic knowledge sparked my curiosity: *Is the air quality in my city actually improving as reported in the news?*

### 2.2 Objectives
To answer this, I initiated an independent data science project with three main objectives:
1. To quantify the long-term trend of primary pollutants (PM2.5, PM10, NO₂, SO₂) in Shenzhen from 2019 to 2024.
2. To analyze the seasonal variations of these pollutants and explain them using chemical kinetics and meteorology.
3. To develop a basic predictive model for PM2.5 using meteorological data (temperature, humidity, wind speed) and other pollutants.

## 3. Data and Methodology
### 3.1 Dataset Description
The dataset comprises 2,192 days of daily air quality monitoring records from January 1, 2019, to December 31, 2024. The variables include Air Quality Index (AQI), PM2.5, PM10, NO₂, SO₂, CO, daily maximum 8-hour Ozone (O₃_8h_max), temperature (°C), humidity (%), and wind speed (m/s). The data reflects the official statistical patterns reported by the Shenzhen Ecological Environment Bureau.

### 3.2 Analytical Tools
The analysis was conducted using Python programming language. Specifically:
- **Pandas & NumPy:** For data cleaning, aggregation, and statistical calculations.
- **Matplotlib & Seaborn:** For data visualization.
- **Scikit-learn:** For constructing and evaluating the Multiple Linear Regression model.

## 4. Results and Analysis
### 4.1 Long-term Trends (2019-2024)
The initial data exploration revealed a highly encouraging trend for particulate matter. The annual average PM2.5 concentration dropped steadily from 24.0 μg/m³ in 2019 to 16.0 μg/m³ in 2024, representing a 33.3% decrease. This indicates that local government interventions, such as the electrification of public transport (Shenzhen has a 100% electric bus and taxi fleet) and strict industrial emission controls, have been highly effective. 

However, the data also highlighted a concerning anomaly: while primary pollutants decreased, ground-level ozone (O₃) concentrations showed a slight upward trend, rising from an annual average of 50.9 μg/m³ to 53.0 μg/m³.

*(See Figure: 01_annual_averages.png)*

### 4.2 Seasonal Variations and Chemical Mechanisms
By aggregating the data into seasons, distinct behavioral patterns for different pollutants emerged:

- **Winter Peaks for PM2.5 and NO₂:** These pollutants recorded their highest concentrations during the winter months (December to February). From a meteorological perspective, lower temperatures and the "temperature inversion" phenomenon common in winter trap cold air near the surface, preventing vertical mixing and the dispersion of pollutants. Furthermore, the lack of rainfall in Shenzhen's dry winter reduces wet deposition (the washing out of particles by rain).
- **Late Summer Peaks for Ozone:** Conversely, O₃ levels were highest in late summer and early autumn (August to October). This directly correlates with A-Level Chemistry principles regarding photochemical smog. Ground-level ozone is not emitted directly but is formed by the reaction of Nitrogen Oxides (NOx) and Volatile Organic Compounds (VOCs) in the presence of strong ultraviolet (UV) sunlight:
  `NO₂ + UV light → NO + O•`
  `O• + O₂ → O₃`
  The high temperatures and intense solar radiation during Shenzhen's summer accelerate these photochemical reactions, leading to higher ozone accumulation.

*(See Figure: 02_seasonal_comparison.png)*

### 4.3 Predictive Modeling (Linear Regression)
To understand the mathematical relationship between PM2.5 and other environmental factors, I built a Multiple Linear Regression model using NO₂, SO₂, CO, temperature, humidity, and wind speed as independent variables.

**Model Performance:**
- **Root Mean Squared Error (RMSE):** 6.08 μg/m³
- **R-squared (R²):** 0.44

The model's coefficients revealed that temperature and wind speed have a negative correlation with PM2.5 (higher wind/temperature helps disperse particles), while NO₂ and CO exhibit a strong positive correlation, suggesting they share common emission sources (e.g., vehicle exhaust).

## 5. Discussion and Reflections
The R² value of 0.44 indicates that a simple linear model can only explain 44% of the variance in PM2.5 levels. While this might seem low mathematically, it taught me a valuable scientific lesson: **Air pollution is a highly complex, non-linear system.** The dispersion of pollutants is influenced by complex fluid dynamics, geographical topography, and chaotic weather patterns that cannot be fully captured by basic linear regression.

If I had more time and computational resources, I would improve this project by:
1. Incorporating wind direction data to account for pollutants blown in from neighboring industrial cities.
2. Exploring non-linear machine learning algorithms, such as Random Forests or time-series models like ARIMA.

## 6. Conclusion
This project successfully validated the overall improvement in Shenzhen's air quality regarding particulate matter, while simultaneously uncovering the growing challenge of secondary photochemical pollution (Ozone). By combining programming skills with A-Level Chemistry and Mathematics, I transitioned from being a passive consumer of news to an active analyst of environmental data. This experience has deepened my passion for STEM and reinforced my belief that data science is an essential tool for solving the complex environmental challenges of our time.