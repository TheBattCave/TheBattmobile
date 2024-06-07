import alfred
import unittest
import altair as alt
import csv
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
import shutil
import numpy as np
import os
import sys
from io import StringIO
from os import listdir
from sklearn.decomposition import PCA

data_path = os.path.join(alfred.__path__[0], 'data/sorted_test_data')

class TestCountSwappedModules(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'all_buses/')

    def test_count_swapped_modules_output(self):
        # Capture the output of the function
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call the function
        output = alfred.count_swapped_modules(self.valid_directory)

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Get the captured output
        captured_output_str = captured_output.getvalue()

        # Check if the key elements are in the captured output
        self.assertIn("COUNT OF SWAPPED MODULES", captured_output_str)
        self.assertIn("Count of '0':", captured_output_str)
        self.assertIn("Count of '1':", captured_output_str)
        self.assertIn("0 = healthy and 1 = swapped", captured_output_str)
    def tearDown(self):
         pass


class TestStandardizeColumns(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'all_buses/') 
    def test_standardize_columns(self):
        df = alfred.count_mod_changes(self.valid_directory)
        
        result = alfred.standardize_columns(df)
        
        self.assertIsInstance(result, pd.DataFrame)
        
    def tearDown(self):
         pass   

class TestBuildAllVoltagesDF(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'all_buses/') 
   
    def test_returns_dataframe(self):
        result = alfred.build_all_voltages_df(self.valid_directory)
        self.assertIsInstance(result, pd.DataFrame, "The function should return a pandas DataFrame")
        
    def test_includes_bus_column(self):
        result = alfred.build_all_voltages_df(self.valid_directory)
        self.assertIn('Bus', result.columns, "The DataFrame should include a 'Bus' column")
        
    def test_includes_module_column(self):
        result = alfred.build_all_voltages_df(self.valid_directory)
        self.assertIn('Module', result.columns, "The DataFrame should include a 'Module' column")
    def tearDown(self):
         pass   

class TestMeanCenter(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'all_buses/') 
    
    def test_output_is_tuple_with_three_elements(self):
        result = alfred.mean_center(self.valid_directory)
        self.assertIsInstance(result, tuple, "The function should return a tuple")
        self.assertEqual(len(result), 3, "The tuple should have exactly three elements")
    def tearDown(self):
         pass  
if __name__ == '__main__':
    unittest.main()
