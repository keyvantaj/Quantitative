import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn import preprocessing
# from sklearn.impute import SimpleImputer
# imp = SimpleImputer(missing_values=[np.nan, np.inf, -np.inf], strategy='most_frequent')

def Momentum(close,window_length):
    
    momentum = log_Returns(close, window_length)
    
    momentum_drz = pd.DataFrame(data = preprocessing.scale(momentum),
                                                           index = momentum.index,
                                                           columns = momentum.columns)
    return momentum_drz

def Smooth(factor, window_length):
    
    smooth_factor = factor.rolling(window=window_length).mean().iloc[(window_length-1):,:].fillna(0)
    
    return smooth_factor

def Returns(close,window_length):

    returns = close.apply(lambda x:(x - x.shift(window_length))/x).iloc[(window_length-1):,:].fillna(0)

    return returns

def log_Returns(close,window_length):

    returns =  (np.log(close / close.shift(window_length)).iloc[(window_length-1):,:]).fillna(0)
    
    return returns
    
    
def volatility(close, window_length, trailing_window):
    vol = close.pct_change().rolling(window_length).std(ddof=0).rolling(trailing_window).sum()
    
    vol_drz = pd.DataFrame(data = preprocessing.scale(vol),
                                                   index = vol.index,
                                                   columns = vol.columns) 
    
    return vol_drz

def overnight_sentiment(close, openn, window_length, trailing_window):
    
    return_over = pd.DataFrame(index = close.index, columns=close.columns)
    close_shifted = close.apply(lambda x:x.shift(window_length))

    for date in close.index:
        return_over.loc[date] = (openn.loc[date] - close_shifted.loc[date]) / close_shifted.loc[date]

    overnight_sentiment = return_over.rolling(trailing_window).sum()
    
    overnight_sentiment_drz = pd.DataFrame(data = preprocessing.scale(overnight_sentiment),
                                                       index = overnight_sentiment.index,
                                                       columns = overnight_sentiment.columns)  
    
    return overnight_sentiment_drz

def direction(close, openn, window_length, trailing_window):
    
    p = ((close - openn)/close)*-1

    p.replace([np.inf, -np.inf], np.nan, inplace=True)    
    rolling_p = p.rolling(trailing_window).sum()
    
    direction_scaled = pd.DataFrame(data = preprocessing.scale(rolling_p),
                                                       index = rolling_p.index,
                                                       columns = rolling_p.columns)  
    
    return direction_scaled

def sentiment(close, high, low, sent, trailing_window, universe):
    
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
    
def sector_neutral(sectors:dict(), df):
    
    result = []
    for sec in sectors.keys():
        result.append(df[sectors[sec]].sub(df[sectors[sec]].mean(axis=1),axis=0))
    
    df_neutralized = pd.concat(result,axis=1)    
    df_neutralized_scaled = pd.DataFrame(data = preprocessing.scale(df_neutralized),
                                                              index = df_neutralized.index,
                                                              columns = df_neutralized.columns)
    
    return df_neutralized_scaled
    