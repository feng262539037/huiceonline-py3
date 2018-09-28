import unittest
import HTMLTestReportCN
import sys
import time
import shutil
import pymysql
import client

if __name__ == '__main__':
    #方式一：构造测试集合
    # from cases.AAARegister import Register
    # from cases.Event import AddEvent, EventDetail
    # #创建suite套件
    # suite = unittest.TestSuite()
    # #如果想用文件里的类：文件名.类名（方法名）
    # suite.addTest(Register.Register("test_register01"))
    # suite.addTest(Register.Register("test_register02"))
    # suite.addTest(AddEvent.AddEvent("test_addevent01"))
    # suite.addTest(EventDetail.EventDetail("test_eventdetail01"))
    # unittest.TextTestRunner().run(suite)

    # #无法在jenkins上集成:push报告有问题
    # # print(sys.argv[0]) #F:\\ITest-huiceonline-2\\cases\\run.py 获取当前run.py路径下
    # start_dir = sys.argv[0] + '\\..\\cases'
    # # 方式二：使用discover：把冒烟测试用例写在一个文件夹里，把基本功能测试用例写在一个文件夹里等等
    # # 创建suite套件：指定测试用例的路径
    # suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='*.py')
    # # 获取当前时间
    # time = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    # # 在report文件夹中生成报告
    # path = sys.argv[0] + '\\..\\report\\'+ time +'.html'
    # fp = open(path, 'wb')
    # # 运行测试套件
    # HTMLTestReportCN.HTMLTestRunner(stream=fp, tester='QA', title='接口测试报告').run(suite)
    # # fp.close()
    # # 把报告拷贝一份
    # shutil.copyfile(path, sys.argv[0] + '\\..\\report\\report.html')

    #方式三：读取xml文件，运用方式一加载测试用例：可以指定顺序，指定跑哪些用例。无法在jenkins运行
    from xml.etree import ElementTree as ET
    suite = unittest.TestSuite()
    #解析xml文件：把xml读成树结构
    #（路径）
    et = ET.parse('./config.xml')
    #返回列表，找回cases下所有的子节点
    #（节点名） ./代表project根节点
    list = et.findall('./cases/*')
    for i in list:
        directory_name = i.tag.split('-')[0]
        class_name = i.tag.split('-')[1]
        method_name = i.tag.split('-')[-1]
        #exec：把字符串当成代码执行！！！
        exec('from cases.%s import %s' % (directory_name, class_name))
        exec("suite.addTest(%s.%s('test_%s'))" % (class_name, class_name, method_name))
    time = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    path = sys.argv[0] + '\\..\\report\\' + time + '.html'
    fp = open(path, 'wb')
    HTMLTestReportCN.HTMLTestRunner(stream=fp, tester='QA', title='接口测试报告').run(suite)
    fp.close()
    shutil.copyfile(path, sys.argv[0] + '\\..\\report\\report.html')

    #简化版（方式二）：可集成jenkins，运行所有测试用例
    # start_dir = sys.argv[0] + '\\..\\cases\\'
    # suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='*.py')
    # fp = open(sys.argv[0] + '\\..\\report.html', 'wb')
    # HTMLTestReportCN.HTMLTestRunner(stream=fp).run(suite)

    # database = {}
    # et = ET.parse('./config.xml')
    # data_config_list = et.findall('./database/*')
    # for d in data_config_list:
    #     database[d.tag] = d.text
    # #for循环正常执行后，才会执行else
    # else:
    #     client.Client.DB = pymysql.connect(host=database.get('host'), user=database.get('user'), password=database.get('password'), db=database.get('db'))


