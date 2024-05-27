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
    
    
    output_dict = {'Measure':[], 'Normality':[], 'Normality1':[], 'machineID':[]}
    
    
    telemetry = ['volt', 'pressure', 'rotate', 'vibration']
    variation = ['', 'mean_3h', 'mean_24h']
    
    for k in data['machineID'].unique():
      for i in telemetry:
        for j in variation:
            z = data[data['machineID'] == k].sort_values('datetime')
            z[i+j] = z[i+j].astype(float)
            q1 = z[i+j].quantile(0.25)
            q3 = z[i+j].quantile(0.75)
            
            iqr = q3 - q1
            
            ul = q3 + 1.5 * iqr
            ll = q1 - 1.5 * iqr
            
            output_dict['Measure'].append(i+j)
            output_dict['machineID'].append(k)
            x = z[i+j].tolist()[-1] 
            if x < ll or x > ul:
                output_dict['Normality'].append(1)
                output_dict['Normality1'].append('Abnormal')
            else:
                output_dict['Normality'].append(0)
                output_dict['Normality1'].append('Normal')
    
    output_df = pd.DataFrame(output_dict)
    # output_df = output_df.set_index('Measure')
    
    
    return output_df[['Measure', 'Normality', 'Normality1', 'machineID']]


