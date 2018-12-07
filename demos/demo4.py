import ddt
import unittest

# @ddt.ddt
# class A(unittest.TestCase):
#     @ddt.data(1, 2, 3, 4)
#     def test_ddt(self, value):
#         print(value)

@ddt.ddt
class A(unittest.TestCase):
    data = [{'a': 1, 'b': 2}, {'a': 2, 'b': 3}]
    @ddt.data(*data)
    #value:代表每一个字典
    def test_ddt(self, value):
        print(value.get('a')+value.get('b'))
