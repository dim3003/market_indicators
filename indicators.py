import datetime
import pandas as pd 
import numpy as np

class Indicator():
    def __init__(self, df_price=None):
        self.df_price = df_price
        self.returns = self.get_returns()
        self.total_returns = self.total_returns()
    
    def __str__(self):
        print(50*"=")
        print("METRICS")
        print(50*"-")
        print(self.total_returns)
        return ""

    def get_returns(self, ffill=0, percentage_outlier=1):
        """
        Gets returns from the price Dataframe given;
        - ffill # set to 1 if you want missing returns to be forward filled
        - percentage_outliers # set the number above and below which returns are considered outliers 1 = 100%
        """
        df = self.df_price.copy()
        #data cleaning
        if ffill:
            df.fillna(method="ffill", inplace=True)
        df.dropna(inplace=True)
        #get returns
        df_returns = df.pct_change()
        df_returns.dropna(how="all", inplace=True) #remove first empty row
        #change returns outliers to 0
        val = df_returns.values
        og_shape = val.shape
        val = val.ravel()
        df_temp = pd.Series(val)
        df_temp[(df_temp > percentage_outlier) | (df_temp < -percentage_outlier)] = 0
        df_temp = df_temp.values.reshape(og_shape)
        df_returns = pd.DataFrame(df_temp, columns = df_returns.columns, index=df_returns.index)
        return df_returns
    
    def total_returns(self):
        r = self.returns + 1
        r = r.product() - 1
        return r

if __name__ == '__main__':
    print(40*"=")
    print("INDICATOR TEST")
    print(40*"=")
    #get random yahoo finance data
    import yfinance as yf
    start_date = '2020-01-01'
    end_date = datetime.datetime.today()
    ticker = ['GOOGL', 'TSLA']
    data = yf.download(ticker, start_date, end_date)
    price = data.loc[:, 'Close']
    #create indicator object
    indicator = Indicator(df_price=price)
    print(indicator)

