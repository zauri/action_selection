#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fastDamerauLevenshtein import damerauLevenshtein
from opportunistic_planning import data, sequence
from scipy.stats import friedmanchisquare, wilcoxon

envs = pd.read_csv('all_task_environments_2021-03-17.csv', header=0)

distances_dict = data.generate_distances_dict(envs)

results = data.calculate_prediction_error(data, distances_dict, error_function='prequential',
          dimensions=[[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']], 
          n=1, seqcol='sequence', coords='coordinates', error='error')

#lowest_mean, lowest_mean_idx, lowest_median, results = data.get_lowest_error(results)

