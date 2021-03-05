import numpy as np
import random
from fastDamerauLevenshtein import damerauLevenshtein
from collections import Counter

def filter_for_dimension(dimension, coordinates, start_coordinates):
    ''' Filter coordinates and start coordinates for given dimension (e.g., xyz -> xy).
        Input: Dimension, coordinates dictionary, list of start coordinates
        Output: Filtered coordinates dictionary, filtered list of start coordinates
    '''
    
    new_coords =  {}
    new_start_coords = []
    
    if dimension[0] == 3:  # no changes if 3D
        new_coords = coordinates
        new_start_coords = start_coordinates

    elif dimension[0] == 2:  # 2D: remove obsolete coordinate
        if dimension[1] == 'xy':
            new_coords = {key: value[:-1] for key, value in coordinates.items()}
            new_start_coords = [x[:-1] for x in start_coordinates]

        elif dimension[1] == 'xz':
            new_start_coords = [[x[0], x[-1]] for x in start_coordinates]

            for key, value in coordinates.items():
                new_value = (value[0], value[-1])
                new_coords[key] = new_value

        elif dimension[1] == 'yz':
            new_coords = {key: value[1:] for key, value in coordinates.items()}
            new_start_coords = [x[1:] for x in start_coordinates]

    elif dimension[0] == 1:  # 1D: choose appropriate coordinate
        if dimension[1] == 'x':
            new_coords = {key: value[0] for key, value in coordinates.items()}
            new_start_coords = [x[0] for x in start_coordinates]

        elif dimension[1] == 'y':
            new_coords = {key: value[1] for key, value in coordinates.items()}
            new_start_coords = [x[1] for x in start_coordinates]

        elif dimension[1] == 'z':
            new_coords = {key: value[2] for key, value in coordinates.items()}
            new_start_coords = [x[2] for x in start_coordinates]
            
    return new_coords, new_start_coords


def predict_editdist(distances_dict, ID, objects, coordinates, start_coordinates, sequence,
                     c, k, dimension=[3, ]):
    ''' Predict sequence based on spatial properties of objects and environment.
        Input: Objects, object coordinates, start coordinates, c, k, dimension
        Output: Sequence of objects as str
    '''
    
    prediction = []
    possible_items = dict.fromkeys(objects, 0)  # generate dict from object list
    coord_index = 0
    
    new_coords, new_start_coords = filter_for_dimension(dimension, coordinates, start_coordinates)

    while bool(possible_items) == True:  # while dict not empty
        for obj in possible_items.keys():            
            try:
                position = tuple(new_start_coords[coord_index])
            except:
                position = str(new_start_coords[coord_index])
            
            possible_items[obj] = distances_dict[dimension[1]][ID][position][obj] ** k[obj] * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        prediction.append(minval)
        del possible_items[minval]
        coord_index += 1

    return prediction


def predict_prequential(distances_dict, ID, objects, coordinates, start_coordinates, sequence, 
                                 c, k, dimension=[3, ]):
    ''' Predict sequence based on prequential method (predict one step, compare with observed behavior,
        error measure: 0 if predicted == observed, 1 if predicted != observed).
        Input: Objects, object coordinates, start coordinates, c, k, dimension
        Output: Sequence of predicted objects as str
    '''
    
    i = 0
    errors = []
    possible_items = dict.fromkeys(objects, 0)  # generate dict from object list
    item_count = Counter(objects)
    
    coord_index = 0
    
    new_coords, new_start_coords = filter_for_dimension(dimension, coordinates, start_coordinates)

    while i < len(sequence) - 1:
        
        for obj in possible_items.keys():            
            try:
                position = tuple(new_start_coords[coord_index])
            except:
                position = str(new_start_coords[coord_index])
            
            possible_items[obj] = distances_dict[dimension[1]][ID][position][obj] ** k[obj] * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        
        prediction = minval
        observed = sequence[i]
        error = 1 - damerauLevenshtein(prediction, observed)
        
        errors.append(error)
        
        if item_count[sequence[i]] > 1:
            item_count[sequence[i]] = item_count[sequence[i]] - 1
        else:
            del possible_items[sequence[i]]
    
        
        coord_index += 1
        i += 1
    
    return errors


def get_median_error(error_function, row, ID, objects, coordinates, start_coordinates, c, k, dimension, sequence, 
                             distances_dict, n=1):

    error_list = []

    for x in range(0, n):
        if error_function == 'editdist':
        	# get predicted sequence for list of objects
            result = ''.join(predict_editdist(distances_dict, ID, objects, coordinates, 
                                          start_coordinates, sequence, c, k, dimension))

            # get normalized error between predicted and given sequence
            dl = 1 - damerauLevenshtein(sequence, result)

            error_list.append(dl)
            
        elif error_function == 'prequential':
            errors = predict_prequential(distances_dict, ID, objects, coordinates,
                                         start_coordinates, sequence, c, k, dimension)
            summed = sum(errors)
            error_list.append(summed)
                        
    median = np.nanmedian(error_list)
    return median

