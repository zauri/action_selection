#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:39:03 2021

@author: Petra Wenzl
"""

import argparse
import os
import pandas as pd


def read_csv(filename):
    df = pd.read_csv(filename, header=0, index_col=False)
    
    return df


def sort_timestamps(dataframe):
    df_new = pd.DataFrame()
    
    for video_id in dataframe['video_id'].unique():
        id_df = dataframe.loc[dataframe['video_id'] == video_id]
        id_df.sort_values('start_timestamp', inplace=True)
        
        df_new.append(id_df)
    
    return df_new


def save_to_file(dataframe, filename):
    dataframe.to_csv(index=False, path_or_buf=filename + '_fixed_timestamps.csv')
    print('File creation succesful.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', help='Input csv file')
    parsed_arguments = parser.parse_args()
    
    inputfile = parsed_arguments.filename
    file_name = os.path.splitext(inputfile)[0]
    
    df = read_csv(inputfile)
    sorted_df = sort_timestamps(df)
    save_to_file(df, file_name)