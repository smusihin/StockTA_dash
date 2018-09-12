import pandas as pd
from indicator import Indicator


def ema(df, n):
    return df.ewm(span=n, min_periods=0).mean()


class BollingerBands(Indicator):
    def __init__(self):
        Indicator.__init__(self)
        self.set_params({'n': 5})

    def description(self):
        return '''


 '''

    def calculate(self, df):
        result = pd.DataFrame(index=df.index)
        result['20 ma'] = ema(df, 20)
        sd = df.rolling(20).std()
        result['Upper Band'] = result['20 ma'] + (sd *2)
        result['Lower Band'] = result['20 ma'] - (sd *2)
        return result

    def params_list(self):
        return self.params