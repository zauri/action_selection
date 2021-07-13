import numpy as np
import pandas as pd
import ast
from scipy.optimize import minimize
from opportunistic_planning.sequence import get_median_error, filter_for_dimension
from opportunistic_planning.data import read_data, generate_distances_dict

data = read_data('../all_lowest_error/task_environments_test.csv')
data = data.loc[0,:]

def minimize_error(data, distances_dict):
    
    
    get_median_error()