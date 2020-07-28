import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.decomposition import PCA
from abc import ABC, abstractmethod
import scipy.stats as stats
import cvxpy as cvx

def fit_pca(close, num_factor_exposures, svd_solver):
    
    returns  = close.apply(lambda x:(x - x.shift(1))/x).iloc[1:,:].fillna(0)
    pca = PCA(n_components=num_factor_exposures, svd_solver=svd_solver)
    pca.fit(returns)
    
    return pca  

def factor_betas(pca, returns):

    factor_beta_columns = pca.components_.shape[0]
    factor_betas = pd.DataFrame(pca.components_.T, returns.columns.values, np.arange(factor_beta_columns))
    return factor_betas

def factor_returns(pca, returns, factor_return_indices, factor_return_columns):

    
    factor_returns =pd.DataFrame(pca.transform(returns), factor_return_indices, factor_return_columns)
    return factor_returns

def factor_cov_matrix(factor_returns, ann_factor):

    annualized_factor_covariance_matrix = np.diag(factor_returns.var(axis=0, ddof=1)*ann_factor)
    
    return annualized_factor_covariance_matrix

def idiosyncratic_var_matrix(returns, factor_returns, factor_betas, ann_factor):

    common_returns_ = pd.DataFrame(np.dot(factor_returns, factor_betas.T), returns.index, returns.columns)
    
    residuals_ = (returns - common_returns_)
    specific_risk_matrix = pd.DataFrame(np.diag(np.var(residuals_))*ann_factor, returns.columns, returns.columns)
    return specific_risk_matrix

def idiosyncratic_var_vector(returns, idiosyncratic_var_matrix):

    idiosyncratic_var_vector = pd.DataFrame(np.diag(idiosyncratic_var_matrix),index=returns.columns)   
    return idiosyncratic_var_vector

def predict_portfolio_risk(factor_betas, factor_cov_matrix, idiosyncratic_var_matrix, weights):

    K = factor_betas.dot(factor_cov_matrix).dot(factor_betas.T) + idiosyncratic_var_matrix
    
    predicted_portfolio_risk = np.sqrt(weights.T.dot(K).dot(weights))    
    
    return predicted_portfolio_risk.values[0][0]

def portfolio_risk(close,num_factor_exposures,weights):
    
    try:
        close.index = pd.to_datetime(close.index, format='%Y%m%d')
    except:
        pass
    
    returns  = close.apply(lambda x:(x - x.shift(1))/x).iloc[1:,:].fillna(0)

    pca = fit_pca(close=close,num_factor_exposures=num_factor_exposures,svd_solver='full')

    plt.title('Explained Variance')
    plt.bar(np.arange(num_factor_exposures), pca.explained_variance_ratio_);
    plt.grid(alpha=0.5)
    
    Risk_Model = {}
    Risk_Model['factor_betas'] = factor_betas(pca, returns)


    Risk_Model['factor_returns'] = factor_returns(
    pca,
    returns,
    returns.index,
    np.arange(num_factor_exposures))

    Risk_Model['factor_returns'].cumsum().plot(legend=None);
    plt.grid(alpha=0.5)

    ann_factor = 252
    Risk_Model['factor_cov_matrix'] = factor_cov_matrix(Risk_Model['factor_returns'], ann_factor)

    Risk_Model['idiosyncratic_var_matrix'] = idiosyncratic_var_matrix(returns, Risk_Model['factor_returns'], Risk_Model['factor_betas'], ann_factor)

    Risk_Model['idiosyncratic_var_vector'] = idiosyncratic_var_vector(returns, Risk_Model['idiosyncratic_var_matrix'])

    predicted_portfolio_risk = predict_portfolio_risk(
        Risk_Model['factor_betas'],
        Risk_Model['factor_cov_matrix'],
        Risk_Model['idiosyncratic_var_matrix'],
        weights)    
    
    return predicted_portfolio_risk,Risk_Model 


def portfolio_calculation(portfolio):

    long = portfolio[portfolio['Position']>0]
    short = portfolio[portfolio['Position']<0]
    long_value = long['marketValue'].sum()
    short_value = short['marketValue'].sum()
    grv = long_value + (short_value*-1)

    weights = []
    for tick in portfolio.index:
        weights.append(np.round(portfolio.loc[tick,'marketValue']/grv,4))
        
    all_weights = pd.DataFrame(weights, portfolio.index, columns=['weights'])
    
    return all_weights, long, short, grv
       
        
        
        