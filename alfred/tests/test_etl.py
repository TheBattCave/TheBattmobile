import os
import tempfile
import unittest
import zipfile
import pandas as pd
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
        directory = alfred.etl.find_directory()
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
        result = alfred.etl.grab_csv(self.temp_dir)
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
        result = alfred.etl.grab_csv(data_path)
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

from alfred.etl import group_files  

class TestGroupFiles(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.test_data_dir = os.path.join(self.test_dir, 'alfred/unsorted_test_data')
        os.makedirs(self.test_data_dir)

        # Add test CSV file
        self.test_file_name = '14F0154_ProfileData_20171116125343(2).csv'
        self.test_file_path = os.path.join(self.test_data_dir, self.test_file_name)
        with open(self.test_file_path, 'w') as f:
            f.write('test data')
            
    def test_group_files(self):
        # Call the group_files function
        group_files(self.test_data_dir)

        # Check if the expected folder and file are created
        expected_dir = os.path.join(self.test_data_dir, 'bus_0039141908140233500710')
        expected_file = os.path.join(expected_dir, self.test_file_name)
        
        self.assertTrue(os.path.isdir(expected_dir), f"Expected directory {expected_dir} does not exist.")
        self.assertTrue(os.path.isfile(expected_file), f"Expected file {expected_file} does not exist.")
    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)


if __name__ == '__main__':
    unittest.main()
