import numpy as np
import random
from fastDamerauLevenshtein import damerauLevenshtein
#from data import generate_distances_dict

def filter_for_dimension(dimension, coordinates, start_coordinates):
    ''' Filters coordinates and start coordinates for given dimension (e.g., xyz -> xy).
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


def predict_sequence(distances_dict, ID, objects, coordinates, start_coordinates, c, k, dimension=[3, ]):
    ''' Predicts sequence based on required objects, object coordinates, start coordinates of subject,
        parameters (c+k) and dimensionality.
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
            
            # calculate euclidean distance between current location and items
            #possible_items[obj] = ((np.linalg.norm(
                                #np.array(new_start_coords[coord_index]) - np.array(new_coords[obj]))
                                #) ** k[obj]) * c[obj]
            possible_items[obj] = distances_dict[dimension[1]][ID][position][obj] ** k[obj] * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        prediction.append(minval)
        del possible_items[minval]
        coord_index += 1

    return prediction


def get_median_edit_distance(ID, objects, coordinates, start_coordinates, c, k, dimension, sequence, 
                             distances_dict, n=100):
    ''' Returns median edit distance (Damerau-Levenshtein) for n trials of sequence prediction.
    	Edit distance is defined as the error between predicted and given sequence 
    	normalized for sequence length ('abc' -> 'acb' = 0.33)

    	Input: list of objects, coordinates for objects, list of start coordinates, parameter values for c, k, and 
    	dimension (x, y, z, xy, xz, yz, xyz), sequence, dictionary with distances, and number of trials (n)
        Output: Median edit distance for n iterations
    '''

    edit_list = []

    for x in range(0, n):
    	# get predicted sequence for list of objects
        result = ''.join(predict_sequence(distances_dict, ID, objects, coordinates, 
                                          start_coordinates, c, k, dimension))

        # get normalized error between predicted and given sequence
        dl = 1 - damerauLevenshtein(sequence, result)

        edit_list.append(dl)

    median = np.median(edit_list)
    return median
