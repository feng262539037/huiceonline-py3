import pymysql

db = pymysql.connect(host="139.199.132.220", user="root", password="123456", db="event")
cursor = db.cursor()
cursor.execute('select * from api_event')
#58：查询回来的数据的行数
# print(cursor.execute('select * from api_event'))
#查询:fetchone和fetchall
#fetchone:返回查询的第一行数据，是个元组
# print(cursor.fetchone())
#fetchall:返回查询的所有数据，是多维元组
print(cursor.fetchall())

#删除
#返回1：说明影响1行数据，但是没有删除成功
# print(cursor.execute("delete from api_event WHERE id='1877'"))
#必须执行commit，才能删除成功
# db.commit()
# db.close()

