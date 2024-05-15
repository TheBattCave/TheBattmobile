from ..build_specific_dfs import find_replaced_modules
from ..build_specific_dfs import swapped_mod_dataframes
import pandas as pd

directory = 'test_data_after_sorted/'

def test_find_replaced_modules_1():
    '''
    Tests to determine that the returned object is a dictionary
    '''
    replaced_dict = find_replaced_modules(directory)
    assert isinstance(replaced_dict, dict), 'Dictionary not returned'
    return

def test_find_replaced_modules_2():
    '''
    Tests to determine dictionary keys are of type strings.
    '''
    replaced_dict = find_replaced_modules(directory)
    for key in replaced_dict.keys():
        assert isinstance(key, str), 'Bus names are not strings.'
    return

def test_find_replaced_modules_3():
    '''
    Tests to determine that the dictionary values are lists.
    '''
    replaced_dict = find_replaced_modules(directory)
    for value in replaced_dict.values():
        assert isinstance(value, list), 'Returned values are not in a list format.'
    return

def test_find_replaced_modules_4():
    '''
    Tests to determine that the returned dictionary values' contents are of type string
    '''
    replaced_dict = find_replaced_modules(directory)
    for value in replaced_dict.values():
        for module in value:
            assert isinstance(module, str), 'Returned serials are not of type string.'
    return

def test_swapped_mod_dataframes_1():
    '''
    Tests to determine that a list is returned.
    '''
    df_swap = swapped_mod_dataframes(directory, 'g2--..-.-.-.-', 'cell voltages')
    assert isinstance(df_swap, list), "A list of dataframes is not returned"
    return

def test_swapped_mod_dataframes_2():
    '''
    Tests to determine that a list is returned.
    '''
    df_swap = swapped_mod_dataframes(directory, 'g2--..-.-.-.-', 'cell voltages')
    for df in df_swap:
        assert isinstance(df, pd.DataFrame), "Not all contents of list are Pandas Dataframes"
    return
