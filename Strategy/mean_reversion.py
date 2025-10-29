#Mean Reversion Strategy

"""
idea :
When prices move too far away from their average, they tend to “revert” back to the mean.

Two popular ways to measure this:
    - Bollinger Bands: Based on moving average ± standard deviation.
    - RSI (Relative Strength Index): Measures overbought/oversold levels.
For simplicity, I will start with the Bollinger Band approach and then the RSI approach.
"""

import pandas as pd
import numpy as np

class BollingerMeanReversionStrategy:
    """
    Mean Reversion strategy using Bollinger Bands.
        - Buy when price is below lower band (oversold)
        - Sell when price is above upper band (overbought)
    """

    def __init__(self, window = 20, num_std = 2):
        self.window = window
        self.num_std = num_std

    def generate_signals(self, df, price_col='EURUSD=X_Close'):
        df = df.copy()

        # # Auto-detect price column if not specified
        # if price_col is None:
        #     price_col = [c for c in df.columns if c.endswith('.Close')]
        #     if not price_col:
        #         raise KeyError("No '.Close' column found in dataframe.")

        if price_col not in df.columns:
            raise ValueError(f"Column '{price_col}' not found in dataframe")

        price_series = df[price_col].astype(float)

        # computing the rolling mean and the standard deviation
        df['rolling_mean'] = price_series.rolling(window=self.window).mean() #Computes moving average (the “mean”)
        df['rolling_std'] = price_series.rolling(window=self.window).std()

        #computing the upper and the lower Bollinger Bands
        #Bollinger Band thresholds(+2 or -2 std by default).
        df['upper_band'] = df['rolling_mean'] + (self.num_std * df['rolling_std'])
        df['lower_band'] = df['rolling_mean'] - (self.num_std * df['rolling_std'])

        # align all relevant columns to prevent shape issues
        # df[['lower_band', 'upper_band']] = df[['lower_band', 'upper_band']].align(price_series, axis=0)

        #generting the trading signals
        df['signals'] = np.where(df[price_col] < df['lower_band'],1,
                                 np.where(df[price_col] > df['upper_band'],-1,0))

        # df[f'{price_col}_Signal'] = np.where(
        #     price_series < df['lower_band'], 1,
        #     np.where(price_series > df['upper_band'], -1, 0)
        # )

        #Buy (1) when price < lower band, Sell (-1) when price > upper band, else hold (0).

        return df

#output : Process finished with exit code 0, meaning no errors - 08/10/25

# class RSIMeanReversionStrategy:
#     def __init__(self, rsi_window = 14, lower_threshold = 30, upper_threshold = 70):
#         # RSI below 30 means “oversold” -> potential buy and
#         # RSI above 70 means “overbought” -> potential sell
#         self.rsi_window = rsi_window #rsi window period = 14 days
#         self.lower_threshold = lower_threshold
#         self.upper_threshold = upper_threshold
#
#     def calculate_rsi(self, series):
#         if isinstance(series, pd.DataFrame):
#             if series.shape[1] == 1:
#                 series = series.iloc[:, 0]
#             else:
#                 raise ValueError("calculate_rsi() expected a 1D Series, got a multi-column DataFrame.")
#
#         series = pd.Series(series).astype(float)
#
#         delta = series.diff()
#         gain = np.where(delta > 0, delta, 0)
#         loss = np.where(delta < 0, -delta, 0)
#
#         avg_gain = pd.Series(gain).rolling(self.rsi_window).mean()
#         avg_loss = pd.Series(loss).rolling(self.rsi_window).mean()
#
#         rs = avg_gain / avg_loss #Relative Strength(rs)
#         rsi = 100 - (100 / (1 + rs))  #this is the formula for RSI
#                                       # Values range between 0 and 100.
#                                       # RSI > 70 → overbought.
#                                       # RSI < 30 → oversold.
#         return rsi
#
#     def generate_signals(self, df, price_col):
#         if isinstance(price_col, str):
#             cols = [price_col]
#         elif isinstance(price_col, (list, tuple)):
#             cols = list(price_col)
#         else:
#             raise TypeError("price_col must be a string or list/tuple of strings.")
#
#         df = df.copy()
#
#         for col in cols:
#             if col not in df.columns:
#                 raise KeyError(f"Column '{col}' not found in dataframe.")
#
#             # Ensure we pass a 1D Series into calculate_rsi
#             series = df[col]
#             if isinstance(series, pd.DataFrame):
#                 # extra safety - should not happen for df[col], but defensive programming
#                 if series.shape[1] == 1:
#                     series = series.iloc[:, 0]
#                 else:
#                     raise ValueError(f"Column '{col}' resolved to a multi-column DataFrame.")
#
#             rsi_col = f"{col}_RSI"
#             signal_col = f"{col}_signal"
#
#             df[rsi_col] = self.calculate_rsi(df[col])  # <--- use df[col] (Series), not df[price_col]
#
#             df[signal_col] = np.where(df[rsi_col] < self.lower_threshold, 1,
#                                       np.where(df[rsi_col] > self.upper_threshold, -1, 0))
#         return df
#
# #output : Process finished with exit code 0, meaning no errors - 08/10/25
