def get_median_edit_distance(objects, coordinates, start_coordinates, c, k, dimension, sequence, n=100):
    ''' Returns median edit distance (Damerau-Levenshtein) for n trials of sequence prediction.
    	Edit distance is defined as the error between predicted and given sequence 
    	normalized for sequence length ('abc' -> 'acb' = 0.33)

    	Input: list of objects, coordinates for objects, list of start coordinates, parameter values for c, k, and 
    	dimension (x, y, z, xy, xz, yz, xyz), sequence and number of trials (n)
    '''

    edit_list = []

    for x in range(0, n):
    	# get predicted sequence for list of objects
        result = ''.join(predict_sequence(objects, coordinates, start_coordinates, c, k, dimension))

        # get normalized error between predicted and given sequence
        dl = 1 - damerauLevenshtein(sequence, result)

        edit_list.append(dl)

    median = np.median(edit_list)
    return median