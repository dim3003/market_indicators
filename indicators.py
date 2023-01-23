import pandas as pd 
import numpy as np

class Indicator():
    def __init__(self, df_price=None):
        self.price = df_price
        self.returns = self.get_returns()

    def get_returns(self):
        pass

