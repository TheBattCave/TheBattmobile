import os
import unittest

import alfred

data_path = os.path.join(alfred.__path__[0], 'data')

# tests on alfred.etl
class test_ETL(unittest.TestCase):

    def test_sort(self):
        """
        Testing the sort functions or some other description here.
        """

        # example of reading a df from a zip using data_path above
        df = pd.read_csv(os.path.join(data_path, "test_data.zip"))
