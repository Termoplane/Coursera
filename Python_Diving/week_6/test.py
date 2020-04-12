
class TestFactorize(unittest.TestCase):
    """
    Test for function factorize(x) that takes an int as an argument
    and return its factors
    """

    def test_wrong_types_raise_exception(self):
        self.cases = ['string', 1.5]
        for x in self.cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)
    
    def test_negative(self):
        self.cases = [-1, -10, -100]
        for x in self.cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)
    
    def test_zero_and_one_cases(self):
        self.cases = [0, 1]
        for x in self.cases:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_simple_numbers(self):
        self.cases = [3, 13, 29]
        for x in self.cases:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
      for x, answer in ((6, (2,3)), (26, (2,13)), (121, (11,11))):
        with self.subTest(x=x):
          self.assertEqual(factorize(x), answer)

    def test_many_multipliers(self):
      for x, answer in ((1001, (7, 11, 13)), (9699690,  (2, 3, 5, 7, 11, 13, 17, 19))):
        with self.subTest(x=x):
          self.assertEqual(factorize(x), answer)