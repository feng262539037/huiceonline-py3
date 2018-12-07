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
        directory_name = i.tag.split('-')[0] #AAARegister, AAARegister, Event,Event
        class_name = i.tag.split('-')[1]     #Register,Register,AddEvent,EventDetail
        method_name = i.tag.split('-')[-1]   #register01,register02,addevent01,eventdetail01
        #exec：把字符串当成代码执行！！！
        exec('from cases.%s import %s' % (directory_name, class_name))
        try:
            #没有数据驱动的
            exec("suite.addTest(%s.%s('test_%s'))" % (class_name, class_name, method_name))
        except ValueError:
            #有数据驱动
            # from cases.AAARegister import Register
            # #test_register02开头的，是数据驱动
            # #['test_register01', 'test_register02_1', 'test_register02_2', 'test_register02_3', 'test_register02_4']
            # print(unittest.defaultTestLoader.getTestCaseNames(Register.Register))

            li = eval('unittest.defaultTestLoader.getTestCaseNames(%s.%s)' % (class_name, class_name))
            for l in li:
                if l.startswith('test_' + method_name):
                    exec("suite.addTest(%s.%s('%s'))" % (class_name, class_name, l))

    time = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    path = sys.argv[0] + '\\..\\report\\' + time + '.html'
    #用open函数：把文件变成二进制流
    fp = open(path, 'wb')
    HTMLTestReportCN.HTMLTestRunner(stream=fp, tester='QA', title='接口测试报告').run(suite)
    fp.close()
    shutil.copyfile(path, sys.argv[0] + '\\..\\report\\report.html')

    #完整版：可集成jenkins，运行所有测试用例
    # start_dir = sys.argv[0] + '\\..\\cases\\'
    # suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='*.py')
    # time = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    # path = sys.argv[0] + '\\..\\report\\' + time + '.html'
    # #用open函数：把文件变成二进制流
    # fp = open(path, 'wb')
    # HTMLTestReportCN.HTMLTestRunner(stream=fp, tester='QA', title='接口测试报告').run(suite)
    # fp.close()
    # shutil.copyfile(path, sys.argv[0] + '\\..\\report\\report.html')

    #最终简化版
    # start_dir = sys.argv[0] + '\\..\\cases\\'
    # suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='*.py')
    # path = sys.argv[0] + '\\..\\report.html'
    # fp = open(path, 'wb')
    # HTMLTestReportCN.HTMLTestRunner(stream=fp).run(suite)

    #链接数据库
    # from xml.etree import ElementTree as ET
    # database = {}
    # et = ET.parse('./config.xml')
    # database_list = et.findall('./database/*')
    # for d in database_list:
    #     database[d.tag] = d.text
    # #for循环正常执行后，才会执行else
    # else:
    #     client.Client.DB = pymysql.connect(host=database.get('host'), user=database.get('user'), password=database.get('password'), db=database.get('db'))

