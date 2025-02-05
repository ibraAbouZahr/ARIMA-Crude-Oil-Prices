import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA


st.set_page_config(page_title="ARIMA Crude Oil Price Forecasting", layout="wide")


st.markdown("<h1 style='text-align: center; margin-top: -20px;'>ARIMA Crude Oil Price Forecasting</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    img {
        border-radius: 15px; 
        padding: 5px;
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("prices.jpg", use_container_width=True, width=400)

# To upload file on sidebar
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Upload World Bank Pink Sheet (Excel)", type=["xlsx"])
    if uploaded_file:
        st.success("File uploaded successfully!")

# Main content
if uploaded_file:
    # Load and clean data
    xls = pd.ExcelFile(uploaded_file, engine='openpyxl')
    sheet_name = st.sidebar.selectbox("Select Sheet", xls.sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=4, engine='openpyxl')
    
    
    df.rename(columns={"Unnamed: 0": "Year"}, inplace=True)
    df = df.drop([0, 1])
    df.replace('…', pd.NA, inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Display cleaned data
    st.header("Cleaned Data")
    st.dataframe(df.head(10))

    # Data Visualization
    st.header("Data Visualization")
    column_to_plot = st.selectbox("Select a Column to Plot", df.columns[1:])
    if column_to_plot:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x="Year", y=column_to_plot, ax=ax, marker='o')
        ax.set_title(f"Trend of Crude Oil Prices Over Years", fontsize=16)
        ax.set_xlabel("Year", fontsize=14)
        ax.set_ylabel("$/bbl", fontsize=14)
        ax.grid(True)
        st.pyplot(fig)

    # ADF Test
    st.header("Stationarity Check (ADF Test)")
    column_to_test = st.selectbox("Select a Column for ADF Test", df.columns[1:])
    d = 0
    if column_to_test:
        result = adfuller(df[column_to_test].dropna())
        
        # Display ADF results
        st.subheader("ADF Test Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ADF Statistic", f"{result[0]:.4f}")
        with col2:
            st.metric("p-value", f"{result[1]:.4f}")
        
        st.write("**Critical Values:**")
        for key, value in result[4].items():
            st.write(f"{key}: {value:.4f}")
        
        if result[1] < 0.05:
            st.success("The series is stationary (p-value < 0.05).")
        else:
            st.warning("The series is not stationary (p-value ≥ 0.05). Consider differencing the data.")

            # Differencing
            st.subheader("Differencing")
            if st.checkbox("Apply Differencing"):
                df[f'{column_to_test}_diff'] = df[column_to_test].diff().dropna()
                d = d + 1
            
                # Plot differenced data
                fig_diff, ax_diff = plt.subplots(figsize=(10, 6))
                sns.lineplot(data=df, x="Year", y=f'{column_to_test}_diff', ax=ax_diff, marker='o', color='orange')
                ax_diff.set_title(f"Differenced Series: {column_to_test}", fontsize=16)
                ax_diff.set_xlabel("Year", fontsize=14)
                ax_diff.set_ylabel(f"{column_to_test}_diff", fontsize=14)
                ax_diff.grid(True)
                st.pyplot(fig_diff)
                
                # ADF test on differenced data
                result_diff = adfuller(df[f'{column_to_test}_diff'].dropna())
                st.subheader("ADF Test Results on Differenced Data")
                col1_diff, col2_diff = st.columns(2)
                with col1_diff:
                    st.metric("ADF Statistic", f"{result_diff[0]:.4f}")
                with col2_diff:
                    st.metric("p-value", f"{result_diff[1]:.10e}")
                
                if result_diff[1] < 0.05:
                    st.success("The differenced series is stationary (p-value < 0.05).")
                    st.subheader("ACF & PACF plots after differencing: ")
                    fig_acf_pacf, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
                    
                    plot_acf(df[f'{column_to_test}_diff'].dropna(), lags=20, ax=ax1)
                    ax1.set_title("ACF for Differenced Data:")
                    
                    
                    
                    plot_pacf(df[f'{column_to_test}_diff'].dropna(), lags=20, ax=ax2)
                    ax2.set_title("PACF for Differenced Data:")
                    
           
                    st.pyplot(fig_acf_pacf)
                else:
                    st.error("The series is still not stationary. Further transformations may be needed.")
                    
    st.header("ARIMA Model Fitting")
    st.text("*Only Fit When Data is Stationary*")
    st.subheader("Select Arima Parameters (p, d, q)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        p = st.number_input("Enter value of p: ",  min_value=0)
    with col2:
        d = st.number_input("Enter value of d (Based on Differencing Count): ",  min_value=0)
    with col3:
        q = st.number_input("Enter valeu of q: ",  min_value=0)
    
    
    if st.button("Fit Arima Model"):
        try:
            train = df[column_to_test][:-12]  # 12 Months
            test = df[column_to_test][-12:]
            
            # Fitting the model 
            model = ARIMA(train, order=(p, d, q))
            results = model.fit()
            
            forecast = results.forecast(steps=12)
            
            st.subheader("Actual vs Forecasted Values")
            fig_forecast, ax_forecast = plt.subplots(figsize=(10, 6))
            ax_forecast.plot(test.index, test, label='Actual')
            ax_forecast.plot(test.index, forecast, label='Forecast')
            ax_forecast.set_title('Actual vs Forecasted Crude Oil Prices')
            ax_forecast.set_xlabel('Date')
            ax_forecast.set_ylabel('Price ($/bbl)')
            ax_forecast.legend()
            st.pyplot(fig_forecast)
            
            # Get MAPE (Error Margin), in this case 5.21%
            mape = np.mean(np.abs((test - forecast) / test)) * 100
            st.metric("Mean Absolute Percentage Error (MAPE)", f"{mape:.2f}%")
            
            df.index = pd.date_range(start=df.index[0], periods=len(df), freq='MS')

            # I Refit the model again but on the entire database instead of splitting it into training and testing sets.
            final_model = ARIMA(df['Crude oil, average'], order=(2, 1, 0))
            final_results = final_model.fit()

            # Forecast for the next 12 months
          
            df.index = pd.date_range(start=df.index[0], periods=len(df), freq='MS')
            future_forecast = final_results.forecast(steps=12)
            fig_final_forecast, ax_final_forecast = plt.subplots(figsize=(10, 6))
            ax_final_forecast.plot(df[column_to_test], label='Historical Data')
            ax_final_forecast.plot(future_forecast.index, future_forecast, label='Forecast', color='red')
            ax_final_forecast.set_title('Crude Oil Price Forecast (Next 12 Months)')
            ax_final_forecast.set_xlabel('Date')
            ax_final_forecast.set_ylabel('Price ($/bbl)')
            ax_final_forecast.legend()
            st.pyplot(fig_final_forecast)

            
            st.subheader("Forecasted Values")
            st.write(future_forecast)

        
        except Exception as e:
            st.error(f"Error fitting ARIMA model: {e}")
else:
    st.info("Please upload an Excel file to get started. (In Sidebar)")
