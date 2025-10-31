import os
import argparse
import pandas as pd
from Strategy.moving_average import MovingAverageCrossover
from Strategy.momentum import MomentumStrategy
from Strategy.mean_reversion import BollingerMeanReversionStrategy
from Backtester.backtest import Backtest
from Reports.reporting import (
    plot_equity_curve,
    plot_drawdown,
    export_performance_summary,
    save_trade_log,
)

parser = argparse.ArgumentParser(description="Run backtest and generate reports")
parser.add_argument("--ticker", type=str, default="EURUSD=X", help="Ticker symbol matching '<TICKER>.Close' column")
parser.add_argument("--strategy", type=str, default="moving_average", choices=["moving_average", "momentum", "mean_reversion"], help="Strategy to run")
parser.add_argument("--short_window", type=int, default=50, help="Short window for moving average")
parser.add_argument("--long_window", type=int, default=200, help="Long window for moving average")
parser.add_argument("--lookback", type=int, default=20, help="Lookback for momentum strategy")
parser.add_argument("--mr_window", type=int, default=20, help="Window for Bollinger mean reversion")
parser.add_argument("--mr_std", type=float, default=2.0, help="Std dev for Bollinger mean reversion")
parser.add_argument("--initial_capital", type=float, default=100000, help="Starting capital")
parser.add_argument("--transaction_cost", type=float, default=0.001, help="Transaction cost (e.g., 0.001 = 0.1%)")
parser.add_argument("--start", type=str, default=None, help="Start date (YYYY-MM-DD)")
parser.add_argument("--end", type=str, default=None, help="End date (YYYY-MM-DD)")
parser.add_argument("--data", type=str, default=None, help="Path to CSV; defaults to Data/market_data_features.csv")
parser.add_argument("--outdir", type=str, default=None, help="Output directory; defaults to Reports/outputs")
args = parser.parse_args()

# Load your feature-engineered data (resolve relative to this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = args.data or os.path.join(BASE_DIR, "Data", "market_data_features.csv")
data = pd.read_csv(data_path, index_col="Date.", parse_dates=True)

# Optional date filtering
if args.start:
    data = data[data.index >= args.start]
if args.end:
    data = data[data.index <= args.end]

# Initialize your strategy
if args.strategy == "moving_average":
    strategy = MovingAverageCrossover(short_window=args.short_window, long_window=args.long_window)
elif args.strategy == "momentum":
    strategy = MomentumStrategy(lookback=args.lookback)
else:
    strategy = BollingerMeanReversionStrategy(window=args.mr_window, num_std=args.mr_std)

# Run backtest
bt = Backtest(data, strategy, ticker=args.ticker, initial_capital=args.initial_capital, transaction_cost=args.transaction_cost)
results = bt.run()
bt.summary()

# Reporting outputs
reports_dir = args.outdir or os.path.join("Reports", "outputs")
equity_path = os.path.join(reports_dir, "equity_curve.png")
drawdown_path = os.path.join(reports_dir, "drawdown.png")
summary_csv_path = os.path.join(reports_dir, "performance_summary.csv")
trades_csv_path = os.path.join(reports_dir, "trade_log.csv")

# Plots
plot_equity_curve(results, save_path=equity_path)
plot_drawdown(results, save_path=drawdown_path)

# Summary export
summary_df = export_performance_summary(results, save_csv_path=summary_csv_path)

# Trades export
trade_log_df = bt.portfolio.get_trade_log()
save_trade_log(trade_log_df, trades_csv_path)

# Save results timeseries
os.makedirs(reports_dir, exist_ok=True)
results.to_csv(os.path.join(reports_dir, "results_timeseries.csv"))

print("Reports saved to:", reports_dir)
