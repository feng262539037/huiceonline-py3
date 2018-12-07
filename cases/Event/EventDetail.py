from client import *

class EventDetail(unittest.TestCase):
    '''获取会议详细信息接口'''
    def setUp(self):
        url = 'http://139.199.132.220:9000/event/api/get_eventdetail/'
        method = Method.GET
        content_type = Content_Type.URL_ENCODE
        self.client = Client(url=url, method=method, content_type=content_type)
        self.token = self.client.value('token')
        self.uid = self.client.value('uid')
        self.eid = self.client.db_values('select id from api_event')[0][0]

    def test_eventdetail01(self):
        '''会议详细信息接口-正向流程'''
        # token = '75ff30521dd7bafb48e07cf7e0a0b564dd8896a4'
        # uid = 1

        Cookie = 'token=%s;uid=%s' % (self.token, self.uid)

        data = {'id': str(self.eid)}

        self.client.set_headers({'Cookie': Cookie})
        self.client.set_data(data)
        self.client.add_sign()
        self.client.send()
        print(self.client.res_json)
        self.client.check_status_code(200)
        self.client.check_jsonNode_equal('$.error_code', 0)
        self.client.check_jsonNode_equal('$.event_detail.id', str(self.eid))