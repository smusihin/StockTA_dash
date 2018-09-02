from exchanges import *
import pandas as pd

class bitfinex (pairs,no_ddos):

    def getPairsx(self):
        return self.request('https://api.bitfinex.com/v1/symbols')
    
    def symbol(self, pair_name):
        return 't'+str(pair_name).upper()

    def getTickers(self,args):
        url = 'https://api.bitfinex.com/v2/tickers?symbols='
        for arg in args:
            if str(arg).lower() in self.getPairs():
                url +='t'+str(arg).upper()+','
        url = url[:-1]
        results = {}
        tickers = self.request(url)
        for ticker in tickers:
            results[ticker[0][1:]]={'ask':ticker[3],'bid':ticker[1]}
        return results

    def getTrades(self,pair_name,start=0):
        symbol = self.symbol(pair_name)
        url = 'https://api.bitfinex.com/v2/trades/'+symbol+'/hist?'
        if int(start)>0:
            url += start
        return self.request(url)

    def get_candles(self, symbol, period):
        url = 'https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist'.format(period, symbol)
        result = pd.DataFrame(self.request(url))
        result.columns=['MTS','OPEN','CLOSE','HIGH','LOW','VOLUME']
        result.index = result['MTS']
        return result