import base64
import hashlib
import random
import string

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