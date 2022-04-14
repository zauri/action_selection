#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:06:39 2022

@author: Petra Wenzl
"""

import argparse
import datetime
import numpy as np
import pandas as pd

food_items = ['apricots', 'avocado', 'bananas', 'beans', 'blueberries', 'bread',
             'broccoli', 'butter', 'carrot', 'carrots', 'cauliflower', 'cereal',
             'cheese', 'chilli', 'cucumber', 'egg', 'fig', 'figs', 'flour', 'garlic',
             'ginger', 'grapes', 'kiwi', 'leek', 'mango', 'onion', 'orange', 'oranges',
             'pepper', 'pineapple', 'plum', 'pomegranate', 'potato', 'salad', 'tomato_plate',
             'yoghurt', 'jar', 'oil']

seasoning = ['herbs', 'lemon_juice_container', 'lime', 'ketchup', 'salt', 'spice',
            'spice_shaker', 'sugar']

drink_items = ['beer', 'can', 'drink', 'milk', 'water']

kitchen_utensils = ['colander', 'flat_grater', 'garlic_press', 'ladle', 'measuring_pitcher', 'peeler',
                   'spatula', 'squeezer', 'wire_whisk']

containers = ['container', 'paper_bag', 'plastic_box', 'tupperware']

cookware = ['pot', 'pan', 'lid']

all_items = food_items + seasoning + drink_items + kitchen_utensils + containers + cookware + ['plate2', 'pot2', 'bowl2']


def replace_category(df, row, old_category, new_category):
    new_category_containment = str(new_category + '.containment')
    new_category_foodk = str(new_category + '.food_k')
    new_category_midk = str(new_category + '.mid_k')
    new_category_strongk = str(new_category + '.strong_k')
    new_category_alreadyseen = str(new_category + '.already_seen')
    new_category_x = str(new_category + '.x')
    new_category_y = str(new_category + '.y')
    new_category_z = str(new_category + '.z')
    
    old_category_containment = str(old_category + '.containment')
    old_category_foodk = str(old_category + '.food_k')
    old_category_midk = str(old_category + '.mid_k')
    old_category_strongk = str(old_category + '.strong_k')
    old_category_alreadyseen = str(old_category + '.already_seen')
    old_category_x = str('coordinates_' + old_category + '.x')
    old_category_y = str('coordinates_' + old_category + '.y')
    old_category_z = str('coordinates_' + old_category + '.z')
    
    df.at[row, new_category_containment] = df.at[row, old_category_containment]
    df.at[row, new_category_foodk] = df.at[row, old_category_foodk]
    df.at[row, new_category_midk] = df.at[row, old_category_midk]
    df.at[row, new_category_strongk] = df.at[row, old_category_strongk]
    df.at[row, new_category_x] = df.at[row, old_category_x]
    df.at[row, new_category_y] = df.at[row, old_category_y]
    df.at[row, new_category_z] = df.at[row, old_category_z]
    df.at[row, new_category_alreadyseen] = df.at[row, old_category_alreadyseen]
    
    df.at[row, old_category_containment] = np.nan
    df.at[row, old_category_foodk] = np.nan
    df.at[row, old_category_midk] = np.nan
    df.at[row, old_category_strongk] = np.nan
    df.at[row, old_category_x] = np.nan
    df.at[row, old_category_y] = np.nan
    df.at[row, old_category_z] = np.nan
    df.at[row, old_category_alreadyseen] = np.nan
    
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
        #if df.at[row, 'input'] in food_items:
            #    replace_category(df, row, df.at[row, 'input'], 'food')
            #    df.at[row, 'input'] = 'food'
        if df.at[row, 'target'] in food_items:
            replace_category(df, row, df.at[row, 'target'], 'food')
            df.at[row, 'target'] = 'food'
    
        # containers
        #if df.at[row, 'input'] in containers:
        #    replace_category(df, row, df.at[row, 'input'], 'container')
        #    df.at[row, 'input'] = 'container'
        if df.at[row, 'target'] in containers:
            replace_category(df, row, df.at[row, 'target'], 'container')
            df.at[row, 'target'] = 'container'
    
        # kitchen utensils
        #if df.at[row, 'input'] in kitchen_utensils:
        #    replace_category(df, row, df.at[row, 'input'], 'utensil')
        #    df.at[row, 'input'] = 'utensil'
        if df.at[row, 'target'] in kitchen_utensils:
            replace_category(df, row, df.at[row, 'target'], 'utensil')
            df.at[row, 'target'] = 'utensil'
    
        # drinks
        #if df.at[row, 'input'] in drink_items:
        #    replace_category(df, row, df.at[row, 'input'], 'drink')
        #    df.at[row, 'input'] = 'drink'
        if df.at[row, 'target'] in drink_items:
            replace_category(df, row, df.at[row, 'target'], 'drink')
            df.at[row, 'target'] = 'drink'
    
        # seasoning
        #if df.at[row, 'input'] in seasoning:
        #    replace_category(df, row, df.at[row, 'input'], 'seasoning')
        #    df.at[row, 'input'] = 'seasoning'
        if df.at[row, 'target'] in seasoning:
            replace_category(df, row, df.at[row, 'target'], 'seasoning')
            df.at[row, 'target'] = 'seasoning'
    
        # cookware
        #if df.at[row, 'input'] in cookware:
        #    replace_category(df, row, df.at[row, 'input'], 'cookware')
        #    df.at[row, 'input'] = 'cookware'
        if df.at[row, 'target'] in cookware:
            replace_category(df, row, df.at[row, 'target'], 'cookware')
            df.at[row, 'target'] = 'cookware'
    
    
    remove_empty_columns(df, all_items)
    
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'data/single_step_df_ints_' + str(date) + '_categorized.csv'
    
    df.to_csv(filename, index=False, header=True)