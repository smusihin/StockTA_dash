import pandas as pd
from indicator import Indicator


def ema(df, n):
    return df.ewm(span=n, min_periods=0).mean()


class PriceChannels(Indicator):
    def __init__(self):
        Indicator.__init__(self)
        self.set_params({'channel': 20, 'sma': 50})

    def description(self):
        return '''


 '''

    def calculate(self, df):
        result = pd.DataFrame(index=df.index)
        tc = int(self.params_list()['channel'])
        tsma = int(self.params_list()['sma'])
        result['{} sma'.format(tsma)] = df['CLOSE'].rolling(tsma).mean()
        result['4WL'] = df['LOW'].rolling(tc).min()
        result['4WH'] = df['HIGH'].rolling(tc).max()
        return result

    def params_list(self):
        return self.params