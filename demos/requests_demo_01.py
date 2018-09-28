#coding:utf-8
import requests
from xml.etree import ElementTree as ET
import jsonpath
import json

#GET无参
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getRegionProvince'
# reponse = requests.get(url=url)
# print(reponse.status_code)
# print(reponse.text)

#GET有参
#响应是xml，用python去解析
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getSupportCityString'
# params_dic = {'theRegionCode': '3117'}
# response = requests.get(url=url, params=params_dic)
# # print(type(response.text))  #unicode编码，字符串
# # print(response.text)
# #从xml字符串(response.text)中解析它，转成elementtree
# print(ET.fromstring(response.text).find('.//{http://WebXml.com.cn/}string').text)
# #findall返回list。可以校验长度
# print(len(ET.fromstring(response.text).findall('.//{http://WebXml.com.cn/}string')))

#GET 下载接口
# url = 'http://139.199.132.220:9000/event/index/export/'
# response = requests.get(url=url)
# #显示二进制流格式，普通文本用text还行，但是遇到其他，比如图片就有问题了，看不懂
# #下载建议用content
# #执行顺序：打开文件形成流，给变量f。当执行完with语句块，自动关闭流
# with open('./user.csv', 'wb') as f:
#     for i in response.iter_content(128):
#         f.write(i)

#POST
#x-www-form-urlencoded形式
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx/getSupportCityString'
# headers_dic = {'Content-Type': 'application/x-www-form-urlencoded'}
# data_dic = {'theRegionCode': '3117'}
# response = requests.post(url = url, headers = headers_dic, data = data_dic)
# print(response.text)

#POST
#form表单
#这种形式不要指定Content-Type，如果指定反而会报错
# url='http://139.199.132.220:9000/event/index/submit_info/'
# data_dic = {'username': '19430904', 'email':'1943@163.com', 'password': '123456'}
# response = requests.post(url = url, data = data_dic)
# print(response.text)

#POST
#form表单，可以上传二进制文件。而urlencoded不能上传二进制文件,同时可以上传多个文件
#上传二进制文件
# url='http://139.199.132.220:9000/event/index/uploadFile/'
# data_dic = {'myfile': open('F:\\discuz.jmx', 'rb')}
# response = requests.post(url = url, files = data_dic)
# print(response.text)

#POST
#raw:xml---webservice或soap
#普通字符串
# url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx'
# headers_dic = {'Content-Type': 'text/xml'}
# data_str = '''<?xml version="1.0" encoding="utf-8"?>
# <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
#   <soap:Body>
#     <getSupportCityString xmlns="http://WebXml.com.cn/">
#       <theRegionCode>3117</theRegionCode>
#     </getSupportCityString>
#   </soap:Body>
# </soap:Envelope>
# '''
# response = requests.post(url=url, headers = headers_dic, data = data_str)
# print(response.text)

#POST
#raw:json
#方式一:把字典转成json字符串（data=json.dumps(params_dic)）
# url = 'http://139.199.132.220:9000/event/weather/getWeather/'
# headers_dic = {'Content-Type': 'application/json'}
# data_dic = {'theCityCode': 1}
# response = requests.post(url=url, headers = headers_dic, data=json.dumps(data_dic))
# print response.status_code
# print response.text

#POST
#raw:json
#方式二：直接传入json字符串（json = params_dic）
url = 'http://139.199.132.220:9000/event/weather/getWeather/'
headers_dic = {'Content-Type': 'application/json'}
data_dic = {'theCityCode': 1}
response = requests.post(url=url, headers = headers_dic, json=data_dic)
# print('type(response.text) =%s' %type(response.text))  #unicode
# print response.text
# print response.status_code
# print response.headers
# print response.cookies
# #print('type(response.json) =%s' %type(response.json()))  #dict
# print(response.json())
# # print response.json()['name']
# #下面的，如果找不到，返回None，而不会报错
# print(response.json().get('name'))
# #print response.json().get('error_code')

#解析json
# $ 代表根路径
# . 代表下一层路径
print(response.json())
print(jsonpath.jsonpath(response.json(), '$.name')[0]) #返回列表，有可能返回多个，根据列表的索引取第一项

#请求响应时间,毫秒
#round,四舍五入
#int,转int类型
# print(int(round(response.elapsed.total_seconds()*1000)))






