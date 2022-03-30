#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import pandas as pd
from datetime import datetime


def read_csv(filename):
    df = pd.read_csv(filename, header=0)
    
    return df


def split_sequences(df):
    for row in range(0, len(df)):
        #sequence = df.at[row, 'sequence']
        items = [elem for elem in df.at[row, 'sequence'].split(',')]
        
        for idx, item in enumerate(items):
            col_name = 'seq' + str(idx + 1)
            df.at[row, col_name] = item
            
    return df


def split_start_coordinates(df):
    for row in range(0, len(df)):
        start_coords = ast.literal_eval(df.at[row, 'start_coordinates'])
    
        for elem in range(0, len(start_coords)):
            coords = start_coords[elem]
        
            for i in range(0, len(coords)):
                if i == 0:
                    col_name_x = 'start_coords' + str(elem + 1) + '.x'
                    df.at[row, col_name_x] = coords[i]
                elif i == 1:
                    col_name_y = 'start_coords' + str(elem + 1) + '.y'
                    df.at[row, col_name_y] = coords[i]
                elif i == 2:
                    col_name_z = 'start_coords' + str(elem + 1) + '.z'
                    df.at[row, col_name_z] = coords[i]

    return df


def get_unique_characters(df):
    vocabulary = set()
    for row in range(0, len(df)):
        #sequence = df.at[row, 'sequence']
        sequence = [elem for elem in df.at[row, 'sequence'].split(',')]
        #for char in range(0, len(sequence)):
        for item in range(0,len(sequence)):
            vocabulary.add(sequence[item])
            
    return vocabulary


def split_parameter_info(df, vocabulary):
    for row in range(0, len(df)):

        for char in vocabulary:
            col_name_c = str(char) + '.containment'
            col_name_k_strong = str(char) + '.strong_k'
            col_name_k_mid = str(char) + '.mid_k'
            col_name_k_food = str(char) + '.food_k'
        
            if pd.notna(df.at[row, 'containment']) and char in df.at[row, 'containment']:
                df.at[row, col_name_c] = 'True'
            else:
                df.at[row, col_name_c] = 'False'
            
            if pd.notna(df.at[row, 'strong_k']) and char in df.at[row, 'strong_k']:
                df.at[row, col_name_k_strong] = 'True'
            else:
                df.at[row, col_name_k_strong] = 'False'
            
            if pd.notna(df.at[row, 'mid_k']) and char in df.at[row, 'mid_k']:
                df.at[row, col_name_k_mid] = 'True'
            else:
                df.at[row, col_name_k_mid] = 'False'
            
            if pd.notna(df.at[row, 'food_k']) and char in df.at[row, 'food_k']:
                df.at[row, col_name_k_food] = 'True'
            else:
                df.at[row, col_name_k_food] = 'False'
                
    return df


def split_coordinates(df):
    for row in range(0, len(df)):
        coordinates = {key: ast.literal_eval(value) for key, value in
                   (elem.split(': ') for elem in df.at[row, 'coordinates'].split(';'))}
    
        for item in coordinates:
            coords = coordinates[item]
        
            for i in range(0, len(coords)):
                if i == 0:
                    col_name_x = 'coordinates_' + str(item) + '.x'
                    df.at[row, col_name_x] = coords[i]
                elif i == 1:
                    col_name_y = 'coordinates_' + str(item) + '.y'
                    df.at[row, col_name_y] = coords[i]
                elif i == 2:
                    col_name_z = 'coordinates_' + str(item) + '.z'
                    df.at[row, col_name_z] = coords[i]
                    
    return df


def remove_obsolete_columns(df):
    to_drop = ['coordinates', 'ID', 'strong_k', 'mid_k', 'food_k', 'containment', 'start_coordinates']
    df.drop(to_drop, axis=1, inplace=True)
    
    return df


def transform_data(df):
    df = read_csv(df)
    vocabulary = get_unique_characters(df)
    
    df = split_sequences(df)
    df = split_start_coordinates(df)
    df = split_parameter_info(df, vocabulary)
    df = split_coordinates(df)
    df = remove_obsolete_columns(df)
    
    return df


def save_to_csv(df):
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'task_environments_' + str(date) + '_transformed.csv'
    
    df.to_csv(filename, header=True, index=True)
    
            
if __name__ == "__main__":
    df = input('Input file (csv): ')
    
    df = transform_data(df)
    save_to_csv(df)
    
            
            