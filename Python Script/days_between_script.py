def transform(data):
    """
    This function body should contain all the desired transformations on incoming DataFrame. Permitted builtin functions
    as well as permitted NumPy and Pandas objects and functions are available inside this function.
    Permitted NumPy and Pandas objects and functions can be used with aliases 'np' and 'pd' respectively.
    This function executes in a sandbox mode. Please refer the documentation for permitted objects and functions. Using
    any restricted functions or objects would cause an internal exception and result in a pipeline failure.
    Any code outside this function body will not be executed and inclusion of such code is discouraged.
    :param data: Pandas DataFrame
    :return: Pandas DataFrame
    """
    #####################################################
    # Provide the function body for data transformation #
    #####################################################
    
    data['datetime'] = data['datetime'].apply(lambda x: pd.Timestamp(x))
    
    col_list = ['failure_comp', 'errorID_error', 'comp_comp']
    g = pd.DataFrame({'machineID':data['machineID'].unique()})
    for i in col_list:
        for j in range(5):
            col = i + str(j+1)
            if col in data.columns:
                y = data[['datetime', col, 'machineID']].copy()
                y = y.drop_duplicates()
                y = y.sort_values(['machineID', 'datetime'])
                y[col+'_diff'] = y[col]
                y.loc[y[col+'_diff'] < 1, col+'_diff'] = None
                y.loc[-y[col+'_diff'].isnull(), col+'_diff'] = y.loc[-y[col+'_diff'].isnull(), 'datetime']
                y.fillna(method='ffill', inplace=True)
                y[col+'_diff'] = y[col+'_diff'].apply(lambda x: pd.Timestamp(x))
                y[col+'_diff'] = y['datetime'] - y[col+'_diff']
                y[col+'_diff'] = y[col+'_diff'] / np.timedelta64(1, "D")
                y[col+'_diff'] = y[col+'_diff'].shift(1)
                y = y[['datetime', 'machineID', col+'_diff', col]].dropna()
                last = y.groupby(['machineID'], as_index=False)[col+'_diff'].last().rename(columns={col+'_diff': col+'_last'})
                y = y[(y[col] == 1) &(y[col+'_diff'] > 0)].groupby('machineID', as_index=False)[col+'_diff'].mean()
                y = pd.merge(y[['machineID', col+'_diff']], last, on=['machineID'], how='left')
                g = pd.merge(g, y, on=['machineID'], how='outer')
          
                dty = g.dtypes.reset_index()
            
                for col in range(len(dty)):
                    if dty[0][col] == 'float64':
                        g[dty['index'][col]] = g[dty['index'][col]].apply(lambda x: Decimal(x))
                
                sel_col = ['machineID', 'failure_comp1_diff', 'failure_comp1_last',
       'failure_comp2_diff', 'failure_comp2_last', 'failure_comp3_diff',
       'failure_comp3_last', 'failure_comp4_diff', 'failure_comp4_last',
       'errorID_error1_diff', 'errorID_error1_last', 'errorID_error2_diff',
       'errorID_error2_last', 'errorID_error3_diff', 'errorID_error3_last',
       'errorID_error4_diff', 'errorID_error4_last', 'errorID_error5_diff',
       'errorID_error5_last', 'comp_comp1_diff', 'comp_comp1_last',
       'comp_comp2_diff', 'comp_comp2_last', 'comp_comp3_diff',
       'comp_comp3_last', 'comp_comp4_diff', 'comp_comp4_last']
                
                # for col in sel_col:
                #     if col not in g.columns:
                #         g[col] = None
                
                
    
    return g[sel_col]


