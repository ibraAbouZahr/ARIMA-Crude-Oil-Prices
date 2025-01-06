# Arima

The Arima model assumes that the data is stationary to ensure predictability.

Staionary means that the mean and standard deviation are not changing over time.

# Math behind Augmented Dicky Fuller Test - For stationary classification

![DickyFullerTest](DickyFullerTest.png)

# NOTE: when diff data, leave an original copy just in case

AR - Auto Regressive
I - Integrated , this part is the number of diff required to make the time series stationary. This only makes the mean constant.
MA - Moving Average

# Box-Cox Method to make standard deviation stationary:

Box-Cox method doesn't allow NAN, zero values or negative values

# How to get p:

Use the Partial Auto-Correlation Function (PACF) to determine p, the number of lag observations that are used in the AR (Auto-Regressive) term.

# How to get q:

Use the Auto-Correlation Function (ACF) to determine q, the number of lagged forecast errors used in the MA (Moving Average) term.


# p is the number of lags at which the PACF cuts off.
# q is the number of lags at which the ACF cuts off.
