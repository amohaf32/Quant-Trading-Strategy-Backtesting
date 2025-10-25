"""
Computes and plots:
    - Sharpe ratio
    - Max drawdown
    - CAGR (compound annual growth rate)
    - Win rate / hit ratio
    - Daily returns distribution
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class PerformanceMetrics:
    def __init__(self, result_df, freq = 'daily'):
        """
        results_df: DataFrame with at least ['TotalValue'] column (from backtest output)
        freq: 'daily', 'weekly', or 'monthly' (used for annualization)
        """
        self.df = result_df.copy()
        self.freq = freq
        self._prepare_returns()

    def _prepare_returns(self):
        self.df['DailyReturn'] = self.df['TotalValue'].pct_change()
        self.df.dropna(inplace=True)

    # 1. Sharpe ratio
    def sharpe_ratio(self, risk_free_rate = 0.02):
        mean_return = self.df['DailyReturn'].mean()
        std_return = self.df['DailyReturn'].std()
        trading_days = {'daily':252, 'weekly':50, 'monthly':12}[self.freq]

        sharpe = (mean_return * trading_days - risk_free_rate) / (std_return * np.sqrt(trading_days))
        return sharpe

    # 2. Max drawdown
    def max_drawdown(self):
        cum_max = self.df['TotalReturn'].cummax()
        drawdown = (self.df['TotalReturn'] - cum_max) / cum_max
        return drawdown

    # 3. CAGR (compound annual growth rate)
    def cagr(self):
        start_val = self.df['TotalReturn'].iloc[0]
        end_val = self.df['TotalReturn'].iloc[-1]
        num_days = (self.df.index[-1] - self.df.index[0]).days
        years = num_days / 365.25
        return (end_val - start_val) ** (1/years) -1

    # 4. Win rate / hit ratio
    def win_rate(self):
        win = (self.df['DailyReturn'] > 0).sum()
        total = len(self.df['DailyReturn'])
        return win / total

    # 5. Daily returns distribution
    def plot_return_distribution(self):
        plt.figure(figsize=(8, 5))
        plt.hist(self.df['DailyReturn'], bins=50, color='skyblue', edgecolor='black')
        plt.title("Daily Returns Distribution")
        plt.xlabel("Daily Return")
        plt.ylabel("Frequency")
        plt.show()

    # 6. Summary
    def summary(self):
        metrics = {
            "Sharpe Ratio": round(self.sharpe_ratio(), 3),
            "Max Drawdown": round(self.max_drawdown(), 3),
            "CAGR": f"{self.cagr() * 100:.2f}%",
            "Win Rate": f"{self.win_rate() * 100:.2f}%"
        }
        return pd.Series(metrics)

