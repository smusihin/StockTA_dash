import pandas as pd
from indicator import Indicator

class MACD(Indicator):
    def __init__(self):
        Indicator.__init__(self)
        self.set_params({'n':5})

    def description(self):
        return '''
        MACD (Moving Average Convergence/Divergence)
        
 '''

    def calculate(self, df):
        return df.rolling(int(self.params_list()['n'])).mean()

    def params_list(self):
        return self.params