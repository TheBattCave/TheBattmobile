import csv
import os
from os import listdir
import datetime
from datetime import datetime
import pandas as pd
import pathlib

def find_directory():
    '''
    Assuming your python file is in the directory containing KCM data files, returns a path to that directory with an additional
    forward slash for future concatenation processes.
    '''
    path = pathlib.Path().absolute()
    directory = str(path) + '/'
    return directory
    
    
def sort_bus_by_date(directory, bus_num):
    ''' input bus_num as string with number of bus desired'''
    
    # find directory of bus from sorted files
    bus_directory = directory + 'Cleaned buses/' + bus_num
    
    #make list of all files in bus folder
    csv_list = []
    for file in listdir(bus_directory):
        if file.endswith('.csv'):
            csv_list.append(file)
    
    # make a list of dates and initialize final columns for dataframe
    list_of_dates = []
    substring = 'Data retrieved'
    cols = ['Filename', 'DateRetrieved']

    for filename in csv_list:
        with open(bus_directory + filename) as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    for element in row:
                        if substring in element:
                            #print(filename, '|', element)
                            list_of_dates.append(element)
                except:
                    pass #some files have no data
    # pull out the 'Date Retrieved' and @ symbol from the date column
    for i in range(len(list_of_dates)):
        date = list_of_dates[i]
        list_of_dates[i] = date[16:].replace('@', '')
    
    # make the dataframe of filenames and dates
    list_of_tuples = list(zip(csv_list, list_of_dates))
    files_dates = pd.DataFrame(list_of_tuples, columns = cols)
    
    #sort by date
    files_dates['DateRetrieved'] = pd.to_datetime(files_dates.DateRetrieved)
    files_dates.sort_values('DateRetrieved', inplace=True)
    files_dates.reset_index(drop = True, inplace=True)
    
    return files_dates
    
def build_bus_df(directory, bus_num, keyword):
    bus_dates = sort_bus_by_date(directory, bus_num)
    if keyword == 'Current':
        row_list = list(range(19)) + list(range(20,960))
        index_range = list(range(0,18)) + list(range(19,960))
    elif keyword == 'Voltage':
        row_list = list(range(23)) + list(range(24,960))
        index_range = list(range(0,22)) + list(range(23,960))
    elif keyword == 'Power':
        row_list = list(range(27)) + list(range(28,960))
        index_range = list(range(0,26)) + list(range(27,960))
    else:
        print("Keyword entered in error. Please select from 'Current', 'Voltage', or 'Power'.")
        
    bus_parameter = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + 'Cleaned buses/' + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list) 
        bus_parameter = bus_parameter.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    bus_parameter.columns = df_index.columns

    bus_parameter = bus_parameter.loc[:, ~bus_parameter.columns.str.contains('^Unnamed')]
    bus_parameter.reset_index(drop = True, inplace=True)

    return bus_parameter
    
    
def build_module_df(directory, bus_num, module_num):
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47)* (module_num-1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51,960))
    
    module_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + 'Cleaned buses/' + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list) 
        module_df = module_df.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    module_df.columns = df_index.columns

    module_df = module_df.loc[:, ~module_df.columns.str.contains('^Unnamed')]
    module_df.reset_index(drop = True, inplace=True)

    return module_df


def build_module_df(directory, bus_num, module_num):
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47)* (module_num-1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51,960))
    
    module_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + 'Cleaned buses/' + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list) 
        module_df = module_df.append(tmp)
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    module_df.columns = df_index.columns

    module_df = module_df.loc[:, ~module_df.columns.str.contains('^Unnamed')]
    module_df.reset_index(drop = True, inplace=True)

    return module_df
    
    
def build_module_average_df(directory, bus_num, module_num):
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 51 + (11+47)* (module_num-1)
    end_row = start_row + 12
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(50)) + list(range(51,960))
    
    module_average_df = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + 'Cleaned buses/' + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        tmp = tmp.dropna(axis=1)
        tmp = tmp.drop(0, axis=1)
        tmp_ave = tmp.mean()
        module_average_df = module_average_df.append(tmp_ave, ignore_index = True)
    
    df_index = pd.read_csv(file_dir, header=0, skiprows = index_range)
    df_index = df_index.loc[:, ~df_index.columns.str.contains('^Unnamed')]
    module_average_df.columns = df_index.columns

    
    module_average_df.reset_index(drop = True, inplace=True)
    module_average_df_final = pd.concat([module_average_df, bus_dates['DateRetrieved'].astype(str)], axis=1)
    module_average_df_final = module_average_df_final.set_index('DateRetrieved')

    return module_average_df_final
    
    
    
