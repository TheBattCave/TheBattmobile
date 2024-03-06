import datetime
import pandas as pd
from ..sort_bus_by_date import sort_bus_by_date

# test_data = 'test_data/'
directory = 'test_data_after_sorted/'
# directory = 'test_data/'

def test_sort_by_bus_1():
    '''
    Tests to determine that a dataframe was returned.
    '''
    df = sort_bus_by_date(directory, 'bus_1/')
    assert isinstance(df, pd.DataFrame), 'No pandas DataFrame was returned'
    return

def test_sort_by_bus_2():
    '''
    Tests to determine that the date column of the dataframe contains only datetime type.
    '''
    df = sort_bus_by_date(directory, 'bus_1/')
    date_col = df['DateRetrieved']
    for date in date_col:
        assert isinstance(date, datetime.datetime), 'Date column contains non-datetime types, dates may not be in order chronologically'
    return

def test_sort_by_bus_3():
    '''
    Tests to determine that the name column of the dataframe contains only csv strings.
    '''
    df = sort_bus_by_date(directory, 'bus_1/')
    file_col = df['Filename']
    for file in file_col:
        assert isinstance(file, str), 'Names of files are not strings'
    return
