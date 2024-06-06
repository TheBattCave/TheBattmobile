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
      
if __name__ == '__main__':
    unittest.main()
