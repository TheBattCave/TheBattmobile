from ..heatmap_mod_changes import count_mod_changes
import pandas as pd

directory = 'test_data_after_sorted/'

def test_count_mod_changes_1():
    '''
    Tests to determine that the return is a Pandas Dataframe
    '''
    count_df = count_mod_changes(directory)
    assert isinstance(count_df, pd.DataFrame), 'Pandas DataFrame not returned'
    return

def test_count_mod_changes_2():
    '''
    Tests to determine that the returned dataframe contains integers only for count for visualization purposes.
    '''
    count_df = count_mod_changes(directory)
    for count in count_df['Change']:
        assert isinstance(count, int), 'Count is not an integer, invalid count'
    return
