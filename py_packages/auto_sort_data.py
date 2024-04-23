import csv
import os
import numpy as np
import pandas as pd
import pathlib
import re
import shutil
import zipfile
from os import listdir
import sys

def find_directory():
    """
    Assuming your python file is in the directory containing KCM data files,
    returns a path to that directory with an additional
    forward slash for future concatenation processes.
    
    Returns:
    str: The absolute path of the current directory formatted for concatenation.
    """
    path = pathlib.Path().absolute()
    directory = str(path) + '/'
    return directory


def grab_csv(directory):
    """
    Returns a list of all csv files in an existing directory.
    Ignoring the lone xlsx file for now, as reader fails to read this file.
    
    Parameters:
    directory (str): The path to the directory to be scanned for '.csv' files.

    Returns:
    list: A list of filenames (str) that end with '.csv'.

    Note:
    The function is designed to ignore any '.xlsx' files present in the directory.
    """
    list_of_csv = []
    for filename in listdir(directory):
        if (filename.endswith('.csv')):  # or filename.endswith('.xlsx')):
            list_of_csv.append(filename)
        else:
            pass
    return list_of_csv


def group_files(directory):
    """
    Finds serial numbers for all modules of a each file in a directory and
    groups CSV files with matching serials into
    individual bus directories.

    Parameters:
    directory (str): The path to the directory containing the CSV files to be organized.

    Returns:
    None

    Side effects:
    - Creates 'bus' subdirectories for files with matching serial numbers.
    - Moves files without matching serial numbers to an 'incomplete' subdirectory.
    - Renames files to include the serial number as a prefix.

    Note:
    The function assumes that each file contains a list of serial numbers, and a file is considered
    complete if it has at least 16 serial numbers. The serial numbers are extracted from a specific
    keyword field in the file's content.
    """
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
                bus_folder = 'bus_' + mod_num + '/'
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
    """
    Count the number of files in a given directory that contain the substring 'bus_'
    but are not named 'sort_bus_by_date'.

    Parameters:
    directory (str): The path to the directory where files are located.

    Returns:
    int: The count of files that match the criteria.

    Note:
    This function does not recursively search through subdirectories.
    """
    #directory = get_directory()
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
    """
    Sort and return a DataFrame of CSV files by the date retrieved for a specific bus number.
    This function locates the directory corresponding to the provided bus number, identifies all CSV files within it,
    and extracts the 'Date Retrieved' information from each file. It then creates a DataFrame with filenames and their
    respective retrieval dates, and sorts this DataFrame in ascending order of the dates.

    Parameters:
    directory (str): The path to the parent directory containing subdirectories for each bus.
    bus_num (str): The bus number as a string, specifying the subdirectory to search within.

    Returns:
    pandas.DataFrame: A DataFrame with two columns, 'Filename' and 'DateRetrieved', sorted by 'DateRetrieved'.

    Note:
    The function assumes that the 'Date Retrieved' information is located after a specific substring within the file's  content.
    It also assumes that the date format is consistent across files and can be converted to datetime objects for sorting.
    """
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
    """
    Compare module serial numbers across CSV files within each 'bus' subdirectory.
    Returns a dictionary of bus numbers as keys and
    concatenated pandas dataframe comparing modules between each CSV file
    and its subsequent number. CSV files are
    ordered by date that data was retrieved.

    Parameters:
    directory (str): The path to the directory containing 'bus' subdirectories with CSV files.

    Returns:
    dict: A dictionary where each key is a 'bus' subdirectory name and each value is a DataFrame
          representing the comparison of module serial numbers between consecutive CSV files.

    Note:
    The function assumes that the module serial numbers are located after a specific keyword within the file's content.
    It also assumes that there are at least 16 module serial numbers in each file to be considered for comparison.
    If a 'bus' subdirectory contains only one CSV file, the function returns a DataFrame with all True values,
    indicating no comparison is possible.
    """
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
    """ 
    Uses the output from the 'compare_file_mods' function to check each 'bus' subdirectory within
    the specified directory. It identifies subdirectories where the comparison DataFrames have at least two columns,
    indicating that there are at least two CSV file comparisons. It then filters for those subdirectories that contain
    any false matches in the module serial numbers and returns a list of unique subdirectory names.

    Parameters:
    directory (str): The path to the directory containing 'bus' subdirectories with comparison DataFrames.

    Returns:
    numpy.ndarray: An array of unique 'bus' subdirectory names that have at least two CSV file comparisons
                   with false module matches.

    Note:
    The function assumes that the 'compare_file_mods' function is available and returns a dictionary where
    each key is a 'bus' subdirectory name and each value is a DataFrame representing the comparison of module
    serial numbers between consecutive CSV files.
    """
    file_list = []
    get_bus = compare_file_mods(directory)
    for folder_name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder_name)):
            match = re.match(r'bus_\w+', folder_name)
            if match:
                bus = get_bus.get(folder_name, None)
                if bus is not None and len(bus.columns) >= 2:
                    file_list.append(folder_name)
    return np.unique(file_list)


