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
        cum_max = self.df['TotalValue'].cummax()
        drawdown = (self.df['TotalValue'] - cum_max) / cum_max
        return drawdown

    # 3. CAGR (compound annual growth rate)
    def cagr(self):
        start_val = self.df['TotalValue'].iloc[0]
        end_val = self.df['TotalValue'].iloc[-1]
        num_days = (self.df.index[-1] - self.df.index[0]).days
        years = num_days / 365.25
        return (end_val / start_val) ** (1/years) -1

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

    def compute_sharpe_ratio(self):
        """Compute annualized Sharpe ratio."""
        mean_return = self.df['DailyReturn'].mean()
        std_return = self.df['DailyReturn'].std()
        if std_return == 0:
            return 0
        return (mean_return / std_return) * (252 ** 0.5)

    def compute_max_drawdown(self):
        """Compute maximum drawdown."""
        cumulative = (1 + self.df['DailyReturn']).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return drawdown.min()

    def compute_sortino_ratio(self):
        """Compute Sortino ratio (uses downside deviation)."""
        mean_return = self.df['DailyReturn'].mean()
        downside_std = self.df.loc[self.df['DailyReturn'] < 0, 'DailyReturn'].std()
        if downside_std == 0:
            return 0
        return (mean_return / downside_std) * (252 ** 0.5)

    def compute_all_metrics(self):
        """
        Compute all key performance metrics for the backtest.
        Returns a dictionary of metric names and values.
        """
        df = self.df.copy()

        # Basic returns
        df['CumulativeReturn'] = (1 + df['DailyReturn']).cumprod() - 1

        # Compute metrics
        sharpe_ratio = self.compute_sharpe_ratio()
        max_drawdown = self.compute_max_drawdown()
        total_return = df['CumulativeReturn'].iloc[-1]
        volatility = df['DailyReturn'].std() * (252 ** 0.5)
        sortino_ratio = self.compute_sortino_ratio() if hasattr(self, "compute_sortino_ratio") else None

        # Return metrics dictionary
        metrics = {
            "Total Return": total_return,
            "Volatility (Annualized)": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Sortino Ratio": sortino_ratio,
            "Max Drawdown": max_drawdown
        }

        return metrics

#
# if __name__ == "__main__":
#     import pandas as pd
#
#     # Load example backtest results (the same file your backtest produces)
#     df = pd.read_csv(
#         '/Users/akilfiros/Desktop/Projects/Side Projects /Quant-Backtesting/Data/sample_backtest_results.csv')
#
#     # Ensure Date column is datetime index
#     df['Date.'] = pd.to_datetime(df['Date.'])
#     df.set_index('Date.', inplace=True)
#
#     from Backtester.metrics import PerformanceMetrics
#
#     pm = PerformanceMetrics(df)
#
#     print("=== Performance Summary ===")
#     print(pm.summary())
#
#     pm.plot_return_distribution()
