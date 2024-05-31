import os
import tempfile
import unittest
import zipfile
import pandas as pd
import shutil
import alfred
#import etl
#from vis import build_bus_df
data_path = os.path.join(alfred.__path__[0], 'data')

class TestBuildBusDF(unittest.TestCase):
    def setUp(self):
        # Setup code here if needed
        self.valid_directory = os.path.join(alfred.etl.find_directory(), 'alfred/sorted_test_data/vis_buses/')
        self.bus_num = "bus_0039142903b40233500710/"  
        #self.valid_keywords = ["Current", "Voltage", "Power"]

    def test_dataframe_creation_current(self):
        # Test to ensure a DataFrame is created for 'Current'
        keyword = "Current"
        result = alfred.vis.build_bus_df(self.valid_directory, self.bus_num, keyword)
        self.assertIsInstance(result, pd.DataFrame, "The result should be a pandas DataFrame for 'Current'")

    def test_dataframe_creation_voltage(self):
        # Test to ensure a DataFrame is created for 'Voltage'
        keyword = "Voltage"
        result = alfred.vis.build_bus_df(self.valid_directory, self.bus_num, keyword)
        self.assertIsInstance(result, pd.DataFrame, "The result should be a pandas DataFrame for 'Voltage'")

    def test_dataframe_creation_power(self):
        # Test to ensure a DataFrame is created for 'Power'
        keyword = "Power"
        result = alfred.vis.build_bus_df(self.valid_directory, self.bus_num, keyword)
        self.assertIsInstance(result, pd.DataFrame, "The result should be a pandas DataFrame for 'Power'")


    def tearDown(self):
        # Clean up code here if needed
        pass

class TestBuildModuleDF(unittest.TestCase):
    def setUp(self):
        # Setup code here if needed
        self.valid_directory = os.path.join(alfred.etl.find_directory(), 'alfred/sorted_test_data/vis_buses/')
        self.invalid_directory = os.path.join('alfred/sorted_test_data/sorted_data/incomplete_test/')
        self.bus_num = "bus_0039142903b40233500710/"  
    def test_dataframe_creation_for_valid_numbers(self):
        # Test to ensure a DataFrame is created for each valid number from 1 to 16
        for num in range(1, 17):
            with self.subTest(num=num):
                result = alfred.vis.build_module_df(self.valid_directory, self.bus_num, num)
                self.assertIsInstance(result, pd.DataFrame, f"The result should be a pandas DataFrame for module number {num}")

    def test_no_dataframe_creation_for_invalid_data(self):
        # Test to ensure no DataFrame is created for invalid/incomplete data
        num = 1
        try:
            result = alfred.vis.build_module_df(self.invalid_directory, self.bus_num, num)
            # Check if the function returns None or handles the case gracefully
            self.assertIsNone(result, "The result should be None for invalid/incomplete data")
        except Exception as e:
            # If an exception is raised, ensure it's the expected behavior
            self.assertIsInstance(e, (FileNotFoundError, pd.errors.EmptyDataError), "Expected an error due to invalid data")
    def test_invalid_number_input(self):
    # Test to ensure no DataFrame is created for invalid module number
        invalid_numbers = [ 17, -1, 'a']
        for num in invalid_numbers:
            with self.subTest(num=num):
                with self.assertRaises((ValueError, TypeError), msg=f"Expected a ValueError or TypeError for invalid module number {num}"):
                    alfred.vis.build_module_df(self.valid_directory, self.bus_num, num)

    def tearDown(self):
        # Clean up code here if needed
        pass

if __name__ == '__main__':
    unittest.main()