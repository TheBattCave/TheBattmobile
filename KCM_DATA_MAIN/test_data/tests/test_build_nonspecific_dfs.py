from ..build_nonspecific_dfs import build_bus_df
from ..build_nonspecific_dfs import build_module_df
# from ..sort_bus_by_date import sort_bus_by_date
import pandas as pd

directory = 'test_data_after_sorted/'

def test_build_bus_df_1():
    '''
    Tests to determine that the return is a Pandas Dataframe
    '''
    bus_df = build_bus_df(directory, 'bus_1/', 'Current')
    assert isinstance(bus_df, pd.DataFrame), 'Pandas DataFrame not returned'
    return

def test_build_module_df_1():
    '''
    Tests to determine that the return is a Pandas Dataframe
    '''
    module_df = build_module_df(directory, 'bus_1/', 1)
    assert isinstance(module_df, pd.DataFrame), 'Pandas DataFrame not returned'
    return