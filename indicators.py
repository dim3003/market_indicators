import datetime, math
import pandas as pd 
import numpy as np
import scipy.stats

class Indicator():
    def __init__(self, df_price=None):
        self.df_price = df_price
        self.returns = self.get_returns()
        self.metrics = self.basic_metrics()
    
    def __str__(self):
        print(50*"=")
        print("METRICS")
        print(50*"-")
        print(self.metrics)
        return ""
    
    @staticmethod
    def _total_returns(returns):
        r = returns + 1
        r = r.product() - 1
        return r

    @staticmethod
    def _confidence_rating(data, mu=0, two_tailed=0):
        """
        Gives back the confidence level in terms of stars for each data column
        - 1 star > 0.9
        - 2 star > 0.95
        - 3 star > 0.99
        """
        
        def perc_to_level(x):
            if x < 0.01:
                return 3
            elif x < 0.05:
                return 2
            elif x < 0.1:
                return 1
            else:
                return 0
        # get the mean
        x_bar = data.mean()
        # get the volatility
        sigma = data.std()
        # z-score
        z = (x_bar-mu)/(sigma/math.sqrt(len(data)))
        # get the percentage of confidence
        p_value = scipy.stats.norm.sf(abs(z)) * (1 + two_tailed)
        #transform to confidence levels
        perc_to_level = np.vectorize(perc_to_level)
        confidence_levels = perc_to_level(p_value)
    
        return confidence_levels

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

    def basic_metrics(self):
        #Set up dataframe
        df = pd.DataFrame(columns=self.df_price.columns)
        #returns
        df.loc["returns",:] = self._total_returns(self.returns).values
        df.loc["returns_confidence_level", :] = self._confidence_rating(self.returns)
        #volatility
        #sharpe
        #TE
        #IR
        #excess returns
        return df
    
    

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

