import altair as alt
import csv
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
from os import listdir

from .etl import find_directory, sort_bus_by_date


def build_bus_df(directory, bus_num, keyword):
    '''
    Creates a DataFrame for a desired bus that displays one of three variables 
    (Current, Voltage, or Power) with the time, in seconds, the bus has spent 
    in discrete intervals for the chosen variable.
    
    Parameters:
    - directory (str): The directory where the files can be found.
    - bus_num (str): The desired bus, written as "bus_" followed by the bus serial number.
    - keyword (str): Keyword for the desired variable to display ('Current', 'Voltage', or 'Power').
    '''
    bus_dates = sort_bus_by_date(directory, bus_num)

    # Check for desired variable
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

    dfs = []
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        dfs.append(tmp)

    bus_parameter = pd.concat(dfs, ignore_index=True)
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    bus_parameter.columns = df_index.columns

    loc_parameter = bus_parameter.columns.str.contains('^Unnamed')
    bus_parameter = bus_parameter.loc[:, ~loc_parameter]
    bus_parameter.reset_index(drop=True, inplace=True)

    return bus_parameter


def build_module_df(directory, bus_num, module_num):
    '''
    Creates a DataFrame of voltages from one module with the rows sequential in time.
    
    Parameters:
    - directory (str): The directory containing the bus files.
    - bus_num (str): The desired bus directory.
    - module_num (int): The integer module number (between 1 and 16).
    
    Note:
    - The module data within the csv files is further subdivided into 12 submodules. 
      Therefore, this function will output 12 rows for each date retrieved within the bus folder.
      For example, running this function on bus 1 module 1 should return a DataFrame with 216 rows.
      Rows 0-11 correspond to the first date in the bus folder, then rows 12-24 to the next date, etc.
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
        module_df = pd.concat([module_df, tmp], ignore_index=True)
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    module_df.columns = df_index.columns

    module_df = module_df.loc[:, ~module_df.columns.str.contains('^Unnamed')]
    module_df.reset_index(drop=True, inplace=True)

    return module_df


def build_module_temp(directory, bus_num, module_num):
    '''
    Creates a DataFrame of temperatures from one module with the rows sequential in time.
    
    Parameters:
    - directory (str): The directory containing the bus files.
    - bus_num (str): The desired bus directory.
    - module_num (int): The integer module number (between 1 and 16).
    '''
    bus_dates = sort_bus_by_date(directory, bus_num)
    start_row = 83 + (11+47) * (module_num - 1)
    end_row = start_row + 2
    row_list = list(range(start_row)) + list(range(end_row, 960))
    index_range = list(range(82)) + list(range(83, 960))

    module_temp = pd.DataFrame()
    for i in range(len(bus_dates)):
        file = bus_dates['Filename'].loc[i]
        file_dir = directory + bus_num + file
        tmp = pd.read_csv(file_dir, header=None, skiprows=row_list)
        module_temp = pd.concat([module_temp, tmp], ignore_index=True)
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    module_temp.columns = df_index.columns

    module_temp = module_temp.loc[:, ~module_temp.columns.str.contains('^Unnamed')]
    module_temp.reset_index(drop=True, inplace=True)
    
    return module_temp


def build_module_average_df(directory, bus_num, module_num):
    '''
    Creates a DataFrame of voltages from one module with the rows sequential in time.
    Similar to build_module_df, but averages the submodule data together to return 
    only one row for each date for the module specified. 
    
    Parameters:
    - directory (str): The directory containing the bus files.
    - bus_num (str): The desired bus directory.
    - module_num (int): The integer module number (between 1 and 16).
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
        tmp_ave = tmp.mean().to_frame().transpose()  # Convert tmp_ave to a DataFrame with one row
        module_average_df = pd.concat([module_average_df, tmp_ave], ignore_index=True)

    # Once the loop completes, you can set the column names as before
    df_index = pd.read_csv(file_dir, header=0, skiprows=index_range)
    df_index = df_index.loc[:, ~df_index.columns.str.contains('^Unnamed')]
    module_average_df.columns = df_index.columns
    module_average_df.reset_index(drop=True, inplace=True)

    # Define 'string' here or adjust it based on your data
    string = 'DateRetrieved'

    # Concatenate the 'DateRetrieved' column to module_average_df_final
    module_average_df_final = pd.concat([module_average_df, bus_dates[string].astype(str)], axis=1)
    module_average_df_final = module_average_df_final.set_index(string)

    return module_average_df_final


def visualize_mod_time(directory, bus_num, module_num):
    '''
    Visualizes the distribution of time spent at each voltage in the voltage range 
    for a given module. Running this function returns a graph with 12 plotted 
    lines, one for each individual date in a given bus, where the x axis is voltage 
    and the y axis is time in seconds. A dropdown menu allows selection of a specific 
    date. Selected date remains in color, other dates are rendered gray. Axes are 
    scalable by clicking & dragging or by mouse scroll.
    
    Parameters:
    - directory (str): The directory where the files can be found.
    - bus_num (str): The desired bus, written as "bus_" followed by the bus serial number.
    - module_num (int): The integer module number (between 1 and 16).

    Returns:
    - line (Altair Chart Object): Altair chart displaying the visualization.
    '''
    df = build_module_average_df(directory, bus_num, module_num)
    df = df.reset_index()
    data = df.melt('DateRetrieved', var_name='voltage', value_name='counts')
    dates = list(data['DateRetrieved'].unique())

    brush = alt.selection_interval(bind='scales')
    input_dropdown = alt.binding_select(options=dates)
    selection = alt.selection_point(fields=['DateRetrieved'],
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
    ).add_params(
        brush,
        selection
    )

    return line


def count_mod_changes(directory):
    '''
    Counts changes in modules sequentially for each bus over all CSV files for all buses. 
    Outputs a DataFrame that is used for heatmap visualizations.
    
    Parameters:
    - directory (str): The directory where the files sorted by bus can be found.
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
    '''
    Uses the count_mod_changes output to produce a heatmap for all buses in the directory, 
    indicating when the modules have been changed (with a color change indicating the module 
    has been changed). The heatmap includes a drop-down menu to select the desired bus to view.
    
    Parameters:
    - directory (str): The directory where the files can be found.

    Returns:
    - chart (Altair Chart Object): Altair chart displaying the heatmap.
    '''
    df1 = count_mod_changes(directory)
    data = df1.melt(id_vars=['Bus', 'Module', 'Date'])
    buses = list(data['Bus'].unique())
    alt.data_transformers.disable_max_rows()
    select_bus = alt.selection_point(
        name='Select', fields=['Bus'],
        bind=alt.binding_select(options=buses)
    )

    chart = alt.Chart(data).mark_rect(stroke='black').encode(
        x=alt.X('Date', title="Date", sort=None),
        y=alt.Y('Module', title="Module", sort=None),
        color=alt.Color('value', legend=None)
    ).add_params(select_bus).transform_filter(select_bus)

    return chart
    
    
def mod_change_statistics(directory):
    '''
    Uses the count_mod_changes output to calculate and graph statistics on how often a 
    given module is changed across all of the bus data. This allows us to see if module 
    position has an effect on the frequency of module failure.
    
    Parameters:
    - directory (str): The directory where the files can be found.

    Returns:
    - chart (Matplotlib Axes Object): Bar chart displaying the average times each module is changed.
    '''
    df1 = count_mod_changes(directory)
    grouped_times_changed = df1.groupby(['Bus', 'Module'], sort=None)['Change'].max()
    average_times_changed = grouped_times_changed.groupby(['Module'], sort=None).mean()
    chart = average_times_changed.plot(kind='bar', figsize=(6,4), fontsize=14, colormap='viridis')
    plt.xlabel('Module', fontsize=16)
    plt.ylabel('Average times changed', fontsize=16)
    
    return chart


def find_replaced_modules(directory):
    '''
    Makes a DataFrame showing the bus, module number and the number of times the module has been changed.
    
    Parameters:
    - directory (str): The directory where the files can be found, sorted by bus.
    '''
    serial_index = 17
    bus_swapped_mods = {}
    # Storing modules that have been swapped with each bus number
    for folder in listdir(directory):
        if folder.startswith('bus_'):
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
    Makes a DataFrame for a specific characteristic (Cell Voltage, Balancers, Temperature, Module Voltages) of
    a desired module, containing each bus file in which the module's serial number occurs (across buses).
    
    Parameters:
    - directory (str): The directory where the files can be found.
    - serial_num (str): The serial number corresponding to a specific module.
    - characteristic (str): The module characteristic ('cell voltages', 'balancers', 'temperatures', 'module voltages').

    Returns:
    - list_desired_dfs (list): A list of DataFrames for the provided characteristic specific to the provided module.
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

def label_bad_module(directory):
    '''
    Counts changes in modules sequentially for each bus over all CSV files for all buses. 
    Outputs a DataFrame that is used for heatmap visualizations.
    
    Parameters:
    - directory (str): The directory where the files sorted by bus can be found.
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
        while i < len(ordered_csvs) - 1:
            first_mods = file_serials[ordered_csvs[i]]
            next_mods = file_serials[ordered_csvs[i + 1]]
            
            for j in range(len(first_mods)):
                m_str = "Module " + str(j + 1)
                prev_m_str = "Module " + str(j) if j > 0 else "Module 1"
                if first_mods[j] != next_mods[j]:
                    # If serials differ, set change for the previous module
                    # to 1
                    mod_change_count[prev_m_str].append(1)
                else:
                    # If serials are the same, set the change 
                    # for the previous module to 0
                    mod_change_count[prev_m_str].append(0)
            
            i += 1
            
        # Now we have dictionary with count of changes per file
        # compared for each module (16 mods)
        num_comps = len(ordered_csvs) - 1
        bus_num_element = bus_key
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