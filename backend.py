import sys, inspect
import pandas as pd
import requests
import os

import importlib
from bitfinex import  *

def get_indicator_list():
    result = []
    for file in os.listdir('indicators'):
        if file[-3:] == '.py':
            result.append(file[:-3])
    return result

def get_indicator(name):
    module = importlib.import_module('indicators.'+name)
    importlib.reload(module)  # Always reload module in case some changes have been made to the strategies
    return getattr(module, name)()

if __name__ == '__main__':
    print(get_indicator_list())
    print(get_indicator('MovingAverage').description())
    #bf = bitfinex()
   # print(bf.get_candles('BTCUSD','1M'))
