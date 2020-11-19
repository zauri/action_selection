import pandas as pd
import numpy as np
import random
import ast
from scipy.spatial import distance
from fastDamerauLevenshtein import damerauLevenshtein


def predict_sequence(objects, coordinates, start_coordinates, c, k, dimension=[3, ]):
    ''' Predicts sequence based on required objects, object coordinates, start coordinates of subject,
        parameters (c+k) and dimensionality.
        Input: Objects, object coordinates, start coordinates, c, k, dimension
        Output: Sequence of objects as str
    '''
    prediction = []
    possible_items = dict.fromkeys(objects, 0)  # generate dict from object list
    coord_index = 0
    start_coords = start_coordinates
    coords = coordinates
    new_coords = {}
    new_start_coords = []

    if dimension[0] == 3:  # no changes if 3D
        new_coords = coords
        new_start_coords = start_coords

    elif dimension[0] == 2:  # 2D: remove obsolete coordinate
        if dimension[1] == 'xy':
            new_coords = {key: value[:-1] for key, value in coords.items()}
            new_start_coords = [x[:-1] for x in start_coords]

        elif dimension[1] == 'xz':
            new_start_coords = [[x[0], x[-1]] for x in start_coords]

            for key, value in coords.items():
                new_value = (value[0], value[-1])
                new_coords[key] = new_value

        elif dimension[1] == 'yz':
            new_coords = {key: value[1:] for key, value in coords.items()}
            new_start_coords = [x[1:] for x in start_coords]

    elif dimension[0] == 1:  # 1D: choose appropriate coordinate
        if dimension[1] == 'x':
            new_coords = {key: value[0] for key, value in coords.items()}
            new_start_coords = [x[0] for x in start_coords]

        elif dimension[1] == 'y':
            new_coords = {key: value[1] for key, value in coords.items()}
            new_start_coords = [x[1] for x in start_coords]

        elif dimension[1] == 'z':
            new_coords = {key: value[2] for key, value in coords.items()}
            new_start_coords = [x[2] for x in start_coords]

    while bool(possible_items) == True:  # while dict not empty
        for obj in possible_items.keys():
            # calculate euclidean distance between current location and items
            possible_items[obj] = ((distance.euclidean(
                new_start_coords[coord_index],
                new_coords[obj])
                                   ) ** k[obj]) * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        prediction.append(minval)
        del possible_items[minval]
        coord_index += 1

    return prediction


def get_median(objects, coordinates, start_coordinates, c, k, dimension, sequence, n=100):
    ''' Returns average edit distance (Damerau-Levenshtein) for n trials of sequence prediction.
    '''
    edit_list = []

    for x in range(0, n):
        result = ''.join(predict_sequence(objects, coordinates, start_coordinates, c, k, dimension))
        dl = damerauLevenshtein(sequence, result)
        edit_list.append(dl)

    median = np.median(edit_list)
    return median


def get_avg_editdist(data, dimensions=[[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']], n=10,
                     seq='sequence_original', coords='coordinates_original', error='error_original'):
    ''' Calculates average edit distance for all combinations of parameters (c, k, dimension).
        Input: Dataframe with objects, coordinates, start coordinates, object categories
        Output: Dataframe with edit distance results (col name: parameters used)
    '''
    results = pd.DataFrame()

    for row in range(0, len(data)):
        objects = list(data.at[row, seq])
        strong_k = list(data.at[row, 'strong_k'].split(','))
        mid_k = list(data.at[row, 'mid_k'].split(','))
        food_k = list(data.at[row, 'food_k'].split(','))
        coordinates = {key: ast.literal_eval(value) for key, value in
                       (elem.split(': ') for elem in data.at[row, coords].split(';'))}
        start_coordinates = list(ast.literal_eval(data.at[row, 'start_coordinates']))
        sequence = str(data.at[row, seq])

        c1 = {obj: 1.2 for obj in objects}
        k1 = {obj: 1.0 for obj in objects}

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
                        median = get_median(objects, coordinates, start_coordinates, c1, k1, dim, sequence, n)
                        params = 'c: ' + str(c) + '; k: ' + str(k_strong) + ',' + str(k_mid) + ',' + str(
                            k_food) + '; ' + str(dim[1])
                        results.at[row, params] = median

        results.at[row, 'sequence'] = sequence
        results.at[row, 'error'] = data.at[row, error]
        results.at[row, 'ID'] = data.at[row, 'ID']

    return results


def get_lowest_error(results):
    ''' Returns lowest error in dataframe and index of lowest error.
    '''
    for col in list(results):
        if col != 'sequence' and col != 'error' and col != 'ID':
            results.loc['mean', col] = results[col].mean()
    lowest = min(results.loc['mean'])
    mean = list(results.loc['mean'])

    return lowest, results.columns[(results.loc['mean'] == lowest)], mean, results