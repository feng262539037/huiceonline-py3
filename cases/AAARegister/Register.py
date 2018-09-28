from client import *
from util import *

class Register(unittest.TestCase):
    #url地址，方法类型，Content-Type
    def setUp(self):
        url = 'http://139.199.132.220:9000/event/api/register/'
        method = Method.POST
        type = Type.URL_ENCODE
        #调用Client类，创建对象！！！！！
        #如果不加self，没法把setUp中的clinet传给下面的方法
        #用了self.client，在这个类中，client都可以用
        self.client = Client(url=url, method=method, type=type)

    #添加参数，发送，添加检查点
    '''登陆接口'''
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
        #注意这里要转int类型，否则报错
        self.client.check_db2('$.uid', "SELECT id fROM auth_user WHERE username = 'huice'")

        #第一个变量名
        #第二个是值
        #一定要按照transmit函数的先后顺序！！！！！
        self.client.transmit('token', self.client.res_json.get('token'))
        self.client.transmit('uid', self.client.res_json.get('uid'))

    def test_register02(self):
        '''密码错误'''
        username = 'huice'
        password = base64_encode('123huicehuice!@')
        data = {'username': username, 'password': password}

        self.client.set_data(data)
        self.client.send()
        self.client.check_status_code(200)
        self.client.check_jsonNode_equal('$.error_code', 10000)
