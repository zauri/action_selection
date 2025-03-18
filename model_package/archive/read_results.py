import pandas as pd

def read_results(file):

	results = pd.read_csv(file, header=0)
	results = results.T
	results.reset_index(drop=True, inplace=True)

	header = results.iloc[0]
	results = results[1:]
	results.columns = header

	results.drop(results.tail(1).index, inplace=True)

	return results