import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import talib
from datetime import datetime
from sklearn import preprocessing
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.regression.rolling import RollingOLS
# from sklearn.impute import SimpleImputer
# imp = SimpleImputer(missing_values=[np.nan, np.inf, -np.inf], strategy='most_frequent')

class FactorManagement():
    
    def __init__(self):
        
        pass
    
    def momentum(self, close, window_length):
        
        momentum = self.log_Returns(close, window_length)
        momentum_drz = pd.DataFrame(data = preprocessing.scale(momentum),
                                                               index = momentum.index,
                                                               columns = momentum.columns)
        return momentum_drz

    def smooth(self, factor, window_length):

        smooth_factor = factor.rolling(window=window_length).mean().iloc[(window_length-1):,:].fillna(0)

        return smooth_factor

    def returns(self, close, window_length):

        returns = close.apply(lambda x:(x - x.shift(window_length))/x).iloc[(window_length-1):,:].fillna(0)

        return returns

    def log_Returns(self, close, window_length):

        returns =  (np.log(close / close.shift(window_length)).iloc[(window_length-1):,:]).fillna(0)

        return returns


    def volatility(self, close, window_length, trailing_window):
       
        vol = close.pct_change().rolling(window_length).std(ddof=0).rolling(trailing_window).sum()

        vol_drz = pd.DataFrame(data = preprocessing.scale(vol),
                                                       index = vol.index,
                                                       columns = vol.columns) 

        return vol_drz

    def overnight_sentiment(self, close, openn, window_length, trailing_window):

        return_over = pd.DataFrame(index = close.index, columns=close.columns)
        close_shifted = close.apply(lambda x:x.shift(window_length))

        for date in close.index:
            return_over.loc[date] = (openn.loc[date] - close_shifted.loc[date]) / close_shifted.loc[date]

        overnight_sentiment = return_over.rolling(trailing_window).sum()

        overnight_sentiment_drz = pd.DataFrame(data = preprocessing.scale(overnight_sentiment),
                                                           index = overnight_sentiment.index,
                                                           columns = overnight_sentiment.columns)  

        return overnight_sentiment_drz

    def direction(self, close, openn, window_length, trailing_window):

        p = ((close - openn)/close)*-1

        p.replace([np.inf, -np.inf], np.nan, inplace=True)    
        rolling_p = p.rolling(trailing_window).sum()

        direction_scaled = pd.DataFrame(data = preprocessing.scale(rolling_p),
                                                           index = rolling_p.index,
                                                           columns = rolling_p.columns)  

        return direction_scaled
    
    def sma(self, close, window_length):
        
        df= pd.DataFrame(index = close.index)

        try:
            for tick in close.columns:
                df[tick] = talib.SMA(close[tick].values, timeperiod=window_length)
        except:
            pass

        sma_min = ((close - df)/df) * -1
        return sma_min
    
    def sentiment(self, close, high, low, sent, trailing_window, universe):

        indexer = close.index

        total = sent['news_volume'].unstack('ticker')[universe]
        score = sent['sentiment'].unstack('ticker')[universe]

        close = close[universe]
        high = high[universe]
        low = low[universe]

        assert len(close.columns) == len(total.columns) == len(score.columns)

        p = ((high-low)/close)
        v = p.rolling(trailing_window).sum()
        s = (total*score).rolling(trailing_window).sum()
        final = (v*s)*-1

        assert len(final.columns) == len(close.columns)

        sent_factor_scaled = pd.DataFrame(data = preprocessing.scale(final),
                                   index = final.index,
                                   columns = final.columns).reindex(indexer)

        return sent_factor_scaled[universe]

    def sector_neutral(self, sectors:dict(), df):

        result = []
        for sec in sectors.keys():
            result.append(df[sectors[sec]].sub(df[sectors[sec]].mean(axis=1),axis=0))

        df_neutralized = pd.concat(result,axis=1)    
        df_neutralized_scaled = pd.DataFrame(data = preprocessing.scale(df_neutralized),
                                                                  index = df_neutralized.index,
                                                                  columns = df_neutralized.columns)

        return df_neutralized_scaled


    def capm(self, close, market, window_length_return, window_length_beta):

        r_market = self.log_Returns(market,window_length_return).loc[slice(close.index[0],close.index[-1])]

        exog = sm.add_constant(r_market)

        cap_beta = pd.DataFrame(columns=close.columns)

        for tick in close.columns:
            r_assets = self.log_Returns(close[[tick]], window_length_return)

            endog = r_assets
            rols = RollingOLS(endog, exog, window = window_length_beta)
            rres = rols.fit()
            capm = rres.params.dropna()
            capm.columns = ['intercept', 'beta']
            cap_beta.loc[:,tick] = capm['beta']
            
        return cap_beta

    
    def channels(self, close, window_length):

        df_ch = pd.DataFrame(index = close.index, columns = close.columns)

        sl = len(close.index)//window_length 

        for tick in close.columns:

            for i in range(0,len(close.index),window_length): 

                j= i + window_length

                if i == 0:
                    distance = max(close[tick].iloc[-j:]) - min(close[tick].iloc[-j:])
                    df_ch[tick].iloc[-j:] = (close[tick].iloc[-j:] - min(close[tick].iloc[-j:])) / distance

                elif i == sl*window_length:
                    distance = max(close[tick].iloc[:-i]) - min(close[tick].iloc[:-i])
                    df_ch[tick].iloc[:-i] = (close[tick].iloc[:-i] - min(close[tick].iloc[:-i])) / distance

                else:
                    distance = max(close[tick].iloc[-j:-i]) - min(close[tick].iloc[-j:-i])
                    df_ch[tick].iloc[-j:-i] = (close[tick].iloc[-j:-i] - min(close[tick].iloc[-j:-i])) / distance

        return df_ch*-1    