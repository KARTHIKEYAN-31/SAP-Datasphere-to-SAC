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
    data[['machineID', 'errorID', 'comp', 'failure']] = data[['machineID', 'errorID', 'comp', 'failure']].astype(str)
    data[['voltmean_3h', 'rotatemean_3h',
              'pressuremean_3h', 'vibrationmean_3h', 'voltstd_3h', 'rotatestd_3h',
              'pressurestd_3h', 'vibrationstd_3h', 'voltmean_24h', 'rotatemean_24h',
              'pressuremean_24h', 'vibrationmean_24h', 'voltstd_24h', 'rotatestd_24h',
              'pressurestd_24h', 'vibrationstd_24h', 'volt', 'rotate', 'pressure',
              'vibration']] = data[['voltmean_3h', 'rotatemean_3h',
              'pressuremean_3h', 'vibrationmean_3h', 'voltstd_3h', 'rotatestd_3h',
              'pressurestd_3h', 'vibrationstd_3h', 'voltmean_24h', 'rotatemean_24h',
              'pressuremean_24h', 'vibrationmean_24h', 'voltstd_24h', 'rotatestd_24h',
              'pressurestd_24h', 'vibrationstd_24h', 'volt', 'rotate', 'pressure',
              'vibration']].astype(float)
    
    data.sort_values(by=['machineID', 'datetime'], inplace=True)

    stat_diff = pd.DataFrame()
    # fault_dict = {'machineID': [], 'Type': [], 'Fault': []}
    
    for k in data['machineID'].unique():
    #   print(k)
      for j in ['errorID', 'comp', 'failure']:
    
        pivot = pd.pivot_table(data[data['machineID'] == k].fillna('None1'), ['voltmean_3h', 'rotatemean_3h',
              'pressuremean_3h', 'vibrationmean_3h', 'voltstd_3h', 'rotatestd_3h',
              'pressurestd_3h', 'vibrationstd_3h', 'voltmean_24h', 'rotatemean_24h',
              'pressuremean_24h', 'vibrationmean_24h', 'voltstd_24h', 'rotatestd_24h',
              'pressurestd_24h', 'vibrationstd_24h', 'volt', 'rotate', 'pressure',
              'vibration'], index=j, aggfunc='mean').reset_index()
        pivot_x = pivot.copy()
        for i in pivot.columns:
          if i != j:
            pivot.loc[(pivot[i] > pivot[i][0]*1.03) | (pivot[i] < pivot[i][0]*0.97), i] = 1
            pivot.loc[pivot[i] > 1 , i] = 0
            pivot[i] = pivot[i].astype(int)
        pivot['machineID'] = k
        pivot['Type'] = j
        pivot = pivot.rename(columns={j: 'Fault'})
    
    
        pred = [0]
    
        for i in pivot['Fault'].to_list():
          if i != '<NA>':
            row = pivot[pivot['Fault'] == i].drop(['machineID', 'Type', 'Fault'], axis = 1)
            row = row.drop([t for t in row.columns if 'std' in t], axis = 1)
            row = row.drop(columns=row.columns[(row == 0).all()])
    
            n = len(row.columns)
            n1 = 0
    
            if len(row.columns) > 0:
              for t in row.columns:
                if abs(pivot_x[pivot_x[j] == i][t].to_list()[0] - data[data['machineID'] == k][t].to_list()[-1]) < abs(pivot_x[pivot_x[j] == '<NA>'][t].to_list()[0] - data[data['machineID'] == k][t].to_list()[-1]):
                  n1 += 1
                
    
              pred.append(n1/n)
            #   pred.append(g)
              # print(pred[-1])
            else:
              pred.append(0.5)
    
    
        pivot['pred'] = pred
    
    
        stat_diff = pd.concat([stat_diff, pivot], ignore_index=True)
    
    stat_diff['pred'] = stat_diff['pred'].apply(lambda x: Decimal(x))
    
    return stat_diff[['machineID', 'Type', 'Fault', 'volt', 'voltmean_3h', 'voltmean_24h',
 'voltstd_3h', 'voltstd_24h', 'pressure', 'pressuremean_3h', 'pressuremean_24h',
 'pressurestd_3h', 'pressurestd_24h', 'vibration', 'vibrationmean_3h',
 'vibrationmean_24h', 'vibrationstd_3h', 'vibrationstd_24h', 'rotate', 'rotatemean_3h',
 'rotatemean_24h', 'rotatestd_3h', 'rotatestd_24h', 'pred']]


