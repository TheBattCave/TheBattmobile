import os
import tempfile
import unittest
import zipfile
import pandas as pd
import numpy as np
import shutil
import alfred

data_path = os.path.join(alfred.__path__[0], 'data')

class TestFindDirectory(unittest.TestCase):
    
    def setUp(self):
        """
        Unpack the zip
        """
        self.temp_dir = tempfile.mkdtemp()

        with zipfile.ZipFile(os.path.join(data_path, "test_data.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def test_find_directory_ends_with_forward_slash(self):
        directory = alfred.find_directory()
        self.assertTrue(directory.endswith('/'), "Directory does not end with a forward slash")

    def tearDown(self):
        """
        Remove .csv files and temp directory
        """
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)


class TestGrabCSV(unittest.TestCase):

    def setUp(self):
        """
        Unpack the zip
        """
        self.temp_dir = tempfile.mkdtemp()

        with zipfile.ZipFile(os.path.join(data_path, "test_data.zip"), 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def test_grab_csv(self):
        """
        Testing the grab_csv function.
        """
        # find the csvs extracted from the zip
        result = alfred.grab_csv(self.temp_dir)
        expected_result = [
            '14F0154_ProfileData_20171116125343(2).csv', 
            '14B0059_ProfileData_20180403061303(2).csv', 
            '14H0221_ProfileData_20171005100537(3).csv',
            '14H0221_ProfileData_20171027081821(2).csv',
            '14H0221_ProfileData_20180403084955(2).csv',
            '0014_ProfileData_20160727062458(2).csv',
            '0014_ProfileData_20161004063626(2).csv',
            '0014_ProfileData_20161201100821(2).csv',
            '0014_ProfileData_20170207092734(2).csv',
            '13J0014_ProfileData_20180801084738(2).csv',
            '13J0014_ProfileData_20180802094539(2).csv',
            '_ProfileData_20180425073946(2).csv',
            '_ProfileData_20180508065837(2).csv'
        ]
        # sort both the actual result and the expected result
        result.sort()
        expected_result.sort()
       
        self.assertListEqual(result, expected_result)

        # this should return an empty list
        result = alfred.grab_csv(data_path)
        self.assertListEqual(result, [])

    def tearDown(self):
        """
        Remove .csv files and temp directory
        """
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)

 


class TestGroupFiles(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'unsorted_test_data')
    
    def test_group_file_creates_subdirectories(self):
            alfred.group_files(self.valid_directory)
    
            # Define the expected subdirectory names
            expected_subdirs = [
                "bus_0039141908140233500710",
                "bus_0039142006m40233500710",
                "bus_0039142903b40233500710",
                "bus_0039151006940233500710",
                "incomplete"
            ]
            for subdir_name in expected_subdirs:
                subdir_path = os.path.join(self.valid_directory, subdir_name)
                # Check if the subdirectory exists
                self.assertTrue(os.path.exists(subdir_path))
                # Check if it's a directory
                self.assertTrue(os.path.isdir(subdir_path))
    def test_bus_0039141908140233500710(self):
        alfred.group_files(self.valid_directory)
        subdir_name = "bus_0039141908140233500710"
        subdir_path = os.path.join(self.valid_directory, subdir_name)
        self.assertTrue(os.path.exists(subdir_path))
        self.assertTrue(os.path.isdir(subdir_path))
        expected_files = [
            '14F0154_ProfileData_20171116125343(2).csv'
        ]
        for file_name in expected_files:
            file_path = os.path.join(subdir_path, file_name)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))

    def test_bus_0039142006m40233500710(self):
        alfred.group_files(self.valid_directory)
        subdir_name = "bus_0039142006m40233500710"
        subdir_path = os.path.join(self.valid_directory, subdir_name)
        self.assertTrue(os.path.exists(subdir_path))
        self.assertTrue(os.path.isdir(subdir_path))
        expected_files = [
            '14B0059_ProfileData_20180403061303(2).csv'
        ]
        for file_name in expected_files:
            file_path = os.path.join(subdir_path, file_name)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))

    def test_bus_0039142903b40233500710(self):
        alfred.group_files(self.valid_directory)
        subdir_name = "bus_0039142903b40233500710"
        subdir_path = os.path.join(self.valid_directory, subdir_name)
        self.assertTrue(os.path.exists(subdir_path))
        self.assertTrue(os.path.isdir(subdir_path))
        expected_files = [
            '14H0221_ProfileData_20171005100537(3).csv',
            '14H0221_ProfileData_20171027081821(2).csv',
            '14H0221_ProfileData_20180403084955(2).csv'
        ]
        for file_name in expected_files:
            file_path = os.path.join(subdir_path, file_name)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))

    def test_bus_0039151006940233500710(self):
        alfred.group_files(self.valid_directory)
        subdir_name = "bus_0039151006940233500710"
        subdir_path = os.path.join(self.valid_directory, subdir_name)
        self.assertTrue(os.path.exists(subdir_path))
        self.assertTrue(os.path.isdir(subdir_path))
        expected_files = [
            '0014_ProfileData_20160727062458(2).csv',
            '0014_ProfileData_20161004063626(2).csv',
            '0014_ProfileData_20161201100821(2).csv',
            '0014_ProfileData_20170207092734(2).csv',
            '13J0014_ProfileData_20180801084738(2).csv',
            '13J0014_ProfileData_20180802094539(2).csv'
        ]
        for file_name in expected_files:
            file_path = os.path.join(subdir_path, file_name)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))

    def test_incomplete(self):
        alfred.group_files(self.valid_directory)
        subdir_name = "incomplete"
        subdir_path = os.path.join(self.valid_directory, subdir_name)
        self.assertTrue(os.path.exists(subdir_path))
        self.assertTrue(os.path.isdir(subdir_path))
        expected_files = [
            '_ProfileData_20180425073946(2).csv',
            '_ProfileData_20180508065837(2).csv'
        ]
        for file_name in expected_files:
            file_path = os.path.join(subdir_path, file_name)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))

    def tearDown(self):
         pass


