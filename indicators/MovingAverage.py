import pandas as pd
from indicator import Indicator

class MovingAverage(Indicator):
    def __init__(self):
        Indicator.__init__(self)
        self.set_params({'n':5})

    def description(self):
        return '''
        A simple moving average is customizable in that it can be calculated for a different number of time periods, simply by adding the closing price of the security for a number of time periods and then dividing this total by the number of time periods, which gives the average price of the security over the time period. A simple moving average smoothes out volatility, and makes it easier to view the price trend of a security. If the simple moving average points up, this means that the security's price is increasing. If it is pointing down it means that the security's price is decreasing. The longer the timeframe for the moving average, the smoother the simple moving average. A shorter-term moving average is more volatile, but its reading is closer to the source data.
        '''

    def calculate(self, df):
        result = pd.DataFrame(index = df.index)
        result['SMA'] = df.rolling(int(self.params_list()['n'])).mean()
        return result

    def params_list(self):
        return self.params


