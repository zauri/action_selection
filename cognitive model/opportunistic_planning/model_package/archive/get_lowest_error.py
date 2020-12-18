import pandas as pd

def get_lowest_error(results):
    ''' Returns lowest error in dataframe, index of lowest error, mean of lowest error col and 
    the updated dataframe.

    Input: Dataframe of results
    Output: lowest mean error, col where mean error is lowest, lowest median error, mean error, result dataframe
    '''

    for col in list(results):
        if col != 'sequence' and col != 'error' and col != 'ID':
            results.loc['mean', col] = results[col].mean()
            results.loc['median', col] = results[col].median()
    lowest = min(results.loc['mean'])
    lowest_median = min(results.loc['median'])
    mean = list(results.loc['mean'])

    return lowest, results.columns[(results.loc['mean'] == lowest)], lowest_median, mean, results