def move_false_bus(directory):
    """
    Move 'bus' subdirectories with false module matches to a 'vis_buses' subdirectory.
    This function identifies 'bus' subdirectories that contain false module matches using the
    'filter_false_module' function. It then moves these subdirectories into a separate 'vis_buses'
    subdirectory within the given directory for further investigation or visualization.

    Parameters:
    directory (str): The path to the directory containing 'bus' subdirectories.

    Returns:
    None

    Side effects:
    - Creates a 'vis_buses' subdirectory within the given directory if it does not exist.
    - Moves identified 'bus' subdirectories with false module matches into the 'vis_buses' subdirectory.

    Note:
    The function assumes that the 'filter_false_module' function is available and returns a list of
    'bus' subdirectory names that contain false module matches.
    """
    False_list = filter_false_module(directory)
    source = directory
    destination = os.path.join(directory, 'vis_buses')
    if not os.path.exists(destination):
        os.makedirs(destination)
    for bus_name in False_list:
        random_part = re.search(r'bus_\w+', bus_name).group()
        bus_folder = os.path.join(source, bus_name)
        shutil.move(bus_folder, os.path.join(destination, random_part))


def copy_csv_to_sorted_data():
    """
    Copies CSV files from a folder called 'KCM-Raw-Data' and pastes them into a folder called 'sorted_data'.
    This function looks for CSV files in the 'KCM-Raw-Data' subfolder located within the 'sorted_data' directory.
    It then copies each CSV file to the parent 'sorted_data' folder. If the 'sorted_data' folder does not exist,
    the function will create it before proceeding with the file copying process.

    Side effects:
    - If the 'sorted_data' folder does not exist, it is created.
    - CSV files from the 'KCM-Raw-Data' subfolder are copied to the 'sorted_data' folder.
    - The function prints out the names of the files as they are copied.

    Note:
    The function assumes that the 'sorted_data/KCM-Raw-Data' path is correct and accessible.
    It also assumes that the 'sorted_data' directory is the intended destination for the CSV files.
    """
    # Define paths
    source_folder = 'sorted_data/KCM-Raw-Data'
    destination_folder = 'sorted_data'
    
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Iterate over files in the source folder
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.csv'):
            # Construct paths for source and destination files
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            
            # Copy file to the destination folder
            shutil.copyfile(source_file_path, destination_file_path)
            #print(f"Copied: {file_name} to {destination_folder}")


"""
This script processes a collection of CSV files related to KCM data. It performs several operations
to organize, sort, and filter the data files based on specific criteria related to bus module serial numbers.

The script follows these steps:
1. Defines paths for raw data, unzipped sorted data, and a specific subfolder within the sorted data.
2. Checks if the unzipped sorted data directory exists:
   - If it does, it filters out and moves 'bus' subdirectories with false module matches.
   - If it doesn't, it unzips the raw data into the sorted data directory.
3. Copies CSV files from a subfolder to the main sorted data folder if the subfolder exists.
4. Groups files in the unzipped directory based on matching serial numbers and moves incomplete files.
5. Filters and moves 'bus' subdirectories with false module matches again after grouping.
6. Moves the 'vis_buses' subdirectory from within 'sorted_data' to the main directory level.

The script assumes that the necessary functions are defined elsewhere in the codebase or are being imported.
These functions include:
- `find_directory()`: Returns the current directory path formatted for concatenation.
- `filter_false_module(directory)`: Filters 'bus' subdirectories with false module matches.
- `move_false_bus(directory)`: Moves identified 'bus' subdirectories to a 'vis_buses' subdirectory.
- `group_files(directory)`: Groups CSV files by matching serial numbers into 'bus' subdirectories.
- `copy_csv_to_sorted_data()`: Copies CSV files from a specific subfolder to the main sorted data folder.

Note:
The script is designed to be used in an environment where the directory structure and file naming conventions
are consistent with those specified in the script. It also assumes that the 'KCM-Raw-Data.zip' file is located
in the 'Raw Data' directory.
"""
directory = find_directory() + 'Raw Data/'
unzip_directory = find_directory() + 'sorted_data/'
annoyingfolder = unzip_directory + 'KCM-Raw-Data/'

if os.path.exists(unzip_directory):
    filter_false_module(unzip_directory)
    move_false_bus(unzip_directory)
else:
    zip_filename = 'KCM-Raw-Data.zip'
    zip_directory = directory + zip_filename
    with zipfile.ZipFile(zip_directory, 'r') as zip_ref:
        zip_ref.extractall(unzip_directory)
    if os.path.exists(annoyingfolder):
        copy_csv_to_sorted_data()
    else:
        pass
group_files(unzip_directory)
filter_false_module(unzip_directory)
move_false_bus(unzip_directory)


current_path =  find_directory() + "sorted_data/vis_buses"
destination_path = find_directory() + "vis_buses"

shutil.move(current_path, destination_path)

vis_path = find_directory() + 'vis_buses'
sorted_path = find_directory() + "sorted_data"
all_folder = find_directory() + "all_buses"  

shutil.copytree(vis_path, all_folder)

for root, dirs, files in os.walk(sorted_path):
    for dir_name in dirs:
        # Check if the folder name starts with 'bus_'
        if dir_name.startswith('bus_'):
            # Construct paths for source and destination folders
            src_folder = os.path.join(root, dir_name)
            dst_folder = os.path.join(all_folder, dir_name)
            # Copy the folder to all_data
            shutil.copytree(src_folder, dst_folder)  

