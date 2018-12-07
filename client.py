import requests
import unittest
import hashlib
import pymysql
import jsonpath
import util
import sys

#用类变量代替固定的数值
class Method:
    # 用大写的变量名（等号前面的）代替具体的数值
    GET = 'GET'
    POST = 'POST'

#用类变量代替固定的数值
class Content_Type:
    # 用大写的变量名（等号前面的）代替具体的数值
    FORM = 'form-data'
    URL_ENCODE = 'url_encoded'
    XML = 'text/xml'
    JSON = 'application/json'
    File = 'binary'

#类：共享很多变量，它比单独写send方法好
class Client(unittest.TestCase):
    #类变量的初始化，不能放在init中，只在整体项目运行时，运行一次。
    '''类变量'''
    VALAUES = {}

    DB = None

    # 初始化函数：用户传入的参数，不要写太多逻辑
    # self. :代表当前对象本身专属的变量！！！！！
    # content_type 选填（get没有type）
    # __:私有化变量！！！
    '''初始化函数(构造方法)，必填参数：url，method'''
    def __init__(self, url, method, content_type=0):
        self.__url = url
        self.__method = method
        self.__content_type = content_type
        # 我们的头信息是字典，所以这里也给定义为字典
        # 每次实例化Client对象，就有一个字典
        self.__headers = {}
        self.__data = {}
        self.__res = None
        #
        self._type_equality_funcs = {}

    '''设置头信息'''
    #成员方法，直接调用__init__中的headers
    #让用户用此方法给headers赋值，不能直接访问init中的headers
    #self：当前对象，所以能直接访问init中的headers
    #谁实例化client对象，self就代表谁
    def set_headers(self, headers):
        if isinstance(headers, dict):
            self.__headers = headers
        else:
            raise Exception('headers类型为字典')

    '''设置正文参数'''
    #用户统一传字典
    def set_data(self, data):
        if isinstance(data, dict):
            self.__data = data
        else:
            raise Exception('data类型为字典')

    '''添加sign'''
    def add_sign(self):
        token = None
        if self.__headers.get('Cookie'):
            list = self.__headers.get('Cookie').split(';')
            for i in list:
                if i.startswith('token='):
                    token = i.split('=')[1]
        li = []
        for k, v in self.__data.items():
            if k not in ['sign']:
                li.append(k + '=' + v)
        li.sort()
        params_str = '&'.join(li)
        md5_str = '%spara=%s' % (token, params_str)
        md5 = hashlib.md5()
        md5.update(md5_str.encode(encoding="utf-8"))
        self.__data['sign'] = md5.hexdigest()

    '''发送请求--->同时在头信息中添加Content-Type--->响应保存在self.__res对象中'''
    #0 -- post请求，无正文体，就要把参数拼接在地址栏中
    def send(self):
        #get请求
        if self.__method == 'GET':
            #get请求：无参数
            #get请求：有参数
            self.__res = requests.get(url=self.__url, params=self.__data, headers = self.__headers)
        #post请求
        elif self.__method == 'POST':
            #post请求：正文体form表单，不要指定Content-Type，如果指定反而会报错
            if self.__content_type == 'form-data':
                self.__res = requests.post(url=self.__url, data=self.__data, headers = self.__headers)
            #post请求：正文体url_encoded
            elif self.__content_type == 'url_encoded':
                #self调用成员方法
                #self有对象才能调用
                self.__headers['Content-Type'] = 'application/x-www-form-urlencoded'
                self.__res = requests.post(url=self.__url, data=self.__data, headers = self.__headers)
            # post请求：正文体xml字符串
            elif self.__content_type == 'text/xml':
                xml = self.__data.get('xml')
                if xml and isinstance(xml, str):
                    self.__headers['Content-Type'] = 'text/xml'
                    #注意这里是data=xml
                    self.__res = requests.post(url=self.__url, data=xml, headers=self.__headers)
                else:
                    raise Exception('xml正文的请求，请正确添加xml字符串：{"xml", xml}')
            # post请求：正文体json串
            elif self.__content_type == 'application/json':
                self.__headers['Content-Type'] = 'application/json'
                #用户传字典，所以这里要写json=
                self.__res = requests.post(url=self.__url, json=self.__data, headers=self.__headers)
            # post请求：上传文件，不需要指定Content-Type
            elif self.__content_type == 'binary':
                self.__res = requests.post(url=self.__url, files=self.__data, headers=self.__headers)
            #post请求：无正文体,就把参数拼在地址栏，一般不这么干
            elif self.__content_type == 0:
                self.__res = requests.post(url=self.__url, headers=self.__headers)
            else:
                raise Exception('不支持的post请求正文格式')
        #非get请求，非post请求
        else:
            raise Exception('不支持的请求方法类型')

    '''获取响应文本'''
    #@property:装饰器，用户调用def text(self)这个函数时，只需要写res_text（看起来简洁），不需要写res_text()
    #这个方法，除了self，没有其他入参
    @property
    def res_text(self):
        if self.__res:
            return self.__res.text
        else:
            return None

    '''获取响应状态码'''
    @property
    def res_status_code(self):
        if self.__res:
            return self.__res.status_code
        else:
            return None

    '''获取响应时间'''
    @property
    def res_times(self):
        if self.__res:
            return int(round(self.__res.elapsed.total_seconds() * 1000))
        else:
            return None

    '''获取响应头信息'''
    @property
    def res_headers(self):
        if self.__res:
            return self.__res.headers
        else:
            return None

    '''获取响应json串'''
    @property
    def res_json(self):
        if self.__res:
            #如果回参，不是json字符串，会报错，所以加try...except
            try:
                #把字符串转成字典
                return self.__res.json()
            except:
                print('解析json响应时错误')
                return None
        else:
            return None

    '''通过jsonpath，获取某个值'''
    '''jsonpath.jsonpath(response.json(), '$.name')[0]'''
    def json_value(self, path):
        if self.__res:
            object = jsonpath.jsonpath(self.res_json, path)
            if object:
                return object[0]
        return None

    '''断言(jsonpath)：响应值 等于 预期值？'''
    def check_jsonNode_equal(self, path, exp):
        node = self.json_value(path)
        self.assertEqual(node, exp)
        print('断言成功。实际结果：[{first}]，预期结果：[{second}]'.format(first=node, second=exp))

    '''断言：响应状态码'''
    def check_status_code(self, exp):
        #assert是python自带的断言，不太好用
        #我们用unnitest里的断言，如下
        #所以Client类继承unittest.TestCase
        #Client类中没有test开头的方法，运行时，它不会自动跑
        if self.__res:
            self.assertEqual(self.__res.status_code, exp, '响应状态码错误。实际结果[{first}]，预期结果：[{second}]'.format(first=str(self.__res.status_code), second=exp))
            print('断言成功。响应状态码的实际结果：[{first}]，预期结果：[{second}]'.format(first=str(self.__res.status_code), second=exp))
        else:
            self.assertTrue(False, '无法获取相应状态码')

    '''断言：响应时间'''
    def check_res_time_less(self, exp):
        if self.__res:
            self.assertLess(self.res_times, exp, '响应时间错误。实际结果[{first}]，预期结果：[{second}]'.format(first=str(self.res_times), second=exp))
            print('断言成功。响应时间的实际结果是：[{first}]，预期结果：[<{second}]'.format(first=str(self.res_times), second=exp))

    '''断言：响应值 等于 预期值？'''
    def check_equal(self, act, exp):
        if self.__res:
            self.assertEqual(act, exp, '响应值错误。实际结果[{first}]，预期结果：[{second}]'.format(first=act, second=exp))
            #如果用%s 就一定是字符串
            #如果用这种方法，{a}不是字符串，会自动转成字符串
            print('断言成功：实际结果[{first}],预期结果[{second}]'.format(first=act, second=exp))
        else:
            return None

    '''链接数据库--->查询 或 执行数据库语句--->断开数据库'''
    def db_values(self, sql):
        #链接数据库
        self.db = pymysql.connect(host='139.199.132.220', user='root', password='123456', db='event')
        if self.db:
            try:
                #创建游标
                cursor = self.db.cursor()
                #执行sql语句
                cursor.execute(sql)
                #提交
                self.db.commit()
                #查询所有返回数据，而为元祖
                return cursor.fetchall()
            except Exception as e:
                print(e)
                raise Exception('数据库操作失败')
            finally:
                #如果没使用db对象，close会报异常
                #所以添加if
                if self.db:
                    self.db.close()
        else:
            raise Exception('数据库链接失败')

        #优化
        # if Client.DB:
        #     try:
        #         #创建游标
        #         cursor = Client.DB.cursor()
        #         #执行sql语句
        #         cursor.execute(sql)
        #         #提交
        #         Client.DB.commit()
        #         #查询所有返回数据，而为元祖
        #         return cursor.fetchall()
        #     except Exception as e:
        #         print(e)
        #         raise Exception('数据库操作失败')
        #     finally:
        #         #如果没使用DB，close会报异常
        #         #所以添加if
        #         if Client.DB:
        #             Client.DB.close()
        # else:
        #     raise Exception('数据库链接失败')



    '''断言：数据库值 等于 接口返回值？(单个值)'''
    def check_db1(self, exp, sql):
        data = self.db_values(sql)
        if data:
            self.check_equal(exp, data[0][0])
        else:
            raise Exception('数据库取值无效：' + sql)

    '''断言(jsonpath)：接口实际的响应值 等于 数据库查询回的结果？(单个值)'''
    def check_db2(self, path, sql):
        data = self.db_values(sql)
        exp = self.json_value(path)
        if data:
            if exp:
                #接口返回的是str
                #因此，把数据库查询回的结果，转成str类型
                self.check_equal(exp, str(data[0][0]))
            else:
                self.assertFalse(True, 'json取值无效：' + path)
        else:
            self.assertFalse(True, '数据库取值无效：' + sql)

    #key：变量名
    #value：变量值
    #把值传给变量
    #如果用self.DATA:只改对象自己，对其他对象不生效
    #如果用类名.DATA：更改类变量，对所有对象生效！！！！！
    # '''传值'''
    # def transmit(self, key, value):
    #     Client.DATA[key] = value
    #
    # '''取值'''
    # def value(self, key):
    #     return Client.DATA.get(key)

    '''传值'''
    def transmit(self, name, path):
        node = self.json_value(path)
        if node:
            Client.VALAUES[name] = node
        else:
            raise Exception('未获取到要传递的值:' + path)
    '''取值'''
    def value(self, name):
        v = Client.VALAUES.get(name)
        if v:
            return v
        else:
            raise Exception('要获取的变量不存在:' + name)