class TestCountBusFile(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'unsorted_test_data')    
    
    def test_count_bus_file(self):
        count = alfred.count_bus_file(self.valid_directory)
        self.assertEqual(count, 4)
        
    def test_count_bus_file_returns_integer(self):
        count = alfred.count_bus_file(self.valid_directory)
        self.assertIsInstance(count, int)   
        
    def tearDown(self):
         pass
        
class TestSortBusByDate(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'unsorted_test_data/')  

    def test_sort_data_by_date_returns_dataframe(self):
        bus_num = 'bus_0039151006940233500710/'
        df = alfred.sort_bus_by_date(self.valid_directory, bus_num)
        self.assertIsInstance(df, pd.DataFrame)


    def test_sort_data_by_date_dataframe_shape(self):
        bus_num = 'bus_0039151006940233500710/'
        bus_directory = os.path.join(self.valid_directory, bus_num)
        csv_files = [f for f in os.listdir(bus_directory) if f.endswith('.csv')]
        expected_rows = len(csv_files)  
        df = alfred.sort_bus_by_date(self.valid_directory, bus_num)
        self.assertEqual(df.shape[0], expected_rows)
        self.assertEqual(df.shape[1], 2)
        
    def tearDown(self):
         pass
        
class TestCompareFileMods(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'unsorted_test_data/')  
        self.invalid_directory = os.path.join(data_path, 'unzipped_test_data/')  
  
    def test_compare_file_mods_returns_dictionary(self):
        result = alfred.compare_file_mods(self.valid_directory)
        self.assertIsInstance(result, dict)

    def test_compare_file_mods_dictionary_length(self):
        result = alfred.compare_file_mods(self.valid_directory)
        subdirs = [d for d in os.listdir(self.valid_directory) if os.path.isdir(os.path.join(self.valid_directory, d))]
        self.assertEqual(len(result), len(subdirs)-1) # -1 to account for the incomplete subdirectory

    def test_compare_file_mods_unsorted_test_data_returns_empty_dict(self):
        result = alfred.compare_file_mods(self.invalid_directory)
        self.assertEqual(result, {})

    def tearDown(self):
         pass

