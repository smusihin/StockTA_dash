from abc import abstractmethod


class Indicator:
    def __init__(self):
        self.params = {}

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def calculate(self, df):
        pass

    @abstractmethod
    def params_list(self):
        pass

    def set_params(self, params):
        self.params = params

