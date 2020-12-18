import pandas as pd
import numpy as np
import ast
from opportunistic_planning import get_median_edit_distance_linalg

def calculate_edit_distances(data,
                             dimensions=[[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']], n=10, seq='sequence', coords='coordinates', error='error'):
    ''' Calculates average edit distance for all combinations of parameters (c, k, dimension).
        Input: Dataframe with objects, coordinates, start coordinates, object categories
        Output: Dataframe with edit distance results (col name: parameters used)
    '''

    results = pd.DataFrame()

    for row in range(0, len(data)):
        # get information from input row

        objects = list(data.at[row, seq])
        coordinates = {key: ast.literal_eval(value) for key, value in
                       (elem.split(': ') for elem in data.at[row, coords].split(';'))}

        start_coordinates = list(ast.literal_eval(data.at[row, 'start_coordinates']))

        sequence = str(data.at[row, seq])

        try:
            strong_k = list(data.at[row, 'strong_k'].split(','))
        except:
            strong_k = []

        try:
            mid_k = list(data.at[row, 'mid_k'].split(','))
        except:
            mid_k = []

        try:
            food_k = list(data.at[row, 'food_k'].split(','))
        except:
            food_k = []

        # set parameters to default values

        c1 = {obj: 1.0 for obj in objects}
        k1 = {obj: 1.0 for obj in objects}

        # go through all possible parameter ranges

        for k2 in np.arange(1.1, 2.0, 0.1):
            k_food = round(k2, 2)
            k1 = {obj: k_food if obj in food_k else 1.0 for obj in objects}

            for k in np.arange(0, 0.9, 0.1):
                k_strong = round(k, 2)
                k_mid = round(k + 0.1, 2)
                k1 = {obj: k_strong if obj in strong_k else k_mid if obj in mid_k else round(k1[obj], 2) for obj in
                      objects}

                for c in np.arange(1.0, 2.0, 0.1):
                    c = round(c, 1)
                    c1 = {obj: c for obj in objects}

                    for dim in dimensions:
                        # get median edit distance for parameter combination
                        median = get_median_edit_distance_linalg.get_median_edit_distance(objects, coordinates, start_coordinates, c1, k1, dim,
                                                          sequence, n)

                        # save parameter combination as col name in results
                        params = 'c: ' + str(c) + '; k: ' + str(k_strong) + ',' + str(k_mid) + ',' + str(
                            k_food) + '; ' + str(dim[1])

                        results.at[row, params] = median

        results.at[row, 'sequence'] = sequence
        results.at[row, 'error'] = data.at[row, error]
        results.at[row, 'ID'] = data.at[row, 'ID']

    return results
