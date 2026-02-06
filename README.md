# Global-Country-emission-modelling
Global CO₂ and GHG emissions analysis using historical country-level data. Includes data cleaning, reporting coverage analysis, annual global aggregation, naïve baseline forecasting, and ARIMA (1,1,1) time-series modeling. Forecasts are evaluated using MAE and RMSE.<br>
This project analyzes historical global CO₂ and total greenhouse gas (GHG) emissions using country-level data and applies time-series forecasting (ARIMA) to model future emission trends.<br>
The analysis emphasizes data quality, transparency, and proper time-series evaluation, making it suitable for climate data studies and forecasting demonstrations.<br>
📂 Dataset<br>
Source: Our World in Data (OWID)<br>
Dataset: CO₂ and Greenhouse Gas Emissions<br>
Link: https://owid-public.owid.io/data/co2/owid-co2-data.csv<br>
The dataset contains annual emissions data for multiple countries, including CO₂, total GHG emissions, and related indicators.<br>
🧪 Methodology<br>
1. Data Preprocessing<br>
Conversion of numeric columns with invalid values coerced to NaN<br>
Separate datasets created for CO₂ and total GHG analysis<br>
Careful handling of missing values to avoid misleading results<br>
2. Coverage Analysis<br>
Counts the number of countries reporting CO₂ and GHG data per year<br>
Helps interpret early-year trends where reporting was incomplete<br>
3. Global Aggregation<br>
Annual global emissions calculated by summing country-level values<br>
Missing years handled responsibly using min_count<br>
4. Time-Series Forecasting<br>
Chronological train–test split (last 5 years held out)<br>
Naïve persistence model used as a baseline<br>
ARIMA (1,1,1) model trained on historical global CO₂ data<br>
5. Evaluation<br>
Forecasts evaluated using:<br>
Mean Absolute Error (MAE)<br>
Root Mean Squared Error (RMSE)<br>
ARIMA performance compared against the naïve baseline<br>
📊 Visualizations<br>
Global CO₂ emissions trend over time<br>
Reporting coverage by year<br>
Forecast vs actual emissions<br>
🛠️ Technologies Used<br>
Python<br>
pandas, NumPy<br>
matplotlib<br>
statsmodels<br>
scikit-learn<br>
🎯 Objective<br>
To demonstrate best practices in environmental time-series analysis, including responsible data handling, baseline comparison, and interpretable forecasting.<br>
📌 License<br>
This project uses publicly available data from Our World in Data. Please cite OWID when using or redistributing results.<br>
