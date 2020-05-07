possible_items[obj] = (np.sqrt(
    (new_start_coords[coord_index[0] - new_coords[obj][0]) ** 2 * weight_x +
    (new_start_coords[coord_index[1] - new_coords[obj][1]) ** 2 * weight_y +
    (new_start_coords[coord_index[2] - new_coords[obj][2]) ** 2 * weight_z)
                       ** k[obj] * c[obj])