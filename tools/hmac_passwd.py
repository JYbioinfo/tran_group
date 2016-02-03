#! /usr/bin/env python
# coding: utf-8
from tools.Mysql_db import DB
from hashlib import sha256
from hmac import HMAC
import binascii, sys, random

class HmacPasswd:

    def __init__(self, passwd):
        salt = "secmsg" #用于hash的密钥，可改为其他固定值
        if isinstance(passwd, unicode):
            passwd = passwd.encode('UTF-8')
        for i in xrange(11):
            self.HmacPassword = HMAC(passwd, salt, sha256).digest()

    def get_hmacpassed(self):
        return binascii.b2a_hex(self.HmacPassword)


def insert_user(account,password,user_right):
    db = DB()
    passwd = HmacPasswd(password).get_hmacpassed()
    select_sql = "SELECT user_no FROM account_for_disease WHERE account = '%s';" % account
    re1 = db.execute(select_sql)
    if re1 > 0:
        sys_no = db.fetchone()[0]
        update_sql = "UPDATE account_for_disease SET password = '%s',user_right = '%s' " \
                     "WHERE account = '%s' AND user_no = '%s';" % (passwd,user_right,account,sys_no)
        db.execute(update_sql)
        print "UPDATA Success"
    else:
        select_sql = "SELECT max(user_no) FROM account_for_disease;"
        re = db.execute(select_sql)
        user_no = db.fetchone()[0] + 1
        insert_sql = "INSERT INTO account_for_disease (user_no,account,password,user_right) " \
                     "VALUES ('%s','%s','%s','%s');" % (user_no,account,passwd,user_right)
        db.execute(insert_sql)
        print "Insert Success"

if __name__ == '__main__':
    # l = ["madonglin","liyingnan","jinyue","liangzhanfeng","yangning","wenjie","zhangxuyang","caijing","chensiyao"]
    # for item in l:
    #     s = item+"%d" % random.randint(10, 99)
    #     print "account: %s  ,  password: %s" % (item, s)
    #     insert_user(item, s, 1)
    insert_user("JingYun", "JingYun", 1)


