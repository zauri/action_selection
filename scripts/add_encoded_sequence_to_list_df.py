#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 13:58:30 2022

@author: Petra Wenzl
"""

import argparse
import ast
import pandas as pd
from datetime import datetime


with open('../opportunistic_planning/documentation/legends/item_legend_neural_nets.txt') as legend:
    legend_dict = legend.read()
    item_legend = eval(legend_dict)


def encode_sequences(df, item_legend):
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
    
    
    for row in range(0, len(df)):
        items = [elem for elem in df.at[row, 'sequence'].split(',')]
        
        encoded_items = [item[:-1] if item[-1] == '2' else item for item in items]
        
        encoded_items = ['food' if item in food_items\
                         else 'seasoning' if item in seasoning\
                         else 'beverage' if item in beverages\
                         else 'utensil' if item in kitchen_utensils\
                         else 'container' if item in containers\
                         else 'cookware' if item in cookware\
                         else item for item in encoded_items]
        
        encoded_items = [item_legend[item] for item in encoded_items]
        encoded_items = ''.join(encoded_items)
            
        df.at[row, 'encoded_sequence'] = encoded_items
        
    return df


def save_to_csv(df):
    date = datetime.today().strftime('%Y-%m-%d')
    filename = 'data/task_environments_' + str(date) + '_encoded_sequences.csv'
    
    df.to_csv(filename, header=True, index=True)
    
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', help='input csv file \
                        to process')
                        
    parsed_arguments = parser.parse_args()
    
    df = parsed_arguments.filename
    df = pd.read_csv(df, header=0)
    df = encode_sequences(df, item_legend)
    
    save_to_csv(df)
    