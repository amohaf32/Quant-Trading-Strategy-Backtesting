#Momentum Strategy

"""
idea :

If an asset has been performing well over a certain lookback period (e.g., the past 20 days), it
tends to continue performing well in the near term. Conversely, poor performers tend to continue
underperforming — at least for a while.

You can measure this “momentum” as percentage return over a lookback window,

Then you can:
- Buy (long) when momentum > 0 (price increasing)
- Sell (short) when momentum < 0 (price decreasing)
"""

import pandas as pd
import numpy as np

class MomentumStrategy:
    """
    - Calculate rolling returns over a lookback period.
    - Go long if momentum > 0, short if momentum < 0.
    """
    def __init__(self, lookback = 20): #lookback defined as 20days to look back
        self.lookback = lookback

    def generate_signals(self, data, price_col=None):
        df=data.copy()

        # Auto-detect price column
        if price_col is None:
            price_col = [c for c in df.columns if c.endswith('.Close')]
            if not price_col:
                raise KeyError("No '.Close' column found in dataframe.")
        elif isinstance(price_col, str):
            price_col = [price_col]  # convert single string to list


        for col in price_col:
            momentum_col = f"{col}_Momentum"
            signal_col = f"{col}_Signal"

            # Calculate percentage momentum
            df[momentum_col] = df[col].pct_change(self.lookback)

            # Generate signals
            df[signal_col] = np.where(df[momentum_col] > 0, 1, -1)

        return df

