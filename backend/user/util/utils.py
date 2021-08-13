from user.models import *

TOKENTIMEOUT = 600 # 用户token生存时间
DEBUG = True # 后端程序运行时是否允许输出信息
WIDTH = 11 # 数据库uid宽度(不可更改)

def idIter(start=0):
    id = start
    while True:
        yield str(id).rjust(WIDTH, '0')
        id += 1

try:
    if DEBUG:
        print('\nUser idIterators')
        print('---------------------------------------')
    user_uid = user_account_info.objects.last()
except:
    user_uid = None
    if DEBUG:
        print('Initiallize idIterators failed')

user_uid = int(user_uid.uid if user_uid else -1) + 1
user_uid = idIter(user_uid)