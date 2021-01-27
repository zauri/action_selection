import pandas as pd
import numpy as np
from opportunistic_planning import data, sequence
#from imp import reload
#reload(data)

df = pd.read_csv('../all_lowest_error/all_task_environments_2021-01-26.csv', header=0)
#small_df = df.loc[df['ID'] == 'E01_01']
#small_df = small_df.reset_index(drop=True)
#df2 = df[:22]
#df2 = df2.reset_index(drop=True)

#df = df.reset_index(drop=True)

distances_dict = data.generate_distances_dict(df)
#distances_dict_small = data.generate_distances_dict(small_df)

results_new, results_sum = data.calculate_edit_distances_prequential(df, distances_dict=distances_dict, n=1)
#results_small = data.calculate_edit_distances_prequential(small_df, distances_dict_small, n=1)