#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 08:16:43 2022

@author: Petra Wenzl
"""

import argparse
import pandas as pd

from datetime import datetime


def read_data(path_to_csv):
    df = pd.read_csv(path_to_csv, header=0, index_col=0)
    
    # select columns by type
    float_cols = df.select_dtypes(include=['float64']).columns
    str_cols = df.select_dtypes(include=['object']).columns
    
    # fill NAs
    df.loc[:, float_cols] = df.loc[:, float_cols].fillna(-99)
    
    # convert str to bool for true/false values
    mask = df.applymap(type) != bool
    bool_to_str = {True: 1, False: 0}
    df = df.where(mask, df.replace(bool_to_str))
    
    return df


def get_unique_values(df):
    sequence_list = [[elem for elem in row.split(',')] for row in df['sequence']]
    unique_items = set([item for sublist in sequence_list for item in sublist])

    return unique_items


def get_sequence_info(df, unique_items):
    list_dicts = []
    input_target_values = []
    list_already_seen = []

    for row in range(0, len(df)):
        items = [elem for elem in df.at[row, 'sequence'].split(',')]
    
        for position, item in enumerate(items):
            new_row_nr = row + position
            item_dict = {}
        
            # specific for position in sequence
            start_coords_col = 'start_coords' + str(position+1)
            item_dict['start_coords.x'] = df.loc[row, str(start_coords_col + '.x')]
            item_dict['start_coords.y'] = df.loc[row, str(start_coords_col + '.y')]
            item_dict['start_coords.z'] = df.loc[row, str(start_coords_col + '.z')]
            
            item_dict['row'] = row
        
            if position == 0:
                input_value = '<start>'
                target_value = item
                input_target_values.append([input_value, target_value])
                
                list_already_seen.append([])
            
            else:
                input_value = items[position-1]
                target_value = item
                input_target_values.append([input_value, target_value])

                list_already_seen.append(items[:position])
                
            list_dicts.append(item_dict)
    
    return list_dicts, input_target_values, list_already_seen


def get_row_info(df):
    dicts_row = {}
    
    for row in range(0, len(df)):
        row_dict = {}
        items = [elem for elem in df.at[row, 'sequence'].split(',')]
        
        for position, item in enumerate(items):
            item_coordinates_x = 'coordinates_' + item + '.x'
            item_coordinates_y = 'coordinates_' + item + '.y'
            item_coordinates_z = 'coordinates_' + item + '.z'
            row_dict[item_coordinates_x] = df.loc[row, item_coordinates_x]
            row_dict[item_coordinates_y] = df.loc[row, item_coordinates_y]
            row_dict[item_coordinates_z] = df.loc[row, item_coordinates_z]
            
            item_containment = item + '.containment'
            item_strong_k = item + '.strong_k'
            item_mid_k = item + '.mid_k'
            item_food_k = item + '.food_k'
            row_dict[item_containment] = df.loc[row, item_containment]
            row_dict[item_food_k] = df.loc[row, item_food_k]
            row_dict[item_strong_k] = df.loc[row, item_strong_k]
            row_dict[item_mid_k] = df.loc[row, item_mid_k]
        
            dicts_row[row] = row_dict
    
    return dicts_row


def create_singlestep_df(list_dicts, input_target_values, list_already_seen,
                         dicts_row, unique_items):
    single_step_df = pd.DataFrame(list_dicts)
    single_step_df.insert(loc=0, column='input', value=0)
    single_step_df.insert(loc=1, column='target', value=0)

    for row in range(0, len(input_target_values)):
        single_step_df.loc[row, 'input'] = input_target_values[row][0]
        single_step_df.loc[row, 'target'] = input_target_values[row][1]
        
    for row, elem in enumerate(list_already_seen):
        for item in unique_items:
            single_step_df.loc[row, str(item + '.already_seen')] = 0
            if item in elem:
                single_step_df.loc[row, str(item + '.already_seen')] = 1
                
    for row in range(0, len(single_step_df)):
        for key, values in dicts_row.items():
            if single_step_df.loc[row, 'row'] == key:
                for k,v in values.items():
                    single_step_df.loc[row, k] = v
                    
    single_step_df = single_step_df.drop('row', axis=1)
                    
    return single_step_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', help='input csv file \
                        to process')
                        
    parsed_arguments = parser.parse_args()
    
    df = parsed_arguments.filename
    
    df = read_data(df)
    unique_items = get_unique_values(df)

    list_dicts, input_target_values, list_already_seen = get_sequence_info(df, unique_items)
    dicts_row = get_row_info(df)

    single_step_df = create_singlestep_df(list_dicts, input_target_values, list_already_seen,
                                          dicts_row, unique_items)
    
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'data/single_step_df_ints_' + str(date) + '.csv'
    
    single_step_df.to_csv(filename, index=False, header=True)