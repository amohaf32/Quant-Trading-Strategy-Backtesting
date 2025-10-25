"""
Handles:
    - starting capital
    - available cash
    - open positions
    - total portfolio value
    - logging trades and P&L (Profit and Loss)
"""

import pandas as pd

class Portfolio:
    def __init__(self, initial_capital=100000, transaction_cost=0.001):
        """
        Initialize portfolio with capital and parameters.
        Args:
            initial_capital (float): starting cash in USD.
            transaction_cost (float): cost per trade (e.g., 0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital #this represents the uninvested cash and depending on the trade it
                                    # can decrease or increase
        self.transaction_cost = transaction_cost # Stores the transaction cost percentage as an instance attribute.
        self.positions = {}  #{ticker: number_of_units} #Initializes an empty dictionary to hold current open positions.
        self.portfolio_history = []             #stores the daily portfolio value
        self.trade_log = []                     #stores all the trades

    def update_positions(self,date,ticker,signal,price):
        #Excecutes the trade based on signal: +1=Buy, -1=Sell, 0=Hold

        #position sizing
        if signal == 1: #Buy position
            # to calculate how many whole units can be bought given self.cash and the price after
            # transaction cost.
            units = int(self.cash // (price * (1 + self.transaction_cost)))
            # price * (1 + self.transaction_cost) — price per unit including transaction cost on buy side.
            # self.cash // ... — maximum full units affordable.
            if units <= 0:
                return
            cost = units * price * (1 +self.transaction_cost) #Total cost paid for the buy, including the
            # transaction cost.
            #Example: if you buy 100 units at price 1.25 and transaction_cost 0.001 → cost = 100 * 1.25 * 1.001.
            self.cash -= cost #Deducts the purchase cost from available cash.
            self.positions[ticker] = self.positions.get(ticker, 0) + units
                #self.positions.get(ticker, 0) returns current units held (0 if not present).
                #Adds units (the newly bought amount)
                # this means that multiple buys will accumulate units(positing scaling)

            self.trade_log.append({
                'Date': date,
                'Ticker': ticker,
                'Signal': 'BUY',
                'Units': units,
                'Price': price,
                'Cost': cost,
                'Remaining': self.cash
            })

        # Sell position and the condition also checks ticker in self.positions so you only try to
        # sell if you hold that ticker.
        elif signal == -1 and ticker in self.positions:
            units = self.positions[ticker]
            revenue = units // (price * (1 - self.transaction_cost))
            #Calculates proceeds received by selling the units after transaction cost on the sell side.
            # 1 - transaction_cost reduces revenue by the fee fraction.
            self.cash += revenue # adds the sales proceed to the available cash
            del self.positions[ticker] # removes the position entry because i have sold all unites, this means
            # position closed

            self.trade_log.append({
                'Date': date,
                'Ticker': ticker,
                'Signal': 'SELL',
                'Units': units,
                'Price': price,
                'Revenue': revenue,
                'Remaining': self.cash
            })

    def total_value(self,current_prices):
        #Calculates the total portfolio value = cash + sum of all open positions
        # current_prices : dict like {'EURUSD=X : 1.10', 'GBPUSD_X : 1.25'}

        holding_value = 0.0 #Initialize an accumulator to sum the market value of all open positions.
        for t, units in self.positions.items(): #loops through every position in the portfolio
            price = current_prices.get(t) #fetches every price for the ticker t and if key does not exist in the current_prices
            # then get() will return None
            if price is None:
                raise ValueError(f"Missing price for {t}")
            holding_value += price * units # Accumulates the value of each open position
        return self.cash + holding_value #Returns total portfolio equity: cash plus holdings market value. Type is float

    def record_daily_value(self,date,current_prices):
        # saves the portoflio's daily value (used for performance tracking)

        value = self.total_value(current_prices) #compute current portfolio equity.
        self.portfolio_history.append({
            'Date': date,
            'TotalValue' : value
        })

    def get_history(self):
        # returns dataframe containing portfolio of value over time

        df = pd.DataFrame(self.portfolio_history)
        # Converts self.portfolio_history (list of dicts) into a pandas.DataFrame and returns it.
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df

    def get_trade_log(self):
        # returns the dataframe of executed trades

        return pd.DataFrame(self.trade_log)
        # Converts self.trade_log to a pandas.DataFrame and returns it.



#Process finished with exit code 0 - 09/10/25