class TestFilterFalseMod(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'unsorted_test_data/')
    
    def test_filter_false_module_returns_numpy_array(self):
        result = alfred.filter_false_module(self.valid_directory)
        self.assertIsInstance(result, np.ndarray)

    def test_filter_false_module_contains_expected_entries(self):
        expected_entries = ['bus_0039142903b40233500710',
                            'bus_0039151006940233500710']
        result = alfred.filter_false_module(self.valid_directory)
        for entry in expected_entries:
            self.assertIn(entry, result)
            
    def tearDown(self):
         pass       
        
class TestMoveFalseBus(unittest.TestCase):
    def setUp(self):
        self.valid_directory = os.path.join(data_path, 'sorted_test_data/')
    
    def test_move_false_bus_creates_vis_buses_directory(self):
        alfred.move_false_bus(self.valid_directory)
        # Check if 'vis_buses' directory is created
        vis_buses_dir = os.path.join(self.valid_directory, 'vis_buses')
        self.assertTrue(os.path.exists(vis_buses_dir))
        self.assertTrue(os.path.isdir(vis_buses_dir))

    def test_move_false_bus_moves_correct_directories(self):
        alfred.move_false_bus(self.valid_directory)
        # Check if 'bus_0039142903b40233500710' and 'bus_0039151006940233500710' are in 'vis_buses'
        vis_buses_dir = os.path.join(self.valid_directory, 'vis_buses')
        expected_directories = ['bus_0039142903b40233500710', 'bus_0039151006940233500710']
        for directory in expected_directories:
            dir_path = os.path.join(vis_buses_dir, directory)
            self.assertTrue(os.path.exists(dir_path))
            self.assertTrue(os.path.isdir(dir_path))

    def test_move_false_bus_no_other_directories_in_vis_buses(self):
        alfred.move_false_bus(self.valid_directory)
        # Check if there are no other directories besides 'bus_0039142903b40233500710' and 'bus_0039151006940233500710' in 'vis_buses'
        vis_buses_dir = os.path.join(self.valid_directory, 'vis_buses')
        expected_directories = ['bus_0039142903b40233500710', 'bus_0039151006940233500710']
        for item in os.listdir(vis_buses_dir):
            if os.path.isdir(os.path.join(vis_buses_dir, item)):
                self.assertIn(item, expected_directories)

    def tearDown(self):
         pass     
        
# class TestUnpackInteractive(unittest.TestCase):
#     def setUp(self):
#         self.valid_directory = os.path.join(data_path, 'sorted_test_data/')
#         raw_data_folder_name = 'alfred/' + 'data/'
#         zip_filename = 'test_data.zip'
        
#     def test_unpack_interactive_creates_sorted_data_directory(self):
#         alfred.etl.unpack_interactive()
#         # Check if 'sorted_data' directory is created
#         sorted_data_dir = os.path.join(self.valid_directory, 'sorted_data')
#         self.assertTrue(os.path.exists(sorted_data_dir))
#         self.assertTrue(os.path.isdir(sorted_data_dir))

#     def test_unpack_interactive_creates_all_buses_directory(self):
#         alfred.etl.unpack_interactive()
#         # Check if 'all_buses' directory is created
#         all_buses_dir = os.path.join(self.valid_directory, 'all_buses')
#         self.assertTrue(os.path.exists(all_buses_dir))
#         self.assertTrue(os.path.isdir(all_buses_dir)) 
#     def tearDown(self):
#          pass   
        
if __name__ == '__main__':
    unittest.main()
