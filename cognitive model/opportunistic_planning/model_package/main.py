#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fastDamerauLevenshtein import damerauLevenshtein
from opportunistic_planning import processing, prediction
from scipy.stats import friedmanchisquare, wilcoxon

data = pd.read_csv('all_task_environments_2021-03-17.csv', header=0)
#data = data[:10]

distances_dict = processing.generate_distances_dict(data)

results = processing.calculate_prediction_error(data, distances_dict, error_function='prequential',
          n=10)

lowest_mean, lowest_mean_idx, lowest_median, results_mean = processing.get_lowest_error(results)

