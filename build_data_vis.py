import altair as alt
import csv
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
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


def build_bus_df(directory, bus_num, keyword):
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


def visualize_mod_time(directory, bus_num, module_num):
    df = build_module_average_df(directory, bus_num, module_num)
    df = df.reset_index()
    data = df.melt('DateRetrieved', var_name='voltage', value_name='counts')
    dates = list(data['DateRetrieved'].unique())

    brush = alt.selection_interval(bind='scales')
    input_dropdown = alt.binding_select(options=dates)
    selection = alt.selection_single(fields=['DateRetrieved'],
                                     bind=input_dropdown,
                                     name=' ')
    color = alt.condition(selection,
                          alt.Color('DateRetrieved:N'),
                          alt.value('lightgray'))

    line = alt.Chart(data.reset_index()).mark_line().encode(
        x='voltage:Q',
        y='counts:Q',
        color=color,
        tooltip='Name:N'
    ).add_selection(
        brush,
        selection
    )

    return line


def count_mod_changes(directory):
    '''
    Counts changes in modules sequentially for a bus
    over all CSV files for all buses.
    Outputs dataframe that is used for heatmap visualizations.
    '''
    keyword = 'Mfg Data (ASCII)'
    list_bus_nums = []  # To get the name of bus number folders
    bus_to_ordered_csvs = {}
    # Dictionary associating each bus folder
    # with an chronologically ordered list of CSVs
    bus_to_ordered_dates = {}
    # Dictionary associating each bus folder
    # with dates listed chronologically
    file_serials = {}  # Dictionary with serial numbers for each CSV
    list_df = []  # List of dataframes for each bus
    column_names = ['Bus', 'Module', 'Date', 'Change']
    num_mods = 16  # Constant number of mods
    module_index = 8  # For grabbing module string indices later
    bus_single = 5
    bus_double = 6
    last_two_chars = -2  # For grabbing last two characters
    last_one_chars = -1  # For grabbing last character
    mod_index = ['Module ' + str(i) for i in range(1, num_mods + 1)]
    # Creating rows for dataframe
    mod_change_count = {}
    # Dictionary for number of changes,
    # sum value for each module # as compared file to file
    keyword = 'Mfg Data (ASCII)'  # Keyword to search for
    for file in listdir(directory):
        # Place this file in directory with False_files -> Keiton's code
        if file.startswith('bus'):
            list_bus_nums.append(file)  # Getting list of bus names
    for bus in list_bus_nums:  # For each bus
        ordered_dates = []
        df = sort_bus_by_date(directory, bus + '/')
        ordered_csv = df['Filename'].tolist()
        ordered_unclean_dates = df['DateRetrieved'].tolist()
        for unclean_date in ordered_unclean_dates:
            split_results = unclean_date.strftime('%m/%d/%Y, %H:%M:%S')
            ordered_dates.append(split_results)
        bus_to_ordered_csvs[bus] = ordered_csv
        # Grabbing a sorted list of CSV's for each bus folder
        bus_to_ordered_dates[bus] = ordered_dates
        # Grabbing a sorted list of dates for each folder
    for bus_key in bus_to_ordered_csvs:
        # For each bus folder (key value for bus to ordered files dictionary)
        for mod_name in mod_index:
            # Setting dictionary with all module count at 0 to start.
            # Should be for each bus.
            mod_change_count[mod_name] = [0]
            # Add the dataframe at the end of the comparisons to the list_df
        ordered_dates = bus_to_ordered_dates[bus_key]
        # Grab list of dates for dataframe use later
        ordered_csvs = bus_to_ordered_csvs[bus_key]
        # Grab the list of ordered CSV's associated with current bus folder
        for i in range(len(ordered_csvs)):
            # For each file in the list of ordered CSV's
            serial_nums = []
            # Start with empty list of serial numbers for that file
            with open(directory + bus_key + '/' + ordered_csvs[i]) as file:
                # Looking through current file
                reader = csv.reader(file)
                for row in reader:
                    for element in row:
                        if keyword in element:
                            mod_num = re.sub(r'\W+', '', element[17:]).lower()
                            serial_nums.append(mod_num)
                            # Grabbing serial numbers for each CSV file
                        else:
                            pass
            # After you get all the serial numbers for a file
            serial_nums.pop(0)  # Getting rid of first module number
            file_serials[ordered_csvs[i]] = serial_nums
            # Key: file name. Value: List of serial numbers for that file name

        # At this point, we have a list of
        # serial numbers associated with each CSV file
        i = 0
        while(i < len(ordered_csvs) - 1):
            # While we are not looking at the last file
            # (can't compare last file with anything)
            first_mods = file_serials[ordered_csvs[i]]
            # Gets you first list of serials
            next_mods = file_serials[ordered_csvs[i + 1]]
            # Get second list of serials
            for j in range(len(first_mods)):
                # For each index (mod #) in the list of modules
                m_str = "Module " + str(j + 1)
                # For first iteration, "Module 1"
                if first_mods[j] != next_mods[j]:
                    mod_change_count[m_str].append(mod_change_count[m_str][-1]
                                                   + 1)
                    # If different, append prev. count + 1
                else:
                    mod_change_count[m_str].append(mod_change_count[m_str][-1])
                    # If same, just append prev. count
            i += 1

        # Now we have dictionary with count of changes per file
        # compared for each module (16 mods)
        num_comps = len(ordered_csvs) - 1
        bus_num_element = ''
        if len(bus_key) == bus_single:
            bus_num_element = bus_key[-1]
        elif len(bus_key) == bus_double:
            bus_num_element = bus_key[-2:]
        else:
            bus_num_element = bus_key[-3:]
            # print(bus_num_element)
        bus_number_list = [bus_num_element for
                           i in range((num_comps + 1) * num_mods)]
        # To get the bus # values
        module_labels = []
        change_labels = []
        mod_num_label = ''
        for mod_label in mod_change_count.keys():
            # For each module number 1 through 16
            change_labels += mod_change_count[mod_label]
            if len(mod_label) > module_index:
                mod_num_label = mod_label[last_two_chars:]
            else:
                mod_num_label = mod_label[last_one_chars]
            for i in range(num_comps + 1):
                module_labels.append(mod_num_label)
        date_labels = ordered_dates * num_mods
        data_lists = [bus_number_list,
                      module_labels,
                      date_labels,
                      change_labels]
        df_dict = {}
        for column, data_list in zip(column_names, data_lists):
            df_dict[column] = data_list
        df_bus_changes = pd.DataFrame(data=df_dict)
        list_df.append(df_bus_changes)
    return pd.concat(list_df, axis=0)


def visualise_mod_changes(directory):
    df1 = count_mod_changes(directory)
    data = df1.melt(id_vars=['Bus', 'Module', 'Date'])
    buses = list(data['Bus'].unique())
    alt.data_transformers.disable_max_rows()
    select_bus = alt.selection_single(
        name='Select', fields=['Bus'], init={'Bus': 1},
        bind=alt.binding_select(options=buses)
    )

    chart = alt.Chart(data).mark_rect(stroke='black').encode(
        x=alt.X('Date', title="Date", sort=None),
        y=alt.Y('Module', title="Module", sort=None),
        color=alt.Color('value', legend=None)
    ).add_selection(select_bus).transform_filter(select_bus)

    return chart
    
    
def mod_change_statistics(directory):
    df1 = count_mod_changes(directory)
    grouped_times_changed = df1.groupby(['Bus', 'Module'], sort=None)['Change'].max()
    average_times_changed = grouped_times_changed.groupby(['Module'], sort=None).mean()
    chart = average_times_changed.plot(kind='bar', figsize=(6,4), fontsize=14, colormap='viridis')
    plt.xlabel('Module', fontsize=16)
    plt.ylabel('Average times changed', fontsize=16)
    
    return chart


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
