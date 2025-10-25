import pandas as pd

class MovingAverageCrossover:
    def __init__(self,short_window=50,long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self,df, price_col):
        #Generate trading signals based on moving average crossover. (Simple Moving Average)
        #Buy when short MA > long MA, sell when short MA < long MA.

        data = df.copy()

        short_col = f"{price_col}_SMA_short"
        long_col = f"{price_col}_SMA_long"
        signal_col = f"{price_col}_Signal"

        data[short_col] = data[price_col].rolling(window=self.short_window).mean()
        data[long_col] = data[price_col].rolling(window=self.long_window).mean()

        #create signals to indicate -
        # to buy : +1, to sell : -1, to hold : 0

        data["Signals"] = 0
        data.loc[data[short_col] > data[long_col], signal_col] = 1
        data.loc[data[short_col] < data[long_col], signal_col] = -1

        return data

#output : Process finished with exit code 0, meaning no errors - 08/10/25
#backtest code for this strategy is working
