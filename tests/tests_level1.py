import unittest
from calc import Calculator

class TestOperations(unittest.TestCase):
    def test_sum(self):
        calculator = Calculator(8,2)
        self.assertEqual(calculator.get_sum(), 10, "The answer was not 10")

    def test_product(self):
        calculator = Calculator(5,2)
        self.assertEqual(calculator.get_product(), 10, "The answer was not 10")

    def test_difference(self):
        calculator = Calculator(9,6)
        self.assertEqual(calculator.get_difference(), 3, "The answer was not 3")

    def test_quotient(self):
        calculator = Calculator(9,3)
        self.assertEqual(calculator.get_quotient(), 3, "The answer was not 3")

if __name__ == "__main__":
    unittest.main()