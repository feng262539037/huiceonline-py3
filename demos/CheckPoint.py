#自定义检查点 --- 原生断言 --- 封装
import unittest
class CheckPoint(unittest.TestCase):
    def __init__(self):
        self.flag = 0
        self._type_equality_funcs = {}

    def equal(self, f, s):
        try:
            self.assertEqual(f,s)
            print('断言成功：实际结果[{f}],预期结果[{s}]'.format(f=f, s=s))
        except:
            self.flag += 1
            print('断言失败：实际结果[{f}],预期结果[{s}]'.format(f=f, s=s))

    def less_then(self,f, s):
        try:
            self.assertLess(f, s)
            print('断言成功：实际结果[{f}],预期结果[<{s}]'.format(f=f, s=s))
        except:
            self.flag += 1
            print('断言失败：实际结果[{f}],预期结果[<{s}]'.format(f=f, s=s))

    def result(self):
        if self.flag > 0:
            #永远失败的断言
            raise Exception('断言失败')
