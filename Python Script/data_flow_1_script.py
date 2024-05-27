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
    
    # data['volt'] = data['volt'].astype('float64')
    data[['volt', 'rotate', 'pressure', 'vibration']] = data[['volt', 'rotate', 'pressure', 'vibration']].astype('float64')
    data[['comp', 'failure', 'errorID', 'model', 'age', 'machineID']] = data[['comp', 'failure', 'errorID', 'model', 'age', 'machineID']].astype(str)
    data['datetime'] = data['datetime'].apply(lambda x: pd.Timestamp(x))
    
    # data1 = data.copy()
    # data1[['comp', 'failure', 'errorID']] = data1[['comp', 'failure', 'errorID']].astype(str)
    # data1[['volt', 'rotate', 'pressure', 'vibration']] = data1[['volt', 'rotate', 'pressure', 'vibration']].astype('float64')
    
    temp = []
    fields = ['volt', 'rotate', 'pressure', 'vibration']
    for col in fields:
        temp.append(pd.pivot_table(data,
                                   index='datetime',
                                   columns='machineID',
                                   values=col).resample('3H', closed='left', label='right').mean().unstack())
    telemetry_mean_3h = pd.concat(temp, axis=1)
    telemetry_mean_3h.columns = [i + 'mean_3h' for i in fields]
    telemetry_mean_3h.reset_index(inplace=True)
    
    temp = []
    fields = ['volt', 'rotate', 'pressure', 'vibration']
    for col in fields:
        temp.append(pd.pivot_table(data,
                                   index='datetime',
                                   columns='machineID',
                                   values=col).resample('3H', closed='left', label='right').std().unstack())
    telemetry_std_3h = pd.concat(temp, axis=1)
    telemetry_std_3h.columns = [i + 'std_3h' for i in fields]
    telemetry_std_3h.reset_index(inplace=True)
    
    temp = []
    fields = ['volt', 'rotate', 'pressure', 'vibration']
    for col in fields:
        temp.append(pd.pivot_table(data,
                                   index='datetime',
                                   columns='machineID',
                                   values=col).rolling(24).mean().resample('3H', closed='left', label='right').first().unstack())
    telemetry_mean_24h = pd.concat(temp, axis=1)
    telemetry_mean_24h.columns = [i + 'mean_24h' for i in fields]
    telemetry_mean_24h.reset_index(inplace=True)
    
    temp = []
    fields = ['volt', 'rotate', 'pressure', 'vibration']
    for col in fields:
        temp.append(pd.pivot_table(data,
                                   index='datetime',
                                   columns='machineID',
                                   values=col).rolling(24).std().resample('3H', closed='left', label='right').first().unstack())
    telemetry_std_24h = pd.concat(temp, axis=1)
    telemetry_std_24h.columns = [i + 'std_24h' for i in fields]
    telemetry_std_24h.reset_index(inplace=True)
    
    telemetry_feat = pd.concat([telemetry_mean_3h,
                            telemetry_std_3h.iloc[:, 2:6],
                            telemetry_mean_24h.iloc[:, 2:6],
                            telemetry_std_24h.iloc[:, 2:6]], axis=1).dropna()
    

    telemetry_feat = pd.merge(telemetry_feat, data, on = ['datetime', 'machineID'], how = 'inner')
    # telemetry_feat['age'] = telemetry_feat['age'].astype('int64')
    # telemetry_feat[['comp', 'failure', 'errorID']] = telemetry_feat[['comp', 'failure', 'errorID']].astype(str)
    telemetry_feat['age'] = telemetry_feat['age'].astype('int')
    telemetry_feat = pd.get_dummies(telemetry_feat.set_index(['datetime', 'machineID', 'model'])).reset_index()
    
    dty = telemetry_feat.dtypes.reset_index()
    
    for col in range(len(dty)):
        if dty[0][col] == 'float64':
            telemetry_feat[dty['index'][col]] = telemetry_feat[dty['index'][col]].apply(lambda x: Decimal(x))
            
    
    for i in ['comp_comp1', 'comp_comp2', 'comp_comp3', 'comp_comp4', 'failure_comp1', 'failure_comp2', 'failure_comp3', 'failure_comp4', 'errorID_error1', 'errorID_error2', 'errorID_error3', 'errorID_error4', 'errorID_error5']:
        if i not in telemetry_feat.columns:
            telemetry_feat[i] = False
    
    telemetry_feat['datetime'] = telemetry_feat['datetime'].apply(lambda x: pd.Timestamp(x))
    telemetry_feat[['age', 'machineID']] = telemetry_feat[['age', 'machineID']].astype('int').astype(str)
    
    telemetry_feat.drop(columns=['errorID_<NA>', 'comp_<NA>' , 'failure_<NA>'], inplace=True)
    telemetry_feat = pd.merge(telemetry_feat, data[['datetime', 'machineID', 'failure', 'comp', 'errorID']], on = ['datetime', 'machineID'], how = 'inner')
    telemetry_feat['Date'] = telemetry_feat['datetime'].dt.date
    
    return telemetry_feat[['voltmean_3h', 'rotatemean_3h', 'pressuremean_3h', 'vibrationmean_3h', 'voltstd_3h', 'rotatestd_3h', 'pressurestd_3h', 'vibrationstd_3h', 'voltmean_24h', 'rotatemean_24h', 'pressuremean_24h', 'vibrationmean_24h', 'voltstd_24h', 'rotatestd_24h', 'pressurestd_24h', 'vibrationstd_24h', 'volt', 'rotate', 'pressure', 'vibration', 'model', 'age', 'machineID', 'datetime', 'comp_comp1', 'comp_comp2', 'comp_comp3', 'comp_comp4', 'failure_comp1', 'failure_comp2', 'failure_comp3', 'failure_comp4', 'errorID_error1', 'errorID_error2', 'errorID_error3', 'errorID_error4', 'errorID_error5', 'failure', 'comp', 'errorID', 'Date']]


