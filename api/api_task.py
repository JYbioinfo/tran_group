# -*- coding: utf-8 -*-
# Create Date 2015/12/9
import json
from flask import Blueprint, request
from tools.Mysql_db import DB
task_api = Blueprint("task_api",__name__)
db = DB()


@task_api.route("/tasks/",methods=["GET"])
def get_task_list():
    return json.dumps({"status":"hello world!"})

def user_affirm(account, password):
    user_flag = 0
    check_sql = "SELECT * FROM account_for_disease WHERE account = '%s' AND password = '%s';" \
                % (account, password)
    re = db.execute(check_sql)
    if re > 0:
        user_flag = 1
    else:
        user_flag = 0
    return user_flag


@task_api.route("/user/check/", methods=["POST"])
def check_user():
    postdata = json.loads(request.data)
    account = postdata["account"]
    password = postdata["password"]
    user_flag = 0
    check_sql = "SELECT user_right FROM account_for_disease WHERE account = '%s' AND password = '%s';" \
                % (account, password)
    re = db.execute(check_sql)
    if re > 0:
        user_right = db.fetchone()[0]
        user_flag = 1
    else:
        user_flag = 0
        user_right = ''
    return json.dumps({"status": user_flag, "user_flag":user_right})


# 获取list
@task_api.route("/tasks/list/",methods=["GET"])
def task_list_get():
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})


        select_sql_1 = "SELECT min(group_no) FROM group_disease " \
                       "WHERE group_status = 0;"
        db.execute(select_sql_1)
        group_no = db.fetchone()[0]


        select_sql_2 = "SELECT sys_no,disease_no,group_no,dissease_name,text,status FROM group_disease " \
                    "WHERE group_no = '%s';" % group_no
        db.execute(select_sql_2)
        result = db.fetchall()
        final_list = []
        for item in result:
            dict1= {}
            sys_no,disease_no,group_no,dissease_name,text,status = item
            dict1["sys_no"] = sys_no
            dict1["disease_no"] = disease_no
            dict1["group_no"] = group_no
            dict1["dissease_name"] = dissease_name
            dict1["text"] = text
            dict1["status"] = status
            final_list.append(dict1)
        return json.dumps({"status": 001, "data":final_list})

    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


# 查看详情
@task_api.route("/tasks/<int:sys_no>/",methods=["GET"])
def disease_info_get(sys_no):
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})
        # 获得用户权限
        right_check = "SELECT user_right FROM account_for_disease WHERE account = '%s';" % account
        re1 = db.execute(right_check)
        if re1 > 0:
            user_right = db.fetchone()[0]
        else:
            return json.dumps({"status":"sys'account not exsit"})

        select_sql = "SELECT disease_id,disease_name,disease_name_zn,text,text_zn,flag,account,score " \
                     "FROM disease_detail WHERE sys_no = %d;" % sys_no
        re = db.execute(select_sql)
        if re > 0:
            result = db.fetchone()
            disease_id,disease_name,disease_name_zn,text,text_zn,flag,account,score = result
        else:
            return json.dumps({"status":"failed get disease info"})

        if user_right == 1:
            if disease_name_zn is None:
                disease_name_zn = "NA"
            if text_zn is None:
                text_zn = "NA"
        elif user_right == 0:
            if disease_name_zn is None:
                disease_name_zn = ""
            if text_zn is None:
                text_zn = ""
        else:
            return json.dumps({"status":"wrong right"})

        disease_info = {}
        disease_info["user_right"] = user_right
        disease_info["disease_id"] = disease_id
        disease_info["disease_name"] = disease_name
        disease_info["disease_name_zn"] = disease_name_zn
        disease_info["text"] = text
        disease_info["text_zn"] = text_zn
        disease_info["flag"] = flag
        disease_info["sys_no"] = sys_no
        disease_info["score"] = score
        disease_info["account"] = account
        return json.dumps({"status":001,"data":disease_info})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


# 更新 提交状态
@task_api.route("/tasks/<int:sys_no>/",methods=["PUT"])
def disease_info_update(sys_no):
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})

        # 更新为删除，status置为9
        update_sql1 = "UPDATE group_disease SET status = '%s' WHERE " \
                          "sys_no = %d;" % (9,sys_no)
        re2 = db.execute(update_sql1)
        return json.dumps({"status":001})

    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


@task_api.route("/tasks/group/<int:group_no>/",methods=["PUT"])
def next_group(group_no):
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})

        # 标记为完成 group_status = 6
        update_sql1 = "UPDATE group_disease SET group_satatus = %d WHERE " \
                          "group_no = %d;" % (6,group_no)
        re2 = db.execute(update_sql1)
        return json.dumps({"status":001})

    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})
