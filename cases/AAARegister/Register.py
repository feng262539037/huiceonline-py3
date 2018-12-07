from client import *
from util import *
import ddt

@ddt.ddt
class Register(unittest.TestCase):
    '''登陆接口'''
    #url地址，方法类型，Content-Type
    def setUp(self):
        url = 'http://139.199.132.220:9000/event/api/register/'
        method = Method.POST
        content_type = Content_Type.URL_ENCODE
        #调用Client类，创建对象！！！！！
        #如果不加self，没法把setUp中的clinet传给下面的方法
        #用了self.client，在这个类中，client都可以用
        self.client = Client(url=url, method=method, content_type=content_type)

    #添加参数，发送，添加检查点
    def test_register01(self):
        '''正向登录用例'''
        username = 'huice'
        password = base64_encode('123huicehuice!@#')
        data = {'username': username, 'password': password}

        self.client.set_data(data)
        self.client.send()
        print(self.client.res_json)
        self.client.check_status_code(200)
        self.client.check_jsonNode_equal('$.error_code', 0)
        self.client.check_db2('$.uid', "SELECT id fROM auth_user WHERE username = 'huice'")

        #第一个变量名
        #第二个是值
        #一定要按照transmit函数的先后顺序！！！！！
        self.client.transmit('token', '$.token')
        self.client.transmit('uid', '$.uid')

    #数据驱动
    data = [{
                "username": "huice",
                "password": "MTIzaHVpY2VodWljZSFAIw==",
                "assert": 0
            },
            {
                "username": "huice",
                "password": "aHVpY2VodWljZSFAIw==",
                "assert": 10000
            },
            {
                "username": "",
                "password": "MTIzaHVpY2VodWljZSFAIw==",
                "assert": 10001
            },
            {
                "username": "huice",
                "password": "",
                "assert": 10001
            }]

    #test_register02_数据驱动
    @ddt.data(*data)
    def test_register02(self, values):
        '''密码错误'''
        username = values.get('username')
        password = values.get('password')
        data = {'username': username, 'password': password}

        self.client.set_data(data)
        self.client.send()
        print(self.client.res_json)
        self.client.check_status_code(200)
        # self.client.check_jsonNode_equal('$.error_code', 10000)
        self.client.check_jsonNode_equal('$.error_code', values.get('assert'))
