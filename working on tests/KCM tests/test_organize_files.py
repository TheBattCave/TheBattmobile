from os import listdir
from ..organize_files import find_directory
from ..organize_files import grab_csv
from ..organize_files import group_files
# import organize_files

def test_find_directory_1():
    '''
    Tests that the returned directory path is a string.
    '''
    directory = find_directory()
    assert isinstance(directory, str), 'The returned directory is not a string'
    return

def test_grab_csv_1():
    '''
    Tests that the return is a list.
    '''
    directory = 'test_data_raw/'
    list_of_csv = grab_csv(directory)
    assert isinstance(list_of_csv, list), 'Returned CSV file names is not in list format.'
    return

def test_grab_csv_2():
    '''
    Tests that the returned list only contains strings.
    '''
    directory = 'test_data_raw/'
    list_of_csv = grab_csv(directory)
    for file_name in list_of_csv:
        assert isinstance(file_name, str), 'The returned list of file names contains elements that are not strings'
    return

def test_grab_csv_3():
    '''
    Tests that the returned strings all end with '.csv'.
    '''
    directory = 'test_data_raw/'
    list_of_csv = grab_csv(directory)
    for file_name in list_of_csv:
        assert file_name.endswith('.csv'), 'The returned list of file names contains elements that are not CSV files.'
    return

def test_group_files_1():
    '''
    Tests that the function has grouped the test files into bus_1, bus_2, and incomplete folders.
    '''
    target_folders = ['bus_1', 'bus_2', 'incomplete']
    grouped_folders = []
    directory = 'test_data_after_sorted/'
    group_files(directory)
    for filename in listdir(directory):
        grouped_folders.append(filename)
    for target in target_folders:
        assert target in grouped_folders, 'Ideally, grouping function should produce three folders of names: bus_1, bus_2, and incomplete. One or more folders missing.'
    return

def test_group_files_2():
    '''
    Tests that the function has grouped the test files into bus_1, bus_2, and incomplete folders.
    '''
    directory = 'test_data_raw/'
    target_folders = [directory + 'bus_1', directory + 'bus_2', directory + 'incomplete']
    group_files(directory)
    for folder in target_folders:
        list_of_csv = grab_csv(folder)
        assert len(list_of_csv) != 0, 'There is an empty folder.'
    return

def test_group_files_3():
    '''
    Tests that the organized folders contain csv files only.
    '''
    directory = 'test_data_raw/'   
    target_folders = [directory + 'bus_1', directory + 'bus_2', directory + 'incomplete']
    group_files(directory)
    for folder in target_folders:
        list_of_csv = grab_csv(folder)
        for file in list_of_csv:
            assert file.endswith('.csv'), 'There is an non-CSV file in one of the bus directories.'
    return
