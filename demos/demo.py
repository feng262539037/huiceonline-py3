import unittest

class MyTest(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def test_case01(self):
        print('test_case01')

    def test_case02(self):
        print('test_case02')

    def tearDown(self):
        print('tearDown')

class MyTest2(unittest.TestCase):
    def test_case03(self):
        print('test_case03')

if __name__ == '__main__':
    unittest.main()

# setUp
# test_case01
# tearDown
# setUp
# test_case02
# tearDown
# test_case03


