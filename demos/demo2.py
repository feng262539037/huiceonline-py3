#coding:utf-8
import unittest

class MyTest(unittest.TestCase):
    #起什么名字都可以，普遍叫self，代表当前对象自身
    #setUpClass方法是在MyTest这个类运行前执行
    #但是这个类还没有对象
    #如果不加@classmethod，此方法是成员方法，永远运行不到
    #所以把此方法设置为类方法，添加@classmethod
    @classmethod
    def setUpClass(self):
        print('setUpClass')

    @classmethod
    def tearDownClass(self):
        print('tearDownClass')

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

# setUpClass
# setUp
# test_case01
# tearDown
# setUp
# test_case02
# tearDown
# tearDownClass
# test_case03

