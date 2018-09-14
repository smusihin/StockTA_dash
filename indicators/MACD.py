import pandas as pd
from indicator import Indicator


def ema(df,n):
    return df.ewm(span=n,min_periods=0).mean()

class MACD(Indicator):
    def __init__(self):
        Indicator.__init__(self)
        self.set_params({'n':5},True)

    def description(self):
        return '''
        MACD (Moving Average Convergence/Divergence)
        

Developed by Gerald Appel in the late seventies, MACD is one of the simplest and most effective momentum indicators available. MACD turns two trend-following indicators, moving averages, into a momentum oscillator by subtracting the longer moving average from the shorter moving average. A nine-day EMA of the MACD, called the "signal line", is then plotted on top of the MACD, functioning as a trigger for buy and sell signals. As a result, MACD offers the best of both worlds: trend following and momentum.

To calculate MACD, the formula is:

    MACD: (12-day EMA - 26-day EMA)

    Signal: 9-day EMA of the MACD

    Crossover: MACD - Signal 

EMA stands for Exponential Moving Average.
        
 '''


    def calculate(self, df):
        result = pd.DataFrame(index=df.index)
        result['MACD'] = ema(df,12) - ema(df,26)
        result['Signal'] = ema(result['MACD'],9)
        result['Crossover'] = result['MACD'] - result['Signal']
        return result

    def params_list(self):
        return self.params