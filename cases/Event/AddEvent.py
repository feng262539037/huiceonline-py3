from client import *

class AddEvent(unittest.TestCase):
    def setUp(self):
        url = 'http://139.199.132.220:9000/event/api/add_event/'
        method = Method.POST
        type = Type.URL_ENCODE
        self.client = Client(url=url, method=method, type=type)

    def tearDown(self):
        self.client.db_values("delete from api_event WHERE title = '接口自动迭代16'")

    '''添加会议接口'''
    def test_addevent01(self):
        '''添加会议'''
        # token = '75ff30521dd7bafb48e07cf7e0a0b564dd8896a4'
        # uid = 1
        token = self.client.value('token')
        uid = self.client.value('uid')
        Cookie = 'token=%s;uid=%s' % (token, uid)

        title = '接口自动迭代16'
        address = '北京'
        time = '2020-10-7 10:00:00'
        data = {'title': title, 'address': address, 'time': time}

        self.client.set_headers({'Cookie': Cookie})
        self.client.set_data(data)
        self.client.add_sign()
        self.client.send()
        print(self.client.res_json)
        self.client.check_status_code(200)
        self.client.check_jsonNode_equal('$.error_code', 0)


