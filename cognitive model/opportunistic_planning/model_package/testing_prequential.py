import pandas as pd
import numpy as np
from opportunistic_planning import data, sequence
from imp import reload
reload(data)

df = pd.read_csv('../all_lowest_error/all_task_environments_2020-12-07.csv', header=0)
df = df[:30]

distances_dict = data.generate_distances_dict(df)

results_new = data.calculate_edit_distances_prequential(df, distances_dict=distances_dict, n=1)