def get_lowest_error(results):
    ''' Returns lowest error in dataframe, index of lowest error, mean of lowest error col and 
    the updated dataframe.

    Input: Dataframe of results
    '''

    for col in list(results):
        if col != 'sequence' and col != 'error' and col != 'ID':
            results.loc['mean', col] = results[col].mean()
    lowest = min(results.loc['mean'])
    mean = list(results.loc['mean'])

    return lowest, results.columns[(results.loc['mean'] == lowest)], mean, results