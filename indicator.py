from abc import abstractmethod


class Indicator:
    def __init__(self):
        self.params = {}
        self.yaxis = 'y'

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def calculate(self, df):
        pass

    @abstractmethod
    def params_list(self):
        pass

    def set_params(self, params, yaxis = False):
        self.params = params
        if yaxis == True:
            self.yaxis = 'y2'


