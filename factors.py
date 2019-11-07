import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import utils




def momentum(close,window_length):
    
    momentum = close.apply(lambda x:(x - x.shift(window_length))/x).iloc[(window_length-1):,:].fillna(0)
    momentum_dr = utils.demean(momentum).rank(axis=1)
    momentum_drz = utils.zscore(momentum_dr)
    
    return momentum_drz


def smooth_factor(factor, window_length):
    
    smooth_factor = utils.zscore((utils.demean(factor.rolling(window=window_length).mean()).rank(axis=1))).iloc[(window_length-1):,:]
    return smooth_factor