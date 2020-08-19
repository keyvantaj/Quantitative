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
class Util:
    
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

    def q_indexing(quantile_to_analyse, df):

        try:
            q_list = []
            for i in quantile_to_analyse:
                q_list.append((df['quantile'] == i))

            df_merge = q_list[0]
            for d in q_list[1:]:       
                df_merge = df_merge ^ d

            q_final_vector = df[df_merge]

        except:

            print ('no specific quantile selected')
            q_final_vector = df

        return q_final_vector


    def quantilize(qunatile_portions, df, weights_col, q_col, sec_col, sec_df):

        quantile_optimal_stacked = pd.DataFrame(index = df.index, 
                                                columns = [weights_col, q_col, sec_col])
        qunatiles = np.linspace(0,1,qunatile_portions+1)
        labels = [i+1 for i in range(len(qunatiles)-1)]

        for date in df.index.levels[0]:

            x = df[weights_col].loc[date.date(),:]

            quantile_optimal_stacked.loc[date,q_col] = pd.qcut(x, qunatiles, 
                                                                    labels = labels)

        quantile_optimal_stacked.loc[:,weights_col] = df[weights_col]
        quantile_optimal_stacked.loc[:,sec_col] = sec_df[sec_col]

        return quantile_optimal_stacked

    def select_sector(df, drop_long_sec, drop_short_sec, sec_col, factor_col):

        try:
            drop_rows_list = []
            for i in drop_long_sec:
                drop_rows_list.append((df.sector == i) & (df[factor_col] == labels[-1]))

            for i in drop_short_sec:
                drop_rows_list.append((df.sector == i) & (df[factor_col] == labels[0]))

            if len(drop_rows_list) == 1:
                df_merge = drop_rows_list[0]
            else:
                df_merge = drop_rows_list[0]

                for d in drop_rows_list[1:]:       
                    df_merge = df_merge ^ d

            final_vector = df[~df_merge]
            sectors = final_vector[sec_col]

        except:
            final_vector = df
            sectors = final_vector[sec_col]

        return  final_vector,sectors

    def rebalancing_to_leverage(df, percent_long_leverage_target,percent_short_leverage_target):

        try:
            for date in df.index.levels[0]:

                long_balance = np.abs(df.loc[date,'optimal_weights'][df.loc[date,'optimal_weights']>0].sum())
                short_balance = np.abs(df.loc[date,'optimal_weights'][df.loc[date,'optimal_weights']<0].sum())

                long_ratio = percent_long_leverage_target / long_balance
                short_ratio = percent_short_leverage_target / short_balance

                df.loc[date,'optimal_weights'][df.loc[date,'optimal_weights']>0] = df.loc[date,'optimal_weights'][df.loc[date,'optimal_weights']>0] * long_ratio
                df.loc[date,'optimal_weights'][df.loc[date,'optimal_weights']<0] = df.loc[date,'optimal_weights'][df.loc[date,'optimal_weights']<0] * short_ratio

        except:

            pass
        return df  
    