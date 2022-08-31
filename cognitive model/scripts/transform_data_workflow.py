#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 11:48:32 2022

@author: Petra Wenzl
"""
import argparse
from datetime import datetime
import pandas as pd
import transform_data_list_format
import transform_data_to_single_step_df_list_format
import create_item_categories_for_neural_net
import encode_item_categories_for_neural_net


if __name__ == "__main__":
    # parse filename
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', help='input csv file \
                        to process')
                        
    parsed_arguments = parser.parse_args()
    
    df = parsed_arguments.filename
    
    # transform data
    df = transform_data_list_format.transform_data(df)
    transform_data_list_format.save_to_csv(df)
    print('Transform complete.')
    
    # transform to single step df
    unique_items = transform_data_to_single_step_df_list_format.get_unique_values(df)

    list_dicts, input_target_values, list_already_seen = transform_data_to_single_step_df_list_format.get_sequence_info(df, unique_items)
    dicts_row = transform_data_to_single_step_df_list_format.get_row_info(df)

    single_step_df = transform_data_to_single_step_df_list_format.create_singlestep_df(list_dicts, input_target_values, list_already_seen,
                                          dicts_row, unique_items)
    
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'data/single_step_df_ints_' + str(date) + '.csv'
    
    single_step_df.to_csv(filename, index=False, header=True)
    print('Single step df created.')
    
    # create item categories
    df, all_items = create_item_categories_for_neural_net.categorize_items(single_step_df)
    df = create_item_categories_for_neural_net.remove_empty_columns(df, all_items)
    
    filename = 'data/single_step_df_ints_' + str(date) + '_categorized.csv'
    df.to_csv(filename, index=False, header=True)
    print('Items categorized.')
    
    # encode item categories
    with open('../opportunistic_planning/documentation/legends/item_legend_neural_nets.txt') as legend:
        legend_dict = legend.read()
        item_legend = eval(legend_dict)

    df_new = encode_item_categories_for_neural_net.encode_categories(df, item_legend)
    filename = 'data/single_step_df_ints_' + str(date) + '_encoded.csv'
    
    df_new.to_csv(filename, index=False, header=True)
    print('Items encoded.')