import pandas as pd
import numpy as np
import random
import ast
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import distance
from pyxdameraulevenshtein import damerau_levenshtein_distance

def predict_sequence(objects, coordinates, start_coordinates, c, k, dimension=[3, ]):
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
            possible_items[obj] = ((distance.euclidean(
                new_start_coords[coord_index],
                new_coords[obj])
                                   ) ** k[obj]) * c[obj]
        # print(possible_items)
        minval = min(possible_items.values())
        minval = [k for k, v in possible_items.items() if v == minval]
        minval = random.choice(minval)  # choose prediction randomly if multiple items have same cost
        prediction.append(minval)
        del possible_items[minval]
        coord_index += 1

    return prediction


def get_average(objects, coordinates, start_coordinates, c, k, dimension, sequence):
    edit_list = []

    for x in range(0, 100):
        result = ''.join(predict_sequence(objects, coordinates, start_coordinates, c, k, dimension))
        dl = damerau_levenshtein_distance(sequence, result)
        edit_list.append(dl)

    avg = np.mean(edit_list)
    return avg


def get_avg_editdist(df):
    results = pd.DataFrame()
    dimensions = [[1, 'x'], [1, 'y'], [1, 'z'], [2, 'xy'], [2, 'xz'], [2, 'yz'], [3, 'xyz']]

    for row in range(0, len(df)):
        objects = list(df.at[row, 'objects'].split(','))
        strong_k = list(df.at[row, 'strong_k'].split(','))
        mid_k = list(df.at[row, 'mid_k'].split(','))
        coordinates = {key: ast.literal_eval(value) for key, value in
                       (elem.split(': ') for elem in df.at[row, 'coordinates'].split(';'))}
        start_coordinates = list(ast.literal_eval(df.at[row, 'start_coordinates']))
        sequence = str(df.at[row, 'sequence'])

        # for k in np.arange(0.0,1.0,0.1):
        for k in np.arange(0, 0.9, 0.1):
            k_strong = round(k, 2)
            k_mid = round(k + 0.1, 2)
            k1 = {obj: k_strong if obj in strong_k else k_mid if obj in mid_k else 1.0 for obj in objects}

            for c in np.arange(1.0, 2.0, 0.1):
                c = round(c, 1)
                c1 = {obj: c if obj in df.at[row, 'containment'] else 1.0 for obj in objects}

                for dim in dimensions:
                    # get average edit distance
                    edit_dist = get_average(objects, coordinates, start_coordinates, c1, k1, dim, sequence)
                    edit_dist = edit_dist / len(sequence)

                    # params = 'c: ' + str(c) + ', k: ' + str(k_strong) + ',' + str(k_mid) + ', dim: ' + str(dim[1])
                    params = 'c: ' + str(c) + '; k: ' + str(k_strong) + ',' + str(k_mid) + '; ' + str(dim[1])
                    results.at[row, params] = edit_dist

    return results

# TODO:
# range for diff between strong/mid k?
# range for c and k in general?

def get_lowest_error(results):
    for col in list(results):
        results.loc['mean', col] = results[col].mean()
    lowest = min(results.loc['mean'])
    mean = sorted(results.loc['mean'])

    return lowest, results.columns[(results.loc['mean'] == lowest)], mean, results

def create_plot(results_new, results_mean):
    c = [float(x[3:6]) for x in results_new.columns.tolist()]
    k = [float(x[11:14]) for x in results_new.columns.tolist()]
    dim = [x.strip() for x in results_new.columns.str.split(';').str[2]]
    error = results_mean.loc['mean'].tolist()
    cm = ['red', 'blue', 'green', 'magenta', 'cyan', 'orange', 'grey']
    dim_num = [0 if x == 'x' else 1 if x == 'y' else 2 if x == 'z' else 3 if x == 'xy' else 4 if x == 'xz' else 5 if x == 'yz' else 6
        for x in dim]

    cmap = matplotlib.colors.ListedColormap(cm)

    ticks = ['x', 'y', 'z', 'xy', 'xz', 'yz', 'xyz']
    norm = matplotlib.colors.BoundaryNorm(ticks, cmap.N)

    # create figure, 3d grid, set background to white
    fig2 = plt.figure(figsize=(12, 8))
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax2.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax2.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

    # create plot
    img = ax2.scatter(c, k, error, alpha=0.5, s=38, c=dim_num, cmap=cmap)

    # set labels
    ax2.set_ylabel('parameter k', fontsize=14, labelpad=7)
    ax2.set_xlabel('parameter c', fontsize=14, labelpad=7)
    ax2.set_zlabel('normalized edit distance', fontsize=14, labelpad=7)
    plt.title('Average edit distance', fontsize=16)

    # create colorbar
    cb = plt.colorbar(img, cax=fig2.add_axes([0.9, 0.3, 0.03, 0.4]))
    cb.ax.set_yticklabels(ticks)
    plt.show()


def main():
    df = pd.read_csv('all_task_environments.csv', header=0, skiprows=[1])
    results_new = get_avg_editdist(df)
    lowest, lowest_idx, list_mean, results_mean = get_lowest_error(results_new)
    print(lowest, lowest_idx)
    create_plot(results_new, results_mean)

main()