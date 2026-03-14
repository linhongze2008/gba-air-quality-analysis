# Air Quality Analysis and Prediction in the Greater Bay Area 🌏

## About This Project

This project analyzes air quality trends in Shenzhen, China (part of the Greater Bay Area) using daily monitoring data from 2019 to 2024. As an A-Level Chemistry and Mathematics student living in Shenzhen, I wanted to use data analysis to better understand the air pollution patterns in my city and explore whether the air quality is actually improving.

## Motivation

In my A-Level Chemistry class, we learned about atmospheric pollutants like NO₂, SO₂, and ozone (O₃), and how they affect both the environment and human health. Living in Shenzhen, I often hear news about the city's efforts to improve air quality, but I wanted to see the actual data for myself. This project is my attempt to combine what I've learned in Chemistry and Mathematics with programming to answer some real questions.

## Research Questions

1. Is Shenzhen's air quality actually improving over the past 6 years?
2. How do different pollutants change across seasons, and why?
3. What are the relationships between different pollutants and weather conditions?
4. Can we use simple statistical models to predict future PM2.5 levels?

## Data

- **Source:** Daily air quality monitoring data from Shenzhen environmental monitoring stations
- **Period:** January 2019 – December 2024 (2,192 days)
- **Variables:** AQI, PM2.5, PM10, NO₂, SO₂, CO, O₃, temperature, humidity, wind speed

## Project Structure

```
├── data/
│   └── shenzhen_daily_aqi_2019_2024.csv    # Raw data
├── notebooks/
│   ├── 01_data_exploration.ipynb            # Initial data exploration
│   ├── 02_seasonal_analysis.ipynb           # Seasonal patterns analysis
│   └── 03_prediction_model.ipynb            # Simple prediction model
├── figures/                                  # Generated charts
├── report/
│   └── project_report.pdf                   # Full project report
└── requirements.txt                          # Python dependencies
```

## Key Findings

*(Summary of results will be added after analysis)*

## How to Run

1. Make sure you have Python 3.x installed
2. Install dependencies: `pip install -r requirements.txt`
3. Open the notebooks in order (01 → 02 → 03)

## Tools Used

- Python 3.11
- Pandas (data manipulation)
- Matplotlib & Seaborn (visualization)
- Scikit-learn (prediction model)

## Author

**Jayden Lin (林宏泽)**
A-Level Student (Mathematics, Physics, Chemistry)
Shenzhen Senior High School Group (深圳高级中学高中园)

## Acknowledgments

- Air quality data from Shenzhen Ecological Environment Bureau
- Inspired by my A-Level Chemistry studies on atmospheric chemistry
- Thanks to my teachers for encouraging me to explore beyond the textbook

## License

This project is for educational purposes.
