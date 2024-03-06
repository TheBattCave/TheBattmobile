import csv
import pandas as pd
from os import listdir


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