from client import *

class EventDetail(unittest.TestCase):
    def setUp(self):
        url = 'http://139.199.132.220:9000/event/api/get_eventdetail/'
        method = Method.GET
        type = Type.URL_ENCODE
        self.client = Client(url=url, method=method, type=type)

    '''获取会议详细信息接口'''
    def test_eventdetail01(self):
        '''会议详细信息接口-正向流程'''
        # token = '75ff30521dd7bafb48e07cf7e0a0b564dd8896a4'
        # uid = 1
        token = self.client.value('token')
        uid = self.client.value('uid')
        Cookie = 'token=%s;uid=%s' % (token, uid)

        self.eid = self.client.db_values('select id from api_event')[0][0]
        data = {'id': str(self.eid)}

        self.client.set_headers({'Cookie': Cookie})
        self.client.set_data(data)
        self.client.add_sign()
        self.client.send()
        print(self.client.res_json)
        self.client.check_status_code(200)
        self.client.check_jsonNode_equal('$.error_code', 0)
        self.client.check_jsonNode_equal('$.event_detail.id', str(self.eid))