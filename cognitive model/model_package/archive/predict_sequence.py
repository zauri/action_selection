from scipy.spatial import distance
import numpy as np
import pandas as pd
import random

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
            possible_items[obj] = ((np.linalg.norm(
                np.array(new_start_coords[coord_index]),
                np.array(new_coords[obj]))
                                   ) ** k[obj]) * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        prediction.append(minval)
        del possible_items[minval]
        coord_index += 1

    return prediction
