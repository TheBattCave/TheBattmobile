import csv
import os
from os import listdir
import numpy as np
import pandas as pd
import re
import shutil
from .sort_bus_by_date import sort_bus_by_date

def compare_file_mods(directory):
    '''
    Returns a dictionary of bus numbers as keys and
    concatenated pandas dataframe comparing modules between each CSV file
    and its subsequent number. CSV files are
    ordered by date that data was retrieved.
    '''
    list_bus_nums = []
    bus_to_ordered_csvs = {}
    bus_to_modules = {}
    num_mods = 16
    mod_index = ['Module ' + str(i) for i in range(1, num_mods + 1)]
    keyword = 'Mfg Data (ASCII)'
    for file in listdir(directory):
        if file.startswith('bus'):
            list_bus_nums.append(file)
    for bus in list_bus_nums:
        df = sort_bus_by_date(directory, bus + '/')
        ordered_csv = df['Filename'].tolist()
        bus_to_ordered_csvs[bus] = ordered_csv
    for bus_key in bus_to_ordered_csvs:
        column_names = []
        ordered_csvs = bus_to_ordered_csvs[bus_key]
        # Grab the list of ordered CSV's associated with that bus folder
        file_count = len(ordered_csvs)
        if file_count > 1:
            # If there is more than one CSV file (thus comparable)
            i = 0
            list_of_comp_df = []
            while(i < file_count - 1):
                # For each csv file in that list of ordered CSV's,
                # while file is not the last file in the list
                og_modules = []
                comp_modules = []
                column_names.append(ordered_csvs[i]
                                    + ' vs '
                                    + ordered_csvs[i+1])
                # Create column names of file vs file
                with open(directory
                          + bus_key
                          + '/'
                          + ordered_csvs[i]) as file:
                    # Looking at the first file
                    reader = csv.reader(file)
                    for row in reader:
                        for element in row:
                            if keyword in element:
                                mod_num = re.sub(r'\W+',
                                                 '',
                                                 element[17:]).lower()
                                og_modules.append(mod_num)
                            else:
                                pass
                with open(directory
                          + bus_key
                          + '/'
                          + ordered_csvs[i + 1]) as file:
                    # Looking at the second file
                    reader = csv.reader(file)
                    for row in reader:
                        for element in row:
                            if keyword in element:
                                mod_num = re.sub(r'\W+',
                                                 '',
                                                 element[17:]).lower()
                                comp_modules.append(mod_num)
                            else:
                                pass
                og_modules.pop(0)  # Getting rid of first overall module number
                comp_modules.pop(0)
                df_1 = pd.DataFrame(og_modules,
                                    columns=[column_names[i]],
                                    index=mod_index)
                df_2 = pd.DataFrame(comp_modules,
                                    columns=[column_names[i]],
                                    index=mod_index)
                comp = df_1.eq(df_2)
                list_of_comp_df.append(comp)
                # Append dataframe to a list of the dataframes
                i += 1
            concat_comp = pd.concat(list_of_comp_df, axis=1)
            # Concatenate list of comparison dataframes
            bus_to_modules[bus_key] = concat_comp
            # style.applymap(color_false_red)
        else:  # If there is only one CSV file
            mod_comp = []
            for i in range(0, 16):
                mod_comp.append(True)
            df_3 = pd.DataFrame(mod_comp, columns=[bus_key], index=mod_index)
            bus_to_modules[bus_key] = df_3
    return bus_to_modules

def count_bus_file(directory):
    '''
    Counts the number of bus folders in a given directory.
    '''
    # directory = get_directory()
    list = []
    for file in listdir(directory):
        substring = 'bus_'
        fullstring = 'sort_bus_by_date'
        if fullstring in file:
            pass
        else:
            if substring in file:
                list.append(file)
    return len(list)

def filter_false_module(directory):
    '''
    Filters out bus folders that do not contain at least two CSV files and therefore cannot have a module swapped.
    '''
    file_list = []
    get_bus = compare_file_mods(directory)
    bus_file_num = count_bus_file(directory)
    for i in range(1, bus_file_num):
        num = 'bus_'+str(i)
        bus = get_bus[num]
        for i in range(len(bus.columns)):
            if len(bus.columns) < 2:
                pass
            else:
                file_list.append(num)
    False_list = np.unique(file_list)
    return False_list


def move_false_bus(directory):
    '''
    Moves bus folders coantaining two or more CSV files to a directory called Cleaned_Buses.
    '''
    False_list = filter_false_module(directory)
    source = directory
    destination = directory + 'Cleaned_Buses'
    if not os.path.exists(destination):
        os.makedirs(destination)
    else:
        pass
    for bus_num in False_list:
        bus_file = source + bus_num
        shutil.move(bus_file, destination)
