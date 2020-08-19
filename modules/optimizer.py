import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod
import scipy.stats as stats
import cvxpy as cvx


class AbstractOptimalHoldings(ABC):    
    @abstractmethod
    def _get_obj(self, weights, alpha_vector):
        
        raise NotImplementedError()
    
    @abstractmethod
    def _get_constraints(self, weights, factor_betas, risk):
        
        raise NotImplementedError()
        
    def _get_risk(self, weights, factor_betas, alpha_vector_index, factor_cov_matrix, idiosyncratic_var_vector):
        
        f = factor_betas.loc[alpha_vector_index].values.T * weights
        X = factor_cov_matrix
        S = np.diag(idiosyncratic_var_vector.loc[alpha_vector_index].values.flatten())

        return cvx.quad_form(f, X) + cvx.quad_form(weights, S)
    
    def find(self, alpha_vector, factor_betas, factor_cov_matrix, idiosyncratic_var_vector):
        weights = cvx.Variable(len(alpha_vector))
        risk = self._get_risk(weights, factor_betas, alpha_vector.index, factor_cov_matrix, idiosyncratic_var_vector)
        
        obj = self._get_obj(weights, alpha_vector)
        
        constraints = self._get_constraints(weights, factor_betas.loc[alpha_vector.index].values, risk)
        
        prob = cvx.Problem(obj, constraints)
        prob.solve(max_iters=500)

        optimal_weights = np.asarray(weights.value)
        
        return pd.DataFrame(data=optimal_weights, index=alpha_vector.index, columns=['optimal_weights'] )             
        
        
class OptimalHoldings(AbstractOptimalHoldings):
    
    def __init__(self, risk_cap=0.05, factor_max=10.0, factor_min=-10.0, weights_max=0.5, weights_min=-0.5):
        
        self.risk_cap=risk_cap
        self.factor_max=factor_max
        self.factor_min=factor_min
        self.weights_max=weights_max
        self.weights_min=weights_min
    
    def _get_obj(self, weights, alpha_vector):

        assert(len(alpha_vector.columns) == 1)

        objective = cvx.Maximize(weights * alpha_vector)

        return objective
    
    def _get_constraints(self, weights, factor_betas, risk):

        assert(len(factor_betas.shape) == 2)

        Constraints = [
            risk <= self.risk_cap**2,
            factor_betas.T * weights <= self.factor_max,
            factor_betas.T * weights >= self.factor_min,
            cvx.sum(weights.T) == 0,
            cvx.sum(cvx.abs(weights)) <= 1.0,
            weights >= self.weights_min,
            weights <= self.weights_max
        ]
        
        return Constraints

              
        
class OptimalHoldingsRegularization(OptimalHoldings):
    
    def __init__(self, lambda_reg=0.5, risk_cap=0.05, 
                 factor_max=10.0, factor_min=-10.0, 
                 weights_max=0.2, weights_min=-0.2):
            
        self.lambda_reg = lambda_reg
        self.risk_cap=risk_cap
        self.factor_max=factor_max
        self.factor_min=factor_min
        self.weights_max=weights_max
        self.weights_min=weights_min 
        
    def _get_obj(self, weights, alpha_vector):
        """
        Parameters
        ----------
        weights : CVXPY Variable
            Portfolio weights
        alpha_vector : DataFrame
            Alpha vector

        Returns
        -------
        objective : CVXPY Objective
            Objective function
        """
        assert(len(alpha_vector.columns) == 1)
            
        objective = cvx.Maximize(weights * alpha_vector - self.lambda_reg * cvx.norm(weights, p=2, axis=None))

        return objective

       
        
        
        