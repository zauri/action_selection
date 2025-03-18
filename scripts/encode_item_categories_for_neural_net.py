#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 07:21:06 2022

@author: Petra Wenzl
"""

import argparse
from datetime import datetime
import pandas as pd


def replace_category(df, row, old_category, new_category):
    new_category_containment = str(new_category + '.containment')
    new_category_foodk = str(new_category + '.food_k')
    new_category_midk = str(new_category + '.mid_k')
    new_category_strongk = str(new_category + '.strong_k')
    new_category_alreadyseen = str(new_category + '.already_seen')
    new_category_x = str('coordinates_' + new_category + '.x')
    new_category_y = str('coordinates_' + new_category + '.y')
    new_category_z = str('coordinates_' + new_category + '.z')
    
    old_category_containment = str(old_category + '.containment')
    old_category_foodk = str(old_category + '.food_k')
    old_category_midk = str(old_category + '.mid_k')
    old_category_strongk = str(old_category + '.strong_k')
    old_category_alreadyseen = str(old_category + '.already_seen')
    old_category_x = str('coordinates_' + old_category + '.x')
    old_category_y = str('coordinates_' + old_category + '.y')
    old_category_z = str('coordinates_' + old_category + '.z')
    
    if not new_category_alreadyseen in df.columns:
        df.rename(columns={old_category_containment: new_category_containment,
                           old_category_foodk: new_category_foodk,
                           old_category_midk: new_category_midk,
                           old_category_strongk: new_category_strongk,
                           old_category_alreadyseen: new_category_alreadyseen,
                           old_category_x: new_category_x,
                           old_category_y: new_category_y,
                           old_category_z: new_category_z},
                           inplace=True)
    else:
        pass
    
    return df


def encode_categories(df, item_legend):
    df_new = df.copy()
    
    for row in range(0, len(df)):
        # input item: encode item
        if str(df.at[row, 'input']) != '<start>':
            item = df.at[row, 'input']
            df_new.at[row, 'input'] = item_legend[item]
        
        # target item: encode item + update spatial/parameter info to new category
        if str(df.at[row, 'target']) != '<start>':
            item = df.at[row, 'target']
            replace_category(df_new, row, item, item_legend[item])
            df_new.at[row, 'target'] = item_legend[item]
        
    
    return df_new


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', help='input csv file \
                        to process')
                        
    parsed_arguments = parser.parse_args()
    
    df = parsed_arguments.filename
    
    df = pd.read_csv(df, header=0)
    
    with open('../opportunistic_planning/documentation/legends/item_legend_neural_nets.txt') as legend:
        legend_dict = legend.read()
        item_legend = eval(legend_dict)

    df_new = encode_categories(df, item_legend)
    
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'data/single_step_df_ints_' + str(date) + '_encoded.csv'
    
    df_new.to_csv(filename, index=False, header=True)