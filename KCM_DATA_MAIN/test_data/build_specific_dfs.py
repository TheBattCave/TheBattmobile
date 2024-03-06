import csv
from os import listdir
import pandas as pd
import re
from .sort_bus_by_date import sort_bus_by_date

def find_replaced_modules(directory):
    serial_index = 17
    bus_swapped_mods = {}
    # Storing modules that have been swapped with each bus number
    for folder in listdir(directory):
        if folder.startswith('bus'):
            bus = folder
            bus_slash = folder + '/'
            replaced_mods = set()
            # For storing modules that are confirmed swapped in and out
            modules_by_date = {}  # Storing every module per date
            serial_start_end = {}
            # Storing each unique module (from set) and
            # their starting and end times
            mod_set = set()
            # A set (unordered, no repeats) of
            # all module numbers in the bus folder
            # case of letter (i.e. to avoid A1 != a1)
            for file in listdir(directory + bus_slash):
                # For each bus folder
                df = sort_bus_by_date(directory, bus_slash)
                # Sarah's dataframe for organized files
                ordered_dates = []
                # List of ordered dates per bus folder
                ordered_csv = df['Filename'].tolist()
                # List of sorted CSV's by date
                ordered_unclean_dates = df['DateRetrieved'].tolist()
                # List of sorted dates corresponding to CSVs
                for unclean_date in ordered_unclean_dates:
                    split_results = unclean_date.strftime('%m/%d/%Y, %H:%M:%S')
                    ordered_dates.append(split_results)
                    # Organized dates as strings

                for i in range(len(ordered_csv)):
                    serials_in_csv = []
                    file_path = directory + bus_slash + ordered_csv[i]
                    with open(file_path) as file:
                        reader = csv.reader(file)
                        for row in reader:
                            for element in row:
                                if 'Mfg Data (ASCII)' in element:
                                    serial_num = element[serial_index:]
                                    mod_num = re.sub(r'\W+',
                                                     '',
                                                     serial_num).upper()
                                    if mod_num != '':
                                        serials_in_csv.append(mod_num)
                                        # Serials in CSV will be regex version
                                        mod_set.add((mod_num, serial_num))
                                        # Adding tuple with the regex
                                        # and non-regex version
                                    else:
                                        pass
                                else:
                                    pass
                    modules_by_date[ordered_dates[i]] = serials_in_csv
                    # Date to list of serials
                # Purpose of this section is just to
                # get a module number associated with start and end date
                for serial_tuple in mod_set:
                    # Look through every serial number in bus
                    count = 0
                    first_date = ''
                    latest_date = ''
                    start_end_list = []
                    base_serial = serial_tuple[0]  # Current serial of interest

                    for each_date in ordered_dates:
                        # For each date
                        # (keys to current_date_serials dictionary)
                        current_date_serials = modules_by_date[each_date]
                        # Getting list of the serials for current CSV/date
                        for comp_serial in current_date_serials:
                            if base_serial == comp_serial:
                                # Compare base serial to comparison serial
                                count += 1
                                latest_date = each_date
                                if count == 1:
                                    first_date = each_date
                                    start_end_list.append(first_date)
                                else:
                                    pass
                    start_end_list.append(latest_date)
                    serial_start_end[serial_tuple[1]] = start_end_list
                    # Uncleaned serial -> start and end dates

# Now compare start and end dates for each module to
# the first and last date of the ordered_csvs by date list
                for serial_key in serial_start_end:
                    start_end = serial_start_end[serial_key]
                    if (start_end[0] != ordered_dates[0] and
                            start_end[-1] != ordered_dates[-1]):
                        replaced_mods.add(serial_key)
                bus_swapped_mods[bus] = list(replaced_mods)
    return {k: v for k, v in bus_swapped_mods.items() if v}

# Function takes in characteristic argument.
# Please use one of the following

# 1. 'cell voltages' for acquiring data for the submodule voltages.
# 2. 'balancers' for acquiring data for the module cell balancers.
# 3. 'temperatures' for acquiring data for the module temperatures.
# 4. 'module voltages' for acquiring data for the overall module voltages.


def swapped_mod_dataframes(directory, serial_num, characteristic):
    '''
    Given a module characteristic and a serial number corresponding to
    a specific module, return dataframes for that characteristic specific to
    the provided module for each file in which that serial number occurs.
    Builds dataframes for a specific module across all CSVs given that module's unique serial identifier.
    '''
    serial_index = 17
    mod_num = re.sub(r'\W+', '', serial_num).upper()
    # Convert the serial number provided
    keyword = 'Mfg Data'
    index_dictionary = {
        'cell voltages': [5, 7, 8, 20],
        'balancers': [21, 23, 24, 36],
        'temperatures': [37, 39, 40, 42],
        'module voltages': [43, 45, 46, 47]
        # Numbers correspond to the number of rows from
        # the module number row that
        # needs to be skipped in order to reach
        # the following: title_row, column_row,
        # start_index of data values, end_index of values
    }

    title_ind = 0
    col_ind = 1
    start = 2
    end = 3
    # empty_space = -2 (never used)
    # key_list = index_dictionary.keys() (never used)
    list_bus_nums = []
    list_desired_dfs = []
    for file in listdir(directory):
        # Place this file in directory with False_files -> Keiton's code
        if file.startswith('bus'):
            list_bus_nums.append(file)
            # Getting list of bus names
    for bus in list_bus_nums:  # For each bus
        ordered_dates = []
        df = sort_bus_by_date(directory, bus + '/')
        ordered_csv = df['Filename'].tolist()
        ordered_unclean_dates = df['DateRetrieved'].tolist()
        for unclean_date in ordered_unclean_dates:
            split_results = unclean_date.strftime('%m/%d/%Y, %H:%M:%S')
            ordered_dates.append(split_results)
        for csv_file in range(len(ordered_csv)):
            # Iterate over each csv file in the current bus folder
            directory_path = directory + bus + '/' + ordered_csv[csv_file]
            # Convert this to file name (for file in bus folder)
            row_list = []
            with open(directory_path) as file:
                # Read in the CSV file specified as a list of rows
                reader = csv.reader(file)
                for row in reader:
                    row_list.append(row)
            for i in range(len(row_list)):
                # For each row in row_list
                for element in row_list[i]:
                    if element is not None:
                        if keyword in element:
                            mod_num_test = re.sub(
                                r'\W+', '', element[serial_index:]
                            ).upper()
                            if mod_num_test == mod_num:
                                char_low = characteristic.lower()
                                indices_list = index_dictionary[char_low]
                                title = row_list[i +
                                                 indices_list[title_ind]][0]
                                title = title + '  ' + ordered_dates[csv_file]
                                # Concatenate with Module Number
                                # (key to dictionary)
                                in_list = indices_list[col_ind]
                                full_column_labels = row_list[i + in_list][1:]
                                column_labels = [
                                    element for
                                    element in
                                    full_column_labels if
                                    element]
                                data_vals = []
                                row_labels = []
                                initial = indices_list[start]
                                finish = indices_list[end]
                                for j in range(initial, finish):
                                    full_row = row_list[i + j][1:]
                                    clean_row = [
                                        element for
                                        element in
                                        full_row if
                                        element
                                    ]
                                    data_vals.append(clean_row)
                                    row_labels.append(row_list[i + j][0])
                                df_characteristic = pd.DataFrame(
                                    data=data_vals,
                                    columns=column_labels,
                                    index=row_labels
                                )
                                for label in column_labels:
                                    dr = df_characteristic[label].astype('int')
                                    df_characteristic[label] = dr
                                index = df_characteristic.index
                                index.name = title
                                list_desired_dfs.append(df_characteristic)
    return list_desired_dfs