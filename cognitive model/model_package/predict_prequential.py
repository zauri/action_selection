def predict_sequence(distances_dict, ID, objects, coordinates, start_coordinates, sequence, 
                                 c, k, dimension=[3, ]):
    '''
    Predict sequence of actions based on weighted cost.
    
    Parameters
    ----------
    distances_dict : dictionary
        Dictionary containing distances between objects in all dimensions.
    ID : str
        Identifier for episode.
    objects : list
        Objects in episode.
    coordinates : dictionary
        Coordinates of objects.
    start_coordinates : list
        List of coordinates where subject is standing before each picking-up action.
    sequence : str
        Observed sequence of objects in episode.
    c : dictionary
        Parameter values for containment for all objects.
    k : dictionary
        Parameter values for relational dependencies for all objects.
    dimension : list [int, str], optional
        Dimension in which to consider distances. The default is [3, ].

    Returns
    -------
    errors : list
        List of error values for observed vs predicted sequence.

    '''
    
    #TODO:
    #fix input parameters
    #check if sequence is human-readable version
    #remove error calculation
    #remove distances dict dependency
    #change output to sequence
    
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
            except TypeError:
                position = str(new_start_coords[coord_index])
            
            possible_items[obj] = distances_dict[dimension[1]][ID][position][obj] ** k[obj] * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        
        prediction = minval
        observed = sequence[i]
        
        if prediction == observed:
            error = 0
        else:
            error = 1
        
        errors.append(error)
        
        if item_count[sequence[i]] > 1:
            item_count[sequence[i]] = item_count[sequence[i]] - 1
        else:
            del possible_items[sequence[i]]
        
        coord_index += 1
        i += 1
    
    return errors
