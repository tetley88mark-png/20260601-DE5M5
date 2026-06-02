import pandas as pd
import unittest

from app.code import library as l

class TestOperations(unittest.TestCase):
    def test_dataEnrich(self):
        test_data = {"Book checkout":["2026-01-01"],
                     "Book Returned":["2026-02-01"]}
        test_result = {"Book checkout":["2026-01-01"],
                       "Book Returned":["2026-02-01"],
                       "days_between":31}
        df_test = pd.DataFrame(test_data)
        df_result = pd.DataFrame(test_result)
        l.dataEnrich(df_test)
        pd.assert_frame_equals(df_test, df_result)

if __name__ == "__main__":
    unittest.main()