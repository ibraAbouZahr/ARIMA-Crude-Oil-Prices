# ARIMA Crude Oil Price Forecasting

## Project Overview

This project uses the ARIMA (AutoRegressive Integrated Moving Average) model to forecast crude oil prices by using the World Bank pinksheet as data. The goal is to provide predictions one year ahead based on historical data which assists in risk management and descion making.

---

## **Features**

1- Data Loading and Cleaning:

. Load historical crude oil price data from the World Bank Pink Sheet.

. Handle missing values and ensure data consistency.

2- Exploratory Data Analysis (EDA):

. Visualize historical crude oil prices to identify trends, seasonality, and anomalies.

. Perform statistical tests (e.g., Augmented Dickey-Fuller test) to check for stationarity.

3- ARIMA Modeling:

. Fit an ARIMA model to the data, selecting optimal parameters (p, d, q) using ACF/PACF plots and statistical tests.

. Validate the model using out-of-sample testing and calculate performance metrics (e.g., MAPE).

4- Forecasting:

. Generate forecasts for future crude oil prices (e.g., 12 months ahead).

. Visualize the forecasted prices alongside historical data.

5- Interactive Interface:

. Provide a user-friendly interface (built with Streamlit) to explore historical data, adjust model parameters, and view forecasts.
