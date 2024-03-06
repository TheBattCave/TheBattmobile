import pandas as pd
from os import listdir
from .sort_bus_by_date import sort_bus_by_date

def build_bus_df(directory, bus_num, keyword):
    '''
    Builds dataframes of the information at the top of CSVs representing data on overall bus battery performance.
    '''
    bus_dates = sort_bus_by_date(directory, bus_num)
    if keyword == 'Current':
        row_list = list(range(19)) + list(range(20, 960))
        index_range = list(range(0, 18)) + list(range(19, 960))
    elif keyword == 'Voltage':
        row_list = list(range(23)) + list(range(24, 960))
        index_range = list(range(0, 22)) + list(range(23, 960))
    elif keyword == 'Power':
        row_list = list(range(27)) + list(range(28, 960))
        index_range = list(range(0, 26)) + list(range(27, 960))
    else:
        print("Keyword entered in error."
              "Please select from 'Current', 'Voltage', or 'Power'.")
    bus_parameter = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        bus_parameter = bus_parameter.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    bus_parameter.columns = df_index.columns
    loc_parameter = bus_parameter.columns.str.contains('^Unnamed')
    bus_parameter = bus_parameter.loc[:, ~loc_parameter]
    bus_parameter.reset_index(drop=True, inplace=True)
    return bus_parameter


def build_module_df(directory, bus_num, module_num):
    '''
    Builds dataframes of the information for a module (1 through 16).
    '''
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47) * (module_num - 1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51, 960))
    module_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        module_df = module_df.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    module_df.columns = df_index.columns
    module_df = module_df.loc[:, ~module_df.columns.str.contains('^Unnamed')]
    module_df.reset_index(drop=True, inplace=True)
    return module_df


def build_module_average_df(directory, bus_num, module_num):
    '''
    Builds dataframes of the averaged data for a module (1 through 16).
    '''
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47) * (module_num-1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51, 960))
    module_average_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        tmp = tmp.dropna(axis=1)
        tmp = tmp.drop(0, axis=1)
        tmp_ave = tmp.mean()
        module_average_df = module_average_df.append(tmp_ave,
                                                     ignore_index=True)
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    df_index = df_index.loc[:, ~df_index.columns.str.contains('^Unnamed')]
    module_average_df.columns = df_index.columns
    module_average_df.reset_index(drop=True, inplace=True)
    string = 'DateRetrieved'
    module_average_df_final = pd.concat([module_average_df,
                                        bus_dates[string].astype(str)],
                                        axis=1)
    module_average_df_final = module_average_df_final.set_index(string)
    return module_average_df_final
