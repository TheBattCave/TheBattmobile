import os
import tempfile
import unittest
import zipfile
import pandas as pd
import shutil
import alfred
import altair as alt
import matplotlib.pyplot as plt
#import etl
#from vis import build_bus_df

data_path = os.path.join(alfred.__path__[0], 'data/sorted_test_data')
bad_data_path = os.path.join(alfred.__path__[0], 'data/sorted_test_data')
class TestBuildBusDF(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.bus_num = "bus_0039142903b40233500710/"  
        #self.valid_keywords = ["Current", "Voltage", "Power"]

    def test_dataframe_creation_current(self):
        # Test to ensure a DataFrame is created for 'Current'
        keyword = "Current"
        result = alfred.build_bus_df(self.valid_directory, self.bus_num, keyword)
        self.assertIsInstance(result, pd.DataFrame, "The result should be a pandas DataFrame for 'Current'")

    def test_dataframe_creation_voltage(self):
        # Test to ensure a DataFrame is created for 'Voltage'
        keyword = "Voltage"
        result = alfred.build_bus_df(self.valid_directory, self.bus_num, keyword)
        self.assertIsInstance(result, pd.DataFrame, "The result should be a pandas DataFrame for 'Voltage'")

    def test_dataframe_creation_power(self):
        # Test to ensure a DataFrame is created for 'Power'
        keyword = "Power"
        result = alfred.build_bus_df(self.valid_directory, self.bus_num, keyword)
        self.assertIsInstance(result, pd.DataFrame, "The result should be a pandas DataFrame for 'Power'")


    def tearDown(self):
        
        pass

class TestBuildModuleDF(unittest.TestCase):
    def setUp(self):
   
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.invalid_directory = os.path.join(bad_data_path, 'sorted_data/incomplete_test/')
        self.bus_num = "bus_0039142903b40233500710/"  
    def test_dataframe_creation_for_valid_numbers(self):
        # Test to ensure a DataFrame is created for each valid number from 1 to 16
        for num in range(1, 17):
            with self.subTest(num=num):
                result = alfred.build_module_df(self.valid_directory, self.bus_num, num)
                self.assertIsInstance(result, pd.DataFrame, f"The result should be a pandas DataFrame for module number {num}")

    def test_no_dataframe_creation_for_invalid_data(self):
        # Test to ensure no DataFrame is created for invalid/incomplete data
        num = 1
        try:
            result = alfred.build_module_df(self.invalid_directory, self.bus_num, num)
            # Check if the function returns None or handles the case gracefully
            self.assertIsNone(result, "The result should be None for invalid/incomplete data")
        except Exception as e:
            # If an exception is raised, ensure it's the expected behavior
            self.assertIsInstance(e, (FileNotFoundError, pd.errors.EmptyDataError), "Expected an error due to invalid data")
    def test_invalid_number_input(self):
        # Test to ensure no DataFrame is created for invalid module number
            invalid_numbers = [ 17, -1, 'DavidBeck']
            for num in invalid_numbers:
                with self.subTest(num=num):
                    with self.assertRaises((ValueError, TypeError), msg=f"Expected a ValueError or TypeError for invalid module number {num}"):
                        alfred.build_module_df(self.valid_directory, self.bus_num, num)
   
    def tearDown(self):
        
        pass

data_path = os.path.join(alfred.__path__[0], 'data/sorted_test_data')
bad_data_path = os.path.join(alfred.__path__[0], 'data/sorted_test_data')

class TestBuildTempDF(unittest.TestCase):
    def setUp(self):
   
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.invalid_directory = os.path.join(bad_data_path, 'sorted_data/incomplete_test/')
        self.bus_num = "bus_0039142903b40233500710/"  
    
    def test_dataframe_creation_for_valid_numbers_temp(self):
        # Test to ensure a DataFrame is created for each valid number from 1 to 16
        for num in range(1, 17):
            with self.subTest(num=num):
                result = alfred.build_module_temp(self.valid_directory, self.bus_num, num)
                self.assertIsInstance(result, pd.DataFrame, f"The result should be a pandas DataFrame for module number {num}")
    def test_no_dataframe_creation_for_invalid_data_temp(self):
        # Test to ensure no DataFrame is created for invalid/incomplete data
        num = 1
        try:
            result = alfred.build_module_temp(self.invalid_directory, self.bus_num, num)
            # Check if the function returns None or handles the case gracefully
            self.assertIsNone(result, "The result should be None for invalid/incomplete data")
        except Exception as e:
            # If an exception is raised, ensure it's the expected behavior
            self.assertIsInstance(e, (FileNotFoundError, pd.errors.EmptyDataError), "Expected an error due to invalid data")
   
    def test_invalid_number_input_temp(self):
        # Test to ensure no DataFrame is created for invalid module number
            invalid_numbers = [ 17, -1, 'DavidBeck']
            for num in invalid_numbers:
                with self.subTest(num=num):
                    with self.assertRaises((ValueError, TypeError), msg=f"Expected a ValueError or TypeError for invalid module number {num}"):
                        alfred.build_module_temp(self.valid_directory, self.bus_num, num)
    def tearDown(self):
        
        pass
        
class TestBuildAvg(unittest.TestCase):
    def setUp(self):
   
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.invalid_directory = os.path.join(bad_data_path, 'sorted_data/incomplete_test/')
        self.bus_num = "bus_0039151006940233500710/"  
    
    def test_dataframe_creation_for_valid_numbers_avg(self):
        # Test to ensure a DataFrame is created for each valid number from 1 to 16
        for num in range(1, 17):
            with self.subTest(num=num):
                result = alfred.build_module_average_df(self.valid_directory, self.bus_num, num)
                self.assertIsInstance(result, pd.DataFrame, f"The result should be a pandas DataFrame for module number {num}")
    def test_no_dataframe_creation_for_invalid_data_avg(self):
        # Test to ensure no DataFrame is created for invalid/incomplete data
        num = 1
        try:
            result = alfred.build_module_average_df(self.invalid_directory, self.bus_num, num)
            # Check if the function returns None or handles the case gracefully
            self.assertIsNone(result, "The result should be None for invalid/incomplete data")
        except Exception as e:
            # If an exception is raised, ensure it's the expected behavior
            self.assertIsInstance(e, (FileNotFoundError, pd.errors.EmptyDataError), "Expected an error due to invalid data")
    def test_invalid_number_input_avg(self):
        # Test to ensure no DataFrame is created for invalid module number
            invalid_numbers = [ 17, -1, 'DavidBeck']
            for num in invalid_numbers:
                with self.subTest(num=num):
                    with self.assertRaises((ValueError, TypeError), msg=f"Expected a ValueError or TypeError for invalid module number {num}"):
                        alfred.build_module_average_df(self.valid_directory, self.bus_num, num)
    def test_invalid_number_input_avg_keyerror(self):
        # Test for KeyError when module_num is 0
        with self.assertRaises(KeyError):
            alfred.build_module_average_df(self.valid_directory, self.bus_num, 0)
            
    def tearDown(self):
        
        pass
        
class TestVisualizeModTime(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.bus_num = 'bus_0039151006940233500710/'
        self.module_num = 1  
        
    def test_visualize_mod_time_output(self):
        # Call the function with test inputs
        chart = alfred.visualize_mod_time(self.valid_directory, self.bus_num, self.module_num)
        
        # Check that the output is an Altair Chart object
        self.assertIsInstance(chart, alt.Chart)

        # Optional: You can add more checks, for example, verifying the chart properties
        self.assertIn('mark_line', dir(chart))
        
    def test_visualize_mod_time_invalid_module_num(self):
        # List of invalid module numbers to test
        invalid_module_nums = [-1, 17]

        for module_num in invalid_module_nums:
            with self.assertRaises(ValueError):
                alfred.visualize_mod_time(self.valid_directory, self.bus_num, module_num)
    
    def test_visualize_mod_time_key_error(self):
        # Test for KeyError when module_num is 0
        with self.assertRaises(KeyError):
            alfred.visualize_mod_time(self.valid_directory, self.bus_num, 0)
    
    def test_visualize_mod_time_type_error(self):
        # Test for TypeError when module_num is 'DavidBeck'
        with self.assertRaises(TypeError):
            alfred.visualize_mod_time(self.valid_directory, self.bus_num, 'DavidBeck')           
   
    def tearDown(self):
        
        pass
    
class TestCountModChanges(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')    
    
    def test_count_mod_changes_output(self):
 
        df = alfred.count_mod_changes(self.valid_directory)
        
        # Check that the output is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)
    
    def test_count_mod_changes_columns(self):
 
        df = alfred.count_mod_changes(self.valid_directory)
        
        # Check that the DataFrame has 4 columns
        self.assertEqual(df.shape[1], 4)
    
    def test_count_mod_changes_rows_divisible_by_16(self):
 
        df = alfred.count_mod_changes(self.valid_directory)
        # Check that the number of rows is divisible by 16
        self.assertEqual(df.shape[0] % 16, 0)     
    def tearDown(self):
        
        pass
        
class TestVisualiseModChanges(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')

    def test_visualise_mod_changes_output(self):
        chart = alfred.visualise_mod_changes(self.valid_directory)
        self.assertIsInstance(chart, alt.Chart)
        
    def tearDown(self):
        
        pass
class TestModChangeStatistics(unittest.TestCase):

    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.empty_data_directory = os.path.join(data_path, 'sorted_data/')
   
    def test_mod_change_statistics_output(self):
        ax= alfred.mod_change_statistics(self.valid_directory)
        self.assertIsInstance(ax, plt.Axes)

    def test_mod_change_statistics_empty_data_directory(self):
        ax = alfred.mod_change_statistics(self.empty_data_directory)
        # Check if the chart is blank (no data)
        has_data = any([line.get_data()[0].size > 0 for line in ax.get_lines()])
        self.assertFalse(has_data, "The chart is not blank")

    def tearDown(self):
        
        pass
class TestFindReplacedModules(unittest.TestCase):

    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.empty_data_directory = os.path.join(data_path, 'sorted_data/')
    
    def testfind_replaced_mod_dict_is_made(self):
 
        result = alfred.find_replaced_modules(self.valid_directory)
        
        # Check if the returned object is a dictionary
        self.assertIsInstance(result, dict, "The returned object is not a dictionary")

    def test_replaced_mod_dict_is_empty(self):
        # Call the function with an empty directory
        result = alfred.find_replaced_modules(self.empty_data_directory)
        
        # Check if the returned dictionary is empty
        self.assertEqual(len(result), 0, "The returned dictionary is not empty")
    def tearDown(self):
        
        pass
        
class TestSwappedModDataframes(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'vis_buses/')
        self.serial_num = '0039-1429-03B-402335-00710'
        self.characteristics = ['cell voltages', 'balancers', 'temperatures', 'module voltages']
   
    def test_return_type(self):
        for characteristic in self.characteristics:
            with self.subTest(characteristic=characteristic):
                result = alfred.swapped_mod_dataframes(self.valid_directory, self.serial_num, characteristic)
                # Check if the returned object is a list
                self.assertIsInstance(result, list, f"The returned object is not a list for characteristic: {characteristic}")
    def tearDown(self):
        
        pass
        
if __name__ == '__main__':
    unittest.main()