#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def read_data(file):
    df = pd.read_csv(file, header=0)
    return df


def check_for_grid_location(df):
    grid_location_set = df[pd.notna(df['grid_location'])]
    return grid_location_set


def get_ids(df_by_grid_loc):
    IDs = df_by_grid_loc['video_id'].unique()
    return IDs


def get_annotated_episodes(df, IDs):
    annotated_episodes = df[df['video_id'].isin(IDs)]
    return annotated_episodes


def save_to_csv(df, filename):    
    df.to_csv(filename, header=True, index=True)
    
    
def filter_for_annotations(filepath, filename):
    df = read_data(filepath)
    grid_location_set = check_for_grid_location(df)
    IDs = get_ids(grid_location_set)
    annotated_episodes = get_annotated_episodes(df, IDs)
    
    filename = 'data/' + str(filename) + '_annotated_episodes.csv'
    save_to_csv(annotated_episodes, filename)    


if __name__ == '__main__':
    df = input('File path: ')
    filename = input('File name for filtered dataframe: ')
    
    filter_for_annotations(df, filename)