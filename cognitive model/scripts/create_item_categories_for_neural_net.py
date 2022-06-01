#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:06:39 2022

@author: Petra Wenzl
"""

import argparse
from datetime import datetime
import numpy as np
import pandas as pd


def categorize_items(df):
    food_items = ['apricots', 'avocado', 'bananas', 'beans', 'blueberries', 'bread',
             'broccoli', 'butter', 'carrot', 'carrots', 'cauliflower', 'cereal',
             'cheese', 'chilli', 'cucumber', 'eggs', 'fig', 'figs', 'flour', 'garlic',
             'ginger', 'grapes', 'kiwi', 'leek', 'mango', 'onion', 'orange', 'oranges',
             'pepper', 'pineapple', 'plum', 'pomegranate', 'potato', 'salad', 'tomato_plate',
             'yoghurt', 'jar', 'oil']

    seasoning = ['herbs', 'lemon_juice', 'lime', 'ketchup', 'salt', 'spice',
            'spice_shaker', 'sugar']

    beverages = ['beer', 'can', 'drink', 'milk', 'water']

    kitchen_utensils = ['colander', 'flat_grater', 'garlic_press', 'ladle', 'measuring_pitcher', 'peeler',
                   'spatula', 'squeezer', 'wire_whisk']

    containers = ['paper_bag', 'plastic_box', 'tupperware']

    cookware = ['pot', 'pan', 'lid']

    all_items = food_items + seasoning + beverages + kitchen_utensils + containers + cookware + ['plate2', 'pot2', 'bowl2']

    
    for row in range(0, len(df)):
    # fix for first_item-second_item pairs
        if '2' in df.at[row, 'input']:
            second_item = df.at[row, 'input']
            replace_category(df, row, second_item, second_item[:-1])
            df.at[row, 'input'] = second_item[:-1]
    
        if '2' in df.at[row, 'target']:
            second_item = df.at[row, 'target']
            replace_category(df, row, second_item, second_item[:-1])
            df.at[row, 'target'] = second_item[:-1]
    
        # food items
        if df.at[row, 'input'] in food_items:
            #    replace_category(df, row, df.at[row, 'input'], 'food')
                df.at[row, 'input'] = 'food'
        if df.at[row, 'target'] in food_items:
            replace_category(df, row, df.at[row, 'target'], 'food')
            df.at[row, 'target'] = 'food'
    
        # containers
        if df.at[row, 'input'] in containers:
        #    replace_category(df, row, df.at[row, 'input'], 'container')
            df.at[row, 'input'] = 'container'
        if df.at[row, 'target'] in containers:
            replace_category(df, row, df.at[row, 'target'], 'container')
            df.at[row, 'target'] = 'container'
    
        # kitchen utensils
        if df.at[row, 'input'] in kitchen_utensils:
        #    replace_category(df, row, df.at[row, 'input'], 'utensil')
            df.at[row, 'input'] = 'utensil'
        if df.at[row, 'target'] in kitchen_utensils:
            replace_category(df, row, df.at[row, 'target'], 'utensil')
            df.at[row, 'target'] = 'utensil'
    
        # beverages
        if df.at[row, 'input'] in beverages:
        #    replace_category(df, row, df.at[row, 'input'], 'drink')
            df.at[row, 'input'] = 'beverage'
        if df.at[row, 'target'] in beverages:
            replace_category(df, row, df.at[row, 'target'], 'beverage')
            df.at[row, 'target'] = 'beverage'
    
        # seasoning
        if df.at[row, 'input'] in seasoning:
        #    replace_category(df, row, df.at[row, 'input'], 'seasoning')
            df.at[row, 'input'] = 'seasoning'
        if df.at[row, 'target'] in seasoning:
            replace_category(df, row, df.at[row, 'target'], 'seasoning')
            df.at[row, 'target'] = 'seasoning'
    
        # cookware
        if df.at[row, 'input'] in cookware:
        #    replace_category(df, row, df.at[row, 'input'], 'cookware')
            df.at[row, 'input'] = 'cookware'
        if df.at[row, 'target'] in cookware:
            replace_category(df, row, df.at[row, 'target'], 'cookware')
            df.at[row, 'target'] = 'cookware'
            
    return df, all_items


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
    
    if not new_category_containment in df.columns:
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


def remove_empty_columns(df, all_items):
    for col in df.columns:
        for item in all_items:
            if item in col:
                df.drop(col, axis=1, inplace=True, errors='ignore')
    
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', help='input csv file \
                        to process')
                        
    parsed_arguments = parser.parse_args()
    
    df = parsed_arguments.filename
    
    df = pd.read_csv(df)
    
    df, all_items = categorize_items(df)
    
    df = remove_empty_columns(df, all_items)
    
    df = df.reindex(sorted(df.columns), axis=1)
    
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'data/single_step_df_ints_' + str(date) + '_categorized.csv'
    
    df.to_csv(filename, index=False, header=True)