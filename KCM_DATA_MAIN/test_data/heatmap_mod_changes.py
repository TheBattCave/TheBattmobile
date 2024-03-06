import csv
from os import listdir
import pandas as pd
import re
from .sort_bus_by_date import sort_bus_by_date


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