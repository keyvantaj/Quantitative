import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep, strftime, localtime,time 

sleeptime = 2

#PREPROCESSING
#########################################################
######################################################### 

def cleaning_dataframe(df, pernan_to_drop):
    print ('cleaning data')

    df_cleaned = df.apply(pd.to_numeric, errors='coerce')
    subset = df_cleaned.select_dtypes(exclude=[np.float, np.int])
    col_len = len(subset.columns)
    if col_len != 0:
        df_cleaned.drop(subset.columns,axis=1,inplace=True)
    else:
        print ('columns are clean')
        pass
    #df_cleaned.replace([0,-1], np.nan, inplace=True)

    total = df_cleaned.isna().sum().sort_values(ascending=False)
    percent = (df_cleaned.isna().sum()/df_cleaned.isna().count()).sort_values(ascending=False)
    nan_df_cleaned = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

    f, ax = plt.subplots(figsize=(20, 10))

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(5)
        plt.xticks(rotation='90')

    sns.barplot(x=nan_df_cleaned.index, y=nan_df_cleaned['Percent'])
    plt.xlabel('Features', fontsize=15)
    plt.ylabel('Percent of nan values', fontsize=15)
    plt.title('Percent nan data by feature dataset', fontsize=15)
    plt.grid()
    plt.show()

    features_to_drop = nan_df_cleaned[nan_df_cleaned['Percent']>pernan_to_drop].index
    cleaned_dropna = df_cleaned.drop(features_to_drop, axis=1)
    cleaned_df_all = cleaned_dropna.fillna(cleaned_dropna.mean(level=1))

    print ('The percentage of dropped columns is {}%.'.format(int(((df_cleaned.shape[1] - cleaned_dropna.shape[1])/df_cleaned.shape[1])*100)))
    print ('Dropped {} columns out of {}'.format(len(df.columns)-len(cleaned_df_all.columns),len(df.columns)))
    
    return cleaned_df_all

def demean_multiindex(df):
    
    df_demean = df - df.mean(axis = 0, level = 0)

    return df_demean

def demean(df):
    
    df_demean = df.subtract(df.mean(axis=1), axis=0)

    return df_demean
    
def normalize_multiindex(df):
    
    df_norm = (df - df.min(axis = 0, level = 0)) / (df.max(axis = 0, level = 0) - df.min(axis = 0, level = 0))

    return df_norm

def rank_multiindex(df, ascending=False):
    
    ranked = df.groupby(level=0).rank(ascending=ascending)

    return ranked

def zscore(df):
    
    dfz = (df - df.mean(axis = 0))/df.std(axis = 0,ddof=0) 
    
    return dfz    
    