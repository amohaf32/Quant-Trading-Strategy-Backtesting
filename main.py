import pandas as pd
from Strategy.moving_average import MovingAverageCrossover
from Backtester.backtest import Backtest

# Load your feature-engineered data
data = pd.read_csv("Data/market_data_features.csv", index_col="Date.", parse_dates=True)

# Initialize your strategy (e.g. 50/200-day crossover)
strategy = MovingAverageCrossover(short_window=50, long_window=200)

# Run backtest
bt = Backtest(data, strategy, initial_capital=100000)
results = bt.run()
bt.summary()
