import pandas as pd
import sys
import unittest

from pathlib import Path

sys.path.append(str(Path("app/code").resolve()))

import library as l

class TestOperations(unittest.TestCase):
    def test_dataEnrich(self):
        test_data = {"Book checkout":["01-01-2026"],
                     "Book Returned":["01-02-2026"]}
        test_result = {"Book checkout":["01-01-2026"],
                       "Book Returned":["01-02-2026"],
                       "days_between":31}
        df_test = pd.DataFrame(test_data)
        df_result = pd.DataFrame(test_result)
        df_result["days_between"] = df_result["days_between"].astype('Int64')
        cols = ["Book checkout", "Book Returned"]
        df_test = l.dates(df_test,cols)
        df_result = l.dates(df_result,cols)
        df_test = l.dataEnrich(df_test)
        pd.testing.assert_frame_equal(df_test, df_result)

    def test_duplicates(self):
        test_data = {"Name":["James","James","Bob"],
                     "ID":[1,1,2]}
        test_result = {"Name":["James","Bob"],
                     "ID":[1,2]}
        df_test = pd.DataFrame(test_data)
        df_result = pd.DataFrame(test_result)
        df_test = l.duplicates(df_test)
        pd.testing.assert_frame_equal(df_test, df_result)

    def test_float_to_int(self):
        test_data = {"Name":["James","Bob"],
                     "ID":[1.0,2.0]}
        test_result = {"Name":["James","Bob"],
                     "ID":[1,2]}
        df_test = pd.DataFrame(test_data)
        df_result = pd.DataFrame(test_result)
        df_result["ID"] = df_result["ID"].astype('Int64')
        df_test = l.float_to_int(df_test,["ID"])
        pd.testing.assert_frame_equal(df_test, df_result)

    def test_drop_na(self):
        test_data = {"Name":["James","Bob",pd.NA]}
        test_result = {"Name":["James","Bob"]}
        df_test = pd.DataFrame(test_data)
        df_result = pd.DataFrame(test_result)
        df_test = l.drop_na(df_test)
        pd.testing.assert_frame_equal(df_test, df_result)

if __name__ == "__main__":
    unittest.main()