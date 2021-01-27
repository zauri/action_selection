import numpy as np
import pandas as pd
import ast
from opportunistic_planning.sequence import get_median_edit_distance, filter_for_dimension, get_median_edit_distance_prequential

def calculate_edit_distances(data, distances_dict,
                             dimensions=[[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']], 
                             n=10, seqcol='sequence', coords='coordinates', error='error'):
    ''' Calculates average edit distance for all combinations of parameters (c, k, dimension).
        Input: Dataframe with objects, coordinates, start coordinates, object categories
        Output: Dataframe with edit distance results (col name: parameters used)
    '''

    results = pd.DataFrame()
    
    for row in range(0, len(data)):
        # get information from input row

        objects = list(data.at[row, seqcol])
        coordinates = {key: ast.literal_eval(value) for key, value in
                       (elem.split(': ') for elem in data.at[row, coords].split(';'))}

        start_coordinates = list(ast.literal_eval(data.at[row, 'start_coordinates']))
        ID = str(data.at[row,'ID'])
        seq = str(data.at[row, seqcol])

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
                    c1 = {obj: c if obj in data.at[row, 'containment'] else 1.0 for obj in objects}

                    for dim in dimensions:
                        # get median edit distance for parameter combination
                        median = get_median_edit_distance(ID, objects, coordinates, start_coordinates, c1, k1, dim,
                                                          seq, distances_dict, n)

                        # save parameter combination as col name in results
                        params = 'c: ' + str(c) + '; k: ' + str(k_strong) + ',' + str(k_mid) + ',' + str(
                            k_food) + '; ' + str(dim[1])

                        results.at[row, params] = median

        results.at[row, 'sequence'] = seq
        results.at[row, 'error'] = data.at[row, error]
        results.at[row, 'ID'] = ID

    return results

def calculate_edit_distances_prequential(data, distances_dict,
                             dimensions=[[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']], 
                             n=10, seqcol='sequence', coords='coordinates', error='error'):
    ''' Calculates average edit distance for all combinations of parameters (c, k, dimension).
        Input: Dataframe with objects, coordinates, start coordinates, object categories
        Output: Dataframe with edit distance results (col name: parameters used)
    '''

    results = pd.DataFrame()
    
    for row in range(0, len(data)):
        # get information from input row

        objects = list(data.at[row, seqcol])
        coordinates = {key: ast.literal_eval(value) for key, value in
                       (elem.split(': ') for elem in data.at[row, coords].split(';'))}

        start_coordinates = list(ast.literal_eval(data.at[row, 'start_coordinates']))
        ID = str(data.at[row,'ID'])
        seq = str(data.at[row, seqcol])

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
                    c1 = {obj: c if obj in data.at[row, 'containment'] else 1.0 for obj in objects}

                    for dim in dimensions:
                        # get median edit distance for parameter combination
                        median = get_median_edit_distance_prequential(row, ID, objects, coordinates, start_coordinates, c1, k1, dim,
                                                          seq, distances_dict, n)

                        # save parameter combination as col name in results
                        params = 'c: ' + str(c) + '; k: ' + str(k_strong) + ',' + str(k_mid) + ',' + str(
                            k_food) + '; ' + str(dim[1])

                        results.at[row, params] = median

        results.at[row, 'sequence'] = seq
        results.at[row, 'error'] = data.at[row, error]
        results.at[row, 'ID'] = ID

    return results


def get_lowest_error(results):
    ''' Returns lowest error in dataframe, index of lowest error, mean of lowest error col and 
    the updated dataframe.

    Input: Dataframe of results
    Output: lowest mean error, col where mean error is lowest, lowest median error, mean error, result dataframe
    '''

    for col in list(results):
        if col != 'sequence' and col != 'error' and col != 'ID':
            results.loc['mean', col] = results[col].mean()
            results.loc['median', col] = results[col].median()
    lowest = min(results.loc['mean'])
    lowest_median = min(results.loc['median'])
    mean = list(results.loc['mean'])

    return lowest, results.columns[(results.loc['mean'] == lowest)], lowest_median, mean, results


def generate_distances_dict(data, dimensions=[[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']]):
    distances_dict = {}
    
    for dim in dimensions:
        dimension = dim[1]
        distances_dict[dimension] = {}
    
        for row in range(0,len(data)):
            objects = list(data.at[row,'sequence'])
            ID = str(data.at[row,'ID'])
            start_coordinates = list(ast.literal_eval(data.at[row,'start_coordinates']))
            coordinates = {key: ast.literal_eval(value) for key, value in
                       (elem.split(': ') for elem in data.at[row,'coordinates'].split(';'))}
    
            distances_dict[dimension][ID] = {}
            
            new_coords, new_start_coords = filter_for_dimension(dim, coordinates, start_coordinates)
    
            for pos in new_start_coords:
                try:
                    position = tuple(pos)
                except:
                    position = str(pos)
                
                distances_dict[dimension][ID][position] = {}
                
                for obj in objects:
                    if obj not in distances_dict[dimension][ID][position]:
                        distances_dict[dimension][ID][position][obj] = np.linalg.norm(np.array(pos) -
                                                                     np.array(new_coords[obj]))
                
    return distances_dict


def read_results(file):

	results = pd.read_csv(file, header=0)
	results = results.T
	results.reset_index(drop=True, inplace=True)

	header = results.iloc[0]
	results = results[1:]
	results.columns = header

	results.drop(results.tail(1).index, inplace=True)

	return results


def check_to_float(x):
	try:
		return float(x)
	except:
		return x