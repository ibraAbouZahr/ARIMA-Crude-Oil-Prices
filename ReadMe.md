# Forecasting Crude Oil Prices with ARIMA

## 🛢️ Introduction

Crude oil prices fluctuate frequently, impacting global markets and refinery companies worldwide. This project uses an **ARIMA (AutoRegressive Integrated Moving Average)** model to forecast crude oil prices one year ahead, helping investors, businesses, and policymakers make informed decisions.

### 📌 Key Features:

- Step-by-step guide on ARIMA modeling
- Data preprocessing and visualization
- Model evaluation and accuracy assessment

---

## ⏳ Understanding Time Series & ARIMA

### 📊 What is Time Series Forecasting?

Time series forecasting involves analyzing sequential data points to predict future values. This is widely used in finance, economics, and resource management.

### Why ARIMA?

**Pros:**
✅ Handles trends & seasonality effectively
✅ Suitable for short-term forecasting

**Cons:**
⚠️ Assumes data stationarity (needs preprocessing)

### 🔢 ARIMA Parameters (p, d, q)

- **p**: Number of lag observations (autoregression)
- **d**: Degree of differencing (to make data stationary)
- **q**: Moving average order

---

## 📚 Data Collection & Preprocessing

**Dataset:** World Bank Pink Sheet Commodity Data (Dec 2024)

- **Time Range:** January 1960 – December 2024
- **Frequency:** Monthly

**🧹 Data Cleaning Steps:**
✔ Dropped unit labels (e.g., $/bbl)
✔ Handled missing values using backward filling
✔ Ensured stationarity with differencing

---

## 📈 Data Analysis & Model Selection

### 📉 Stationarity Check: Augmented Dickey-Fuller (ADF) Test

- **Null Hypothesis:** Data has a unit root (non-stationary)
- **If p-value > 0.05**, data is non-stationary → Apply differencing

### 🔄 Making Data Stationary

- **Differencing**: Removed trends to achieve stationarity
- **Log Transformation**: Stabilized variance (optional)

### 📌 ACF & PACF Analysis

- Determines the best ARIMA parameters:
  - **PACF cutoff → ARIMA(p, d, 0)**
  - **ACF cutoff → ARIMA(0, d, q)**
  - **Both tail off → ARIMA(p, d, q)**

---

## 🚀 Model Training & Forecasting

### 🔧 Fitting the ARIMA Model

Using **ARIMA(2,1,0)** based on ACF & PACF analysis.

```python
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(data, order=(2, 1, 0))
model_fit = model.fit()
print(model_fit.summary())
```

### Forecasting Future Prices

📌 Forecasting next 12 months' crude oil prices.

**Actual vs Forecasted Values:**

- Compared predicted values with real prices
- Evaluated using **Mean Absolute Percentage Error (MAPE)**

### 📊 Model Accuracy Check

✅ **January 2025 Actual Price:** $75.74 per barrel
✅ **Forecasted Price:** $71.60 per barrel
✅ **Model Accuracy:** 94%

---

## 🏆 Conclusion

- Successfully applied ARIMA to forecast crude oil prices
- Achieved **94% accuracy**
- Demonstrated how tuning parameters improves predictions

🚀 **Future Work:**

- Experiment with SARIMA for seasonal patterns
- Incorporate external economic indicators for improved forecasting

📌 **Author:** Ibrahim Abou Zahr

📌 **Dataset Source:** [World Bank Pink Sheet](https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/CMO-Pink-Sheet-December-2024.pdf)

**Happy Forecasting!** 📈
