from ..filter_false_modules import count_bus_file
from ..filter_false_modules import filter_false_module
from ..filter_false_modules import compare_file_mods
import numpy as np
import pandas as pd
import os
from os import listdir

directory = 'test_data_after_sorted/'

def test_count_bus_file_1():
    '''
    Test to determine that returned bus folders of test data is 2.
    '''
    bus_count = count_bus_file(directory)
    assert bus_count == 2, "Number of buses in folder should be 2"
    return

def test_filter_false_module_1():
    '''
    Test the function should return an array type
    '''
    return_type = filter_false_module(directory)
    assert isinstance(return_type,np.ndarray),'The return type is not an array'
    return

def test_filter_false_module_2():
    '''
    Test the function should return a list type and each element should be string
    '''
    return_list = filter_false_module(directory)
    for element in return_list:
        assert isinstance(element,str),'Each element in this list should be string.'
    return

def test_move_false_bus_1():
    '''
    Test each folder that get relocated should have at least two csv files.
    '''
    for file in listdir(directory):
        if file.startswith('bus'):
            directory_path = os.path.join(directory, file)
            each_bus = listdir(directory_path)
            assert len(each_bus) >= 2, 'Each bus file should contain at least two csv files.'
        else:
            pass
    return

def test_move_false_bus_2():
    '''
    Test each folder that get relocated should have be all csv type files.
    '''
    for file in listdir(directory):
        directory_path = os.path.join(directory, file)
        each_bus = listdir(directory_path)
        for element in each_bus:
            assert element.endswith('.csv'), 'There is a non csv file.'
    return


def test_compare_file_mods_1():
    '''
    Tests that function returns a dictionary
    '''
    return_type = compare_file_mods(directory)
    assert isinstance(return_type,dict), 'The returned type is not a dictionary'
    return


def test_compare_file_mods_2():
    '''
    Tests that dictionary returns a pandas dataframe when type in attribute name, such as "bus_1"
    '''
    test_folder = ['bus_1','bus_2']
    dic = compare_file_mods(directory)
    for folder_name in test_folder:
        dic_key = dic[folder_name]
        assert isinstance(dic_key,pd.DataFrame), 'The returned type is not a pandas dataframe'
    return


def test_compare_file_mods_3():
    '''
    Tests that returned dataframe has 16 index, from "Module 1" to "Module 16"
    '''
    test_folder = ['bus_1', 'bus_2']
    dic = compare_file_mods(directory)
    for folder_name in test_folder:
        dic_key = dic[folder_name]
        index_len = dic_key.index
        assert len(index_len) == 16, 'The dataframe is not in complete form, module number is not 16'
    return