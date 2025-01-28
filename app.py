import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import statsmodels as arima ## For Arima modeling 
from statsmodels.tsa.stattools import adfuller

st.header("Select World Bank Pink Sheet")
uploaded_file = st.file_uploader("", type=["xlsx"])
if uploaded_file:
    # Load Excel File
    xls = pd.ExcelFile(uploaded_file, engine='openpyxl')
    st.write("Available sheets:", xls.sheet_names)
    
    # Select Data Sheet and Load Data
    sheet_name = st.selectbox("Select the Available Sheets", xls.sheet_names)
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name, skiprows=4, engine='openpyxl')
    
    # Data Cleaning
    df.rename(columns={"Unnamed: 0": "Year"}, inplace=True)
    df = df.drop([0, 1])
    df.replace('…', pd.NA, inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Display Data
    st.subheader("Cleaned Data (First 10 Rows)")
    st.dataframe(df.head(10))
    
    # Showing original graphs:
    
    st.subheader("Data Visualization")
    column_to_plot = st.selectbox("Select a column to plot", df.columns[1:])
    if column_to_plot:
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x="Year", y=column_to_plot, ax=ax)
        ax.set_title(f"Trend of {column_to_plot} Over Years")
        st.pyplot(fig)
        
        
    # Augmented Dickey-Fuller Test for Stationarity
    adFuller = True
    st.header("Augmented Dickey-Fuller Test for Stationarity")
    column_to_test = st.selectbox("Select a column for the ADF test", df.columns[1:])
    if st.button("Run Ad Fuller Test"):
        if column_to_test:
            result = adfuller(df[column_to_test].dropna())
        
        # Display Results
        st.write("### ADF Test Results")
        st.write(f"#### ADF Statistic: {result[0]}")
        st.write(f"#### p-value: {result[1]}")
        st.write("Critical Values:")
        for key, value in result[4].items():
            st.write(f"{key}: {value}")
        
        # Interpretation
        if result[1] < 0.05:
            st.success("The series is stationary.")
            st.text("p value greater than 0.05")
        else:
            st.error("The series is not stationary.")
            st.text("p value less than 0.05")
            adFuller = False


        if adFuller == False:
            countD = 0
            if st.button("Difference Data for Stationarity"):
                df['Crude oil, average_diff'] = df['Crude oil, average'].diff().dropna()
                countD+=countD   
  
                result_diff = adfuller(df['Crude oil, average_diff'].dropna())
                st.write("### ADF Test Results")
                st.write(f"#### ADF Statistic: {result_diff[0]}")
                st.write(f"#### p-value: {result_diff[1]}")
                st.write("Critical Values:")
                st.write(f"Number of diffrenctiations: {countD}")
  
                for key, value in result_diff[4].items():
                    st.write(f"{key}: {value}")
        
                if result_diff[1] < 0.05:
                    st.success("The series is stationary.")
                    st.text("p value greater than 0.05")
                else:
                    st.error("The series is not stationary.")
                    st.text("p value less than 0.05")
            
