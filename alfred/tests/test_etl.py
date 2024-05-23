import os
import tempfile
import unittest
import zipfile

import pandas as pd

import alfred

data_path = os.path.join(alfred.__path__[0], 'data')

class Test_find_directory(unittest.TestCase):
   
    def setUp(self):
            """
            Unpack the zip
            """
            self.temp_dir = tempfile.mktemp()
    
            with zipfile.ZipFile(os.path.join(data_path, "test_data.zip")) as zip_ref:
                zip_ref.extractall(self.temp_dir)
    
    def test_find_directory_ends_with_forward_slash(self):
        directory = find_directory()

        self.assertTrue(directory.endswith('/'), "Directory does not end with a forward slash")



     def tearDown(self):
            """
            Remove .csv files
            """
            for file_name in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
# remove test dir
        os.rmdir(self.temp_dir)

# tests on alfred.etl
class test_ETL(unittest.TestCase):

    def setUp(self):
        """
        Unpack the zip
        """
        self.temp_dir = tempfile.mktemp()

        with zipfile.ZipFile(os.path.join(data_path, "test_data.zip")) as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def test_grab_csv(self):
        """
        Testing the sort functions or some other description here.
        """

        # find the csvs extracted from the zip
        result = alfred.etl.grab_csv(self.temp_dir)
        assert result == ['14H0221_ProfileData_20180403084955(2).csv', '14H0221_ProfileData_20171027081821(2).csv', '0014_ProfileData_20161201100821(2).csv', '13J0014_ProfileData_20180802094539(2).csv', '0014_ProfileData_20161004063626(2).csv', '14H0221_ProfileData_20171005100537(3).csv', '0014_ProfileData_20170207092734(2).csv', '_ProfileData_20180425073946(2).csv', '14F0154_ProfileData_20171116125343(2).csv', '13J0014_ProfileData_20180801084738(2).csv', '_ProfileData_20180508065837(2).csv', '14B0059_ProfileData_20180403061303(2).csv', '0014_ProfileData_20160727062458(2).csv']

        # this should return an empty list
        result = alfred.etl.grab_csv(data_path)
        assert result == []

    def tearDown(self):
        """
        Remove .csv files
        """
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # remove test dir
        os.rmdir(self.temp_dir)

