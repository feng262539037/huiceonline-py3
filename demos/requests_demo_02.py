#coding:utf-8

#get:有参数
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getSupportCityString'
# method = Method.GET
# client1 = Client(url=url, method=method)
# data = {'theRegionCode':'3117'}
# client1.set_data(data)
# client1.send()
# print client1.res_text

#post
#urlencoded
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getSupportCityString'
# method = Method.POST
# type = Type.URL_ENCODE
# client2 = Client(url=url,method=method,type=type)
# data = {'theRegionCode':'3117'}
# client2.set_data(data)
# client2.send()
# print client2.res_text

#post
#raw:xml---webservice或soap
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx'
# method = Method.POST
# type = Type.XML
# client3 = Client(url=url, method=method,type=type)
# xml = '''<?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <getSupportCityString xmlns="http://WebXml.com.cn/">
#       <theRegionCode>3117</theRegionCode>
#     </getSupportCityString>
#   </soap:Body>
# </soap:Envelope>
# '''
# client3.set_data({'xml': xml})
# client3.send()
# print client3.res_text

#post
#json
# url = 'http://139.199.132.220:9000/event/weather/getWeather/'
# method = Method.POST
# type = Type.JSON
# client4 = Client(url=url, method=method, type=type)
# data = {'theCityCode': 1}
# client4.set_data(data)
# client4.send()
# print(client4.res_text)
# print(client4.res_json)
# print client4.res_headers
# print client4.res_status_code
# print client4.res_times
# client4.check_status_code(200)
# client4.check_res_time_less(200)
# client4.check_equal(client4.res_json.get('error_code'), 0)
