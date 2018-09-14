import pandas as pd
from indicator import Indicator


def ema(df, n):
    return df.ewm(span=n, min_periods=0).mean()


class ROC(Indicator):
    def __init__(self):
        Indicator.__init__(self)
        self.set_params({'n': 5},True)

    def description(self):
        return '''


The Rate of Change (ROC) is a technical indicator of momentum that measures the percentage change in price between the current price and the price n periods in the past.

The Rate of Change (ROC) is calculated as follows:

    ROC = ((Most recent closing price - Closing price n periods ago) / Closing price n periods ago) x 100

The Rate of Change (ROC) is classed as a momentum indicator because it measures strength of price momentum. For example, if a stock's price at the close of trading today is 10, and the closing price five trading days prior was 7, then the Rate of Change (ROC) over that time frame is approximately 43, calculated as (10 - 7 / 7) x 100 = 42.85.

Positive values indicate upward buying pressure or momentum, while negative values below zero indicate selling pressure or downward momentum. Increasing values in either direction, positive or negative, indicate increasing momentum, and decreasing values indicate waning momentum.

The Rate of Change (ROC) is also sometimes used to indicate overbought or oversold conditions for a security. Positive values that are greater than 30 are generally interpreted as indicating overbought conditions, while negative values lower than negative 30 indicate oversold conditions.


 '''

    def calculate(self, df):
        result = pd.DataFrame(index=df.index)
        n = self.params_list()['n']
        M = df['CLOSE'].diff(n - 1)
        N = df['CLOSE'].shift(n - 1)
        result['ROC'] = (M / N) * 100
        return result

    def params_list(self):
        return self.params