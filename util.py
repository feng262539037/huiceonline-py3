import base64
import hashlib
import random
import string
import xlrd

def base64_encode(str):
    return base64.b64encode(str.encode('utf-8'))

def get_sign(token, params_dic):
    params_list = []
    params_str = ''
    for k, v in params_dic.items():
        if k not in ['sign']:
            params_list.append(k + '=' + v)
    params_list.sort()
    params_str = '&'.join(params_list)
    md5_str = '%spara=%s' % (token, params_str)
    print(md5_str)
    md5 = hashlib.md5()
    md5.update(md5_str.encode(encoding="utf-8"))
    server_sign = md5.hexdigest()
    # print 'server_sign =' + server_sign
    print(server_sign)
    return server_sign

def get_str(len):
    return ''.join(random.sample(string.ascii_letters + string.digits, len))



book = xlrd.open_workbook('./cases.xlsx')
table = book.sheet_by_name('用例')
# print(table.nrows)
# print(table.row_values(1))
# print(table.cell_value(0,0))

# for n in range(1, table.nrows):
#     values = table.row_values(n)
#     # print(values)
#     for i in range(0, len(values)):
#         ctype = table.cell_value(, i)
#         print(ctype)




try:
    book = xlrd.open_workbook('./cases.xlsx')
    table = book.sheet_by_name('用例')
except Exception:
    raise Exception('项目配置文件不存在:'+'./cases.xlsx'+' '+'用例')
else:
    nrows = table.nrows
    # print(nrows) #4
    if nrows > 0:
        li = []
        for n in range(1, nrows):
            values = table.row_values(n)
            # print(values)
            data = {}
            for i in range(0, len(values)): #0~7
                ctype = table.cell_type(n, i)
                print(ctype)
                #是number类型，
                if ctype == 2 and values[i] % 1 == 0:
                    data[table.cell_value(0, i)] = str(int(values[i]))
                elif ctype == 2 and values[i] % 1 != 0:
                    data[table.cell_value(0, i)] = str(values[i])
                elif ctype == 3:
                    date = xlrd.xldate_as_datetime(values[i], 0)
                    data[table.cell_value(0, i)] = date.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data[table.cell_value(0, i)] = values[i]
            else:
                li.append(data)
        # return {sheet_name: li}