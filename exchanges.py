import time
from abc import abstractmethod


current_milli_time = lambda: int(round(time.time() * 1000))

class no_ddos:
    __last_req_time = 0
    __interval = 800
    def request(self,url):
        while(self.__last_req_time + self.__interval > current_milli_time()):
            pass
        self.__last_req_time = current_milli_time()
        import requests
        try:
            result = requests.get(url).json()
            if 'error' in result and result['error'] != []:
                print(result['error'])
            return result
        except BaseException:
            print ('exception')
            result = {'error':'request exception','result':()}
            #result = json.dumps({'error':'request exception','result':()}, sort_keys=True)
            return result

class pairs:
    __list_pairs =[]
    def __init__(self):
        self.__list_pairs = self.getPairsx()

    @abstractmethod    
    def getPairsx(self):
      ''''''

    def getPairs(self):
        if self.__list_pairs == [] or 'error' in self.__list_pairs:
            self.__init__()
        return self.__list_pairs





    
