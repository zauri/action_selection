import random
from collection import Counter
from scipy.spatial.distance import euclidean


def predict_sequence(objects, coordinates, sequence,
                     start_coordinates, c, k, dimension=2):
    '''
    Generate a sequence of actions based on weighted cost.

    Parameters
    ----------
    objects : list
        Objects in episode.
    coordinates : dictionary
        Coordinates of objects.
    sequence : list
        List of actions/objects in sequence.
    start_coordinates : list
        List of coordinates where subject is standing before each action.
    c : dictionary
        Parameter values for containment for all objects.
    k : dictionary
        Parameter values for relational dependencies for all objects.
    dimension : list [int, str], optional
        Dimension in which to consider distances. The default is [3, ].

    Returns
    -------
    predicted_sequence : list
        Model-generated sequence of actions (objects to interact with).

    '''

    # TODO:
    # fix input parameters
    # check if sequence is human-readable version
    # remove distances dict dependency

    i = 0
    generated_sequence = []
    possible_items = dict.fromkeys(objects, 0)  # generate dict from obj list
    item_count = Counter(objects)

    coord_index = 0

    new_coords, new_start_coords = filter_for_dimension(coordinates,
                                                        start_coordinates,
                                                        dimension)

    while i < len(sequence) - 1:
        for obj in possible_items.keys():
            try:
                position = tuple(new_start_coords[coord_index])
            except TypeError:
                position = str(new_start_coords[coord_index])

            distance = euclidean(position, new_coords[obj])

            possible_items[obj] = distance ** k[obj] * c[obj]

        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        # choose prediction randomly if multiple items have same cost
        minval = random.choice(minval)

        prediction = minval
        generated_sequence.append(prediction)

        if item_count[sequence[i]] > 1:
            item_count[sequence[i]] = item_count[sequence[i]] - 1
        else:
            del possible_items[sequence[i]]

        coord_index += 1
        i += 1

    return generated_sequence


def filter_for_dimension(coordinates, start_coordinates, dimension=2):
    '''
    Filter coordinates and start coordinates for given dimension
    (e.g., xyz -> xy).

    Parameters
    ----------
    dimension : int, default: 2
        Dimension for which to adapt coordinates
        (default before filtering: 3D).
    coordinates : dictionary
        Coordinates of objects in 3D.
    start_coordinates : list
        List of start coordinates where subject is standing before next
        picking_up action in 3D.

    Returns
    -------
    new_coords : dictionary
        Dictionary with filtered coordinates.
    new_start_coords : list
        List with filtered start coordinates.

    '''

    new_coords = {}
    new_start_coords = []

    new_coords = {key: value[:-1] for key, value in coordinates.items()}
    new_start_coords = [x[:-1] for x in start_coordinates]

    return new_coords, new_start_coords
