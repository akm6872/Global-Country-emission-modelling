# Global-Country-emission-modelling
Global CO₂ and GHG emissions analysis using historical country-level data. Includes data cleaning, reporting coverage analysis, annual global aggregation, naïve baseline forecasting, and ARIMA (1,1,1) time-series modeling. Forecasts are evaluated using MAE and RMSE.
This project analyzes historical global CO₂ and total greenhouse gas (GHG) emissions using country-level data and applies time-series forecasting (ARIMA) to model future emission trends.
The analysis emphasizes data quality, transparency, and proper time-series evaluation, making it suitable for climate data studies and forecasting demonstrations.
📂 Dataset
Source: Our World in Data (OWID)
Dataset: CO₂ and Greenhouse Gas Emissions
Link: https://owid-public.owid.io/data/co2/owid-co2-data.csv
The dataset contains annual emissions data for multiple countries, including CO₂, total GHG emissions, and related indicators.
🧪 Methodology
1. Data Preprocessing
Conversion of numeric columns with invalid values coerced to NaN
Separate datasets created for CO₂ and total GHG analysis
Careful handling of missing values to avoid misleading results
2. Coverage Analysis
Counts the number of countries reporting CO₂ and GHG data per year
Helps interpret early-year trends where reporting was incomplete
3. Global Aggregation
Annual global emissions calculated by summing country-level values
Missing years handled responsibly using min_count
4. Time-Series Forecasting
Chronological train–test split (last 5 years held out)
Naïve persistence model used as a baseline
ARIMA (1,1,1) model trained on historical global CO₂ data
5. Evaluation
Forecasts evaluated using:
Mean Absolute Error (MAE)
Root Mean Squared Error (RMSE)
ARIMA performance compared against the naïve baseline
📊 Visualizations
Global CO₂ emissions trend over time
Reporting coverage by year
Forecast vs actual emissions
🛠️ Technologies Used
Python
pandas, NumPy
matplotlib
statsmodels
scikit-learn
🎯 Objective
To demonstrate best practices in environmental time-series analysis, including responsible data handling, baseline comparison, and interpretable forecasting.
📌 License
This project uses publicly available data from Our World in Data. Please cite OWID when using or redistributing results.
