#! /usr/bin/env python
# coding: utf-8
import requests
from tools.hmac_passwd import HmacPasswd
import json

account = "yangrui"
password = HmacPasswd("yangrui").get_hmacpassed()

# 1 hello
postdata = json.dumps({})
# task_test = requests.get("http://127.0.0.1:7788/api/tasks/",
#                                             data=postdata)
# print task_test.text


# 2 get_list
postdata = json.dumps({"account": account,
            "password": password
            })
task_test = requests.get("http://127.0.0.1:7788/api/tasks/list/",
                                            data=postdata)
print task_test.text

# 3 detail
postdata = json.dumps({"account": account,
                       "password":password})
task_test = requests.get("http://127.0.0.1:7788/api/tasks/3/",data=postdata)
# print task_test.text

# 4 update

postdata = json.dumps({"account": account,
                       "password":password,
                       "disease_name_zn": "dota",
                       "flag": 2})
# task_test = requests.put("http://127.0.0.1:7788/api/tasks/3/",data=postdata)
# print task_test.text
