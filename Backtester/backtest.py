"""
Does the loop:
    - reads signals from strategy
    - executes trades
    - updates portfolio each day
    - stores daily results
"""
try:
    import Backtester.portfolio as portfolio
except ModuleNotFoundError:
    # Allow running this file directly by adding the project root to sys.path
    import sys
    from pathlib import Path
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
    import Backtester.portfolio as portfolio

class Backtest:
    def __init__(self, data, strategy, ticker='EURUSD=X', initial_capital=100000, transaction_cost=0.001):
        """
        Runs a backtest for a given strategy and dataset.
        Args:
            data (pd.DataFrame): time series data (must include 'Close').
            strategy (object): strategy instance with generate_signals(data).
            initial_capital (float): starting portfolio value.
        """

        self.data = data.copy()
        self.strategy = strategy
        self.ticker = ticker
        self.portfolio = portfolio.Portfolio(initial_capital=initial_capital, transaction_cost=transaction_cost)
        self.results = None

    def run(self):

        price_col = f'{self.ticker}.Close'

        df_signals = self.strategy.generate_signals(
            self.data,
            price_col=price_col
        )
        self.data['Signal'] = df_signals[f"{price_col}_Signal"]

        for date, row in self.data.iterrows():
            price = row[price_col]
            signal = row['Signal']

            self.portfolio.update_positions(date, self.ticker, signal, price)

            # current_prices = {self.ticker: price}
            self.portfolio.record_daily_value(date, {self.ticker: price})

        self.results = self.portfolio.get_history()
        return self.results

    def summary(self):
        """""
        Print summary of the portfolio.
        """
        if self.results is None:
            print("Run the backtest first using .run()")
            return

        start_val = self.results['TotalValue'].iloc[0]
        end_val = self.results['TotalValue'].iloc[-1]
        returns = (end_val - start_val) / start_val * 100
        print(f'Initial capital: ${start_val:.2f}')
        print(f'Final Portfolio Value: ${end_val:.2f}')
        print(f"Total return: {returns:.2f}")

        #to show the trade log summary
        trades = self.portfolio.get_trade_log()
        print (f"Total trades Executed: {len(trades)}")
        print(trades.tail())





