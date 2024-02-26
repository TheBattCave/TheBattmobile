import csv
import os
import numpy as np
import pandas as pd
import pathlib
import re
import shutil
import zipfile
from os import listdir


def find_directory():
    '''
    Assuming your python file is in the directory containing KCM data files,
    returns a path to that directory with an additional
    forward slash for future concatenation processes.
    '''
    path = pathlib.Path().absolute()
    directory = str(path) + '/'
    return directory


def grab_csv(directory):
    '''
    Returns a list of all csv files in an existing directory.
    Ignoring the lone xlsx file for now, as reader fails to read this file.
    '''
    list_of_csv = []
    for filename in listdir(directory):
        if (filename.endswith('.csv')):  # or filename.endswith('.xlsx')):
            list_of_csv.append(filename)
        else:
            pass
    return list_of_csv


def group_files(directory):
    '''
    Finds serial numbers for all modules of a each file in a directory and
    groups CSV files with matching serials into
    individual bus directories.
    '''
    keyword = 'Mfg Data (ASCII)'
    count = 1
    list_of_csv = grab_csv(directory)
    moved_files = []
    for filename in list_of_csv:
        list_matches = []
        if filename in moved_files:
            pass
        else:
            module_list = []
            source = os.path.join(directory, filename)
            with open(directory + filename) as file_1:
                reader = csv.reader(file_1)
                for row in reader:
                    for element in row:
                        if keyword in element:
                            mod_num = re.sub(r'\W+', '', element[17:]).lower()
                            module_list.append(mod_num)
                        else:
                            pass
            if not module_list:
                pass
            else:
                module_list.pop(0)
            if len(module_list) >= 16:
                bus_folder = 'bus_' + str(count) + '/'
                if not os.path.exists(os.path.join(directory, bus_folder)):
                    os.makedirs(os.path.join(directory, bus_folder))
                else:
                    pass
                destination = os.path.join(directory, bus_folder + filename)
                moved_files.append(filename)
                shutil.move(source, destination)
                # Finish moving complete source file to new directory

                for otherfile in list_of_csv:
                    if otherfile in moved_files:
                        pass
                    else:
                        other_modules = []
                        with open(directory + otherfile) as file_2:
                            reader = csv.reader(file_2)
                            for row in reader:
                                for element in row:
                                    if keyword in element:
                                        mod_num = re.sub(r'\W+',
                                                         '',
                                                         element[17:]).lower()
                                        other_modules.append(mod_num)
                                    else:
                                        pass
                        if not other_modules:
                            pass
                        else:
                            other_modules.pop(0)
                        if(len(other_modules) >= 16):
                            if (any(module_num in module_list
                                    for module_num in other_modules)):
                                list_matches.append(otherfile)
                                moved_files.append(otherfile)
                            else:
                                pass
                        else:
                            pass
                for match in list_matches:
                    # Modified from before because
                    # generally not safe to modify list as we loop
                    source = directory + match
                    destination = os.path.join(directory, bus_folder + match)
                    shutil.move(source, destination)
                count += 1
            else:
                moved_files.append(filename)
                incomplete = os.path.join(directory + 'incomplete/')
                if not os.path.exists(incomplete):
                    os.makedirs(os.path.join(incomplete))
                destination = incomplete + filename
                shutil.move(source, destination)


def count_bus_file(directory):
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


def sort_bus_by_date(directory, bus_num):
    ''' input bus_num as string with number of bus desired'''

    # find directory of bus from sorted files
    bus_directory = directory + bus_num

    # make list of all files in bus folder
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
                            # print(filename, '|', element)
                            list_of_dates.append(element)
                except IndexError:
                    pass  # some files have no data
    # pull out the 'Date Retrieved' and @ symbol from the date column
    for i in range(len(list_of_dates)):
        date = list_of_dates[i]
        list_of_dates[i] = date[16:].replace('@', '')

    # make the dataframe of filenames and dates
    list_of_tuples = list(zip(csv_list, list_of_dates))
    files_dates = pd.DataFrame(list_of_tuples, columns=cols)

    # sort by date
    files_dates['DateRetrieved'] = pd.to_datetime(files_dates.DateRetrieved)
    files_dates.sort_values('DateRetrieved', inplace=True)
    files_dates.reset_index(drop=True, inplace=True)

    return files_dates


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


def filter_false_module(directory):
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


directory = find_directory() + 'Raw Data/'
unzip_directory = find_directory() + 'sorted_data/'
if os.path.exists(unzip_directory):
    filter_false_module(unzip_directory)
    move_false_bus(unzip_directory)
else:
    zip_filename = 'KCM-Raw-Data.zip'
    zip_directory = directory + zip_filename
    with zipfile.ZipFile(zip_directory, 'r') as zip_ref:
        zip_ref.extractall(unzip_directory)
    group_files(unzip_directory)
    filter_false_module(unzip_directory)
    move_false_bus(unzip_directory)
