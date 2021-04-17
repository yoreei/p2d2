import unittest

# raise unittest.SkipTest("not implemented yet")


# @unittest.skip('comments_for_skipping_unit_tests')
class DataFrameTest(unittest.TestCase):
    def setUp(self):
        self.testcode = 1
        self.skipTest('module not tested')

    def tearDown(self):
        del self.testcode

    def test_procedural_representation(self):
        self.assertEquals(True,False)


