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


# @task_api.route("/tasks/list/",methods=["GET"])
# def task_list_get():
#     try:
#         postdata = json.loads(request.data)
#         account = postdata["account"]
#         password = postdata["password"]
#         if type(account) != str and type(account) != unicode and len(account) <= 0:
#             return json.dumps({"status":"403, account"})
#         if type(password) != str and type(password) != unicode and len(password) <= 0:
#             return json.dumps({"status":"403, account"})
#         user_flag = user_affirm(account,password)
#         if user_flag == 0:
#             return json.dumps({"status":"user not exit"})
#         select_sql = "SELECT sys_no,disease_id,disease_name,disease_name_zn " \
#                      "FROM disease_detail WHERE flag = 0 AND available = 0 limit 0,100;"
#         re = db.execute(select_sql)
#         if re > 0:
#             result = db.fetchall()
#         else:
#             return json.dumps({"status":"failed get list"})
#         task_list = []
#         for item in result:
#             dict1 = {}
#             sys_no,disease_id,disease_name,disease_name_zn = item
#             set_sql = "UPDATE disease_detail SET available = 1 WHERE sys_no = %d;" % sys_no
#             re = db.execute(set_sql)
#             dict1["sys_no"] = sys_no
#             dict1["disease_id"] = disease_id
#             dict1["disease_name"] = disease_name
#             dict1["disease_name_zn"] = disease_name_zn
#             task_list.append(dict1)
#         return json.dumps({"status":"success!","data":task_list})
#     except Exception,e:
#         print str(e)
#         return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


# @task_api.route("/tasks/<int:sys_no>/",methods=["GET"])
# def disease_info_get(sys_no):
#     try:
#         postdata = json.loads(request.data)
#         account = postdata["account"]
#         password = postdata["password"]
#         if type(account) != str and type(account) != unicode and len(account) <= 0:
#             return json.dumps({"status":"403, account"})
#         if type(password) != str and type(password) != unicode and len(password) <= 0:
#             return json.dumps({"status":"403, account"})
#         user_flag = user_affirm(account,password)
#         if user_flag == 0:
#             return json.dumps({"status":"user not exit"})
#         select_sql = "SELECT disease_id,disease_name,disease_name_zn,text,text_zn,flag " \
#                      "FROM disease_detail WHERE sys_no = %d;" % sys_no
#         re = db.execute(select_sql)
#         if re > 0:
#             result = db.fetchone()
#             disease_id,disease_name,disease_name_zn,text,text_zn,flag = result
#         else:
#             return json.dumps({"status":"failed get disease info"})
#         disease_info = {}
#         disease_info["disease_id"] = disease_id
#         disease_info["disease_name"] = disease_name
#         disease_info["disease_name_zn"] = disease_name_zn
#         disease_info["text"] = text
#         disease_info["text_zn"] = text_zn
#         disease_info["flag"] = flag
#         disease_info["sys_no"] = sys_no
#         return json.dumps({"status":"success!","data":disease_info})
#     except Exception,e:
#         print str(e)
#         return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})

# @task_api.route("/tasks/<int:sys_no>/",methods=["PUT"])
# def disease_info_update(sys_no):
#     try:
#         postdata = json.loads(request.data)
#         account = postdata["account"]
#         password = postdata["password"]
#         if type(account) != str and type(account) != unicode and len(account) <= 0:
#             return json.dumps({"status":"403, account"})
#         if type(password) != str and type(password) != unicode and len(password) <= 0:
#             return json.dumps({"status":"403, account"})
#         user_flag = user_affirm(account,password)
#         if user_flag == 0:
#             return json.dumps({"status":"user not exit"})
#         disease_name_zn = postdata.get("disease_name_zn")
#         text_zn = postdata.get("text_zn")
#         flag = postdata.get("flag")
#         if disease_name_zn is None:
#             disease_name_zn = "N\A"
#         if text_zn is None:
#             text_zn = "N\A"
#         if flag is None:
#             flag = 0
#         update_sql = "UPDATE disease_detail SET disease_name_zn = '%s',text_zn = '%s',flag = %d " \
#                      "WHERE sys_no = %d;" % (disease_name_zn,text_zn,flag,sys_no)
#         re = db.execute(update_sql)
#         if re > 0:
#             postdata.pop("account")
#             postdata.pop("password")
#             postdata["sys_no"] = sys_no
#             return json.dumps({"status":"success!","data":postdata})
#         else:
#             return json.dumps({"status":"failed to update"})
#     except Exception,e:
#         print str(e)
#         return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


@task_api.route("/tasks/reset/",methods=["PUT"])
def reset_available():
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
        sys_no_list = postdata.get("sys_no_list")
        if sys_no_list is None:
            return json.dumps({"status":"403, sys_no_list not exit"})
        elif type(sys_no_list) != list:
            return json.dumps({"status":"403, sys_no_list need list"})
        failed_list = []
        for sys_no in sys_no_list:
            reset_sql = "UPDATE disease_detail SET available = 0 WHERE sys_no = %d;" % sys_no
            re = db.execute(reset_sql)
            if re == 0:
                failed_list.append(sys_no)
        return json.dumps({"status": 001, "data": {"failed":failed_list}})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


# --------------------------------------第二版----------------------------------------------------------------------
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

        # 判断权限
        right_check = "SELECT user_right FROM account_for_disease WHERE account = '%s';" % account
        re1 = db.execute(right_check)
        if re1 > 0:
            user_right = db.fetchone()[0]
        else:
            return json.dumps({"status":"sys'account not exsit"})
        # 录入员
        if user_right == 1:
            # 判断是否有已占用的数据
            select_sql1 = "SELECT sys_no,disease_id,disease_name,disease_name_zn" \
                          " FROM disease_detail WHERE account = '%s' AND flag = '%s';" % \
                          (account, 1)
            re2 = db.execute(select_sql1)
            # 存在已占用的数据 只返回已占用 已保存，已提交
            task_list1 = []
            if re2 > 0:
                result1 = db.fetchall()
                for item1 in result1:
                    dict1 = {}
                    sys_no,disease_id,disease_name,disease_name_zn = item1
                    dict1["sys_no"] = sys_no
                    dict1["disease_id"] = disease_id
                    dict1["disease_name"] = disease_name
                    if disease_name_zn is None:
                        disease_name_zn = 'NA'
                    dict1["disease_name_zn"] = disease_name_zn
                    task_list1.append(dict1)
            # 不存在已占用的数据 取100未被占用的数据 并置为1 account,并返回已保存，已提交
            else:
                select_sql2 = "SELECT sys_no,disease_id,disease_name,disease_name_zn " \
                            "FROM disease_detail WHERE flag = 0 limit 0,100;"
                re2 = db.execute(select_sql2)
                if re2 > 0:
                    result2 = db.fetchall()
                else:
                    result2 = []
                for item2 in result2:
                    dict2 = {}
                    sys_no,disease_id,disease_name,disease_name_zn = item2
                    dict2["sys_no"] = sys_no
                    dict2["disease_id"] = disease_id
                    dict2["disease_name"] = disease_name
                    if disease_name_zn is None:
                        disease_name_zn = 'NA'
                    dict2["disease_name_zn"] = disease_name_zn
                    # 置为占用状态
                    update_sql1 = "UPDATE disease_detail SET flag = 1,account = '%s' " \
                                  "WHERE sys_no = '%s' AND disease_id = '%s';" % \
                                  (account, sys_no, disease_id)
                    re3 = db.execute(update_sql1)
                    task_list1.append(dict2)
            # 返回已保存的数据
            task_list2 = []
            select_sql3 = "SELECT sys_no,disease_id,disease_name,disease_name_zn " \
                          "FROM disease_detail WHERE flag = 2 AND account = '%s';" % \
                          (account)
            re4 = db.execute(select_sql3)
            if re4 > 0:
                result4 = db.fetchall()
                for item4 in result4:
                    sys_no,disease_id,disease_name,disease_name_zn = item4
                    dict3 = {}
                    dict3["sys_no"] = sys_no
                    dict3["disease_id"] = disease_id
                    dict3["disease_name"] = disease_name
                    if disease_name_zn is None:
                        disease_name_zn = 'NA'
                    dict3["disease_name_zn"] = disease_name_zn
                    task_list2.append(dict3)
            # 返回已提交的数据
            task_list3 = []
            select_sql4 = "SELECT sys_no,disease_id,disease_name,disease_name_zn " \
                          "FROM disease_detail WHERE flag = 3 AND account = '%s';" % \
                          (account)
            re5 = db.execute(select_sql4)
            if re5 > 0:
                result5 = db.fetchall()
                for item5 in result5:
                    sys_no,disease_id,disease_name,disease_name_zn = item5
                    dict5 = {}
                    dict5["sys_no"] = sys_no
                    dict5["disease_id"] = disease_id
                    dict5["disease_name"] = disease_name
                    if disease_name_zn is None:
                        disease_name_zn = 'NA'
                    dict5["disease_name_zn"] = disease_name_zn
                    task_list3.append(dict5)
            return json.dumps({"status": 001,
                               "data": {"user_right": user_right, "new_get": task_list1, "saved": task_list2, "commit": task_list3}})

        # 审核员
        elif user_right == 0:
            # 按用户获得已提交的数据
            # 获得所有录入员
            assessor_sql = "SELECT user_no,account FROM account_for_disease WHERE user_right = 1;"
            res1 = db.execute(assessor_sql)
            if res1 > 0:
                result21 = db.fetchall()
            else:
                return json.dumps({"status":"no users"})
            account_no = len(result21)
            big_dict = {}

            big_dict["pushed"] = {}
            big_dict["checked"] = {}
            big_dict["user_right"] = user_right
            for account_item in result21:
                user_no = account_item[0]
                account = account_item[1]
                # 该用户已提交的数据
                sql1 = "SELECT sys_no,disease_id,disease_name,disease_name_zn,text,text_zn," \
                       "score FROM disease_detail WHERE account = '%s' AND flag = '%s';" % \
                       (account, 3)
                res2 = db.execute(sql1)
                if res2 > 0:
                    result22 = db.fetchall()
                    account_list1 = []
                    for commit_item in result22:
                        account_dict = {}
                        sys_no,disease_id,disease_name,disease_name_zn,text,text_zn,sore = commit_item
                        account_dict["sys_no"] = sys_no
                        account_dict["disease_id"] = disease_id
                        account_dict["disease_name"] = disease_name
                        account_dict["disease_name_zn"] = disease_name_zn
                        account_dict["text"] = text
                        account_dict["text_zn"] = text_zn
                        account_dict["sore"] = sore
                        account_list1.append(account_dict)
                    big_dict["pushed"][account] = account_list1


                sql2 = "SELECT sys_no,disease_id,disease_name,disease_name_zn,text,text_zn," \
                       "score FROM disease_detail WHERE account = '%s' AND flag = '%s';" % \
                       (account, 4)
                res3 = db.execute(sql2)
                if res3 > 0:
                    result23 = db.fetchall()
                    account_list2 = []
                    for commit_item2 in result23:
                        account_dict2 = {}
                        sys_no,disease_id,disease_name,disease_name_zn,text,text_zn,sore = commit_item2
                        account_dict2["sys_no"] = sys_no
                        account_dict2["disease_id"] = disease_id
                        account_dict2["disease_name"] = disease_name
                        account_dict2["disease_name_zn"] = disease_name_zn
                        account_dict2["text"] = text
                        account_dict2["text_zn"] = text_zn
                        account_dict2["sore"] = sore
                        account_list2.append(account_dict2)
                    big_dict["checked"][account] = account_list2
            return json.dumps({"status": 001, "data":big_dict})
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
        disease_name_zn = postdata.get("disease_name_zn")
        text_zn = postdata.get("text_zn")
        flag = postdata.get("flag")
        score = postdata.get("score")
        if disease_name_zn is None:
            disease_name_zn = "N\A"
        if text_zn is None:
            text_zn = "N\A"
        if flag is None:
            return json.dumps({"status":"need flag"})
        if type(flag) != int and flag == 0 and flag > 4 and flag < 2:
            return json.dumps({"status":"403, flag"})

        disease_name_zn = disease_name_zn.replace("'","\\'")
        text_zn = text_zn.replace("'","\\'")

        # 获得用户权限
        right_check = "SELECT user_right FROM account_for_disease WHERE account = '%s';" % account
        re1 = db.execute(right_check)
        if re1 > 0:
            user_right = db.fetchone()[0]
        else:
            return json.dumps({"status":"sys'account not exsit"})

        # 审核者
        if user_right == 0:
            if flag != 4:
                return json.dumps({"status":"flag should equal 4"})
            update_sql1 = "UPDATE disease_detail SET score = '%s',flag = 4 WHERE " \
                          "sys_no = %d;" % (score,sys_no)
            re2 = db.execute(update_sql1)
            if re2 > 0:
                return json.dumps({"status":001})
            else:
                return json.dumps({"status":001,
                                   "data": {"user_right": user_right,"score":score,"flag":flag,"sys_no": sys_no}})
        # 录入员
        elif user_right == 1:
            if flag == 4:
                return json.dumps({"status":"flag do not have right equal 4"})
            if flag not in (2,3):
                return json.dumps({"status":"flag should equal 2,3"})
            update_sql2=  "UPDATE disease_detail SET disease_name_zn = '%s',text_zn = '%s',flag = %d" \
                          " WHERE sys_no = %d AND account = '%s';" % \
                          (disease_name_zn,text_zn,flag,sys_no,account)
            re3 = db.execute(update_sql2)
            if re3 > 0:
                return json.dumps({"status":001, "data": {"user_right": user_right,
                                                                 "flag":flag,"sys_no":sys_no,"text_zn":text_zn,"disease_name_zn":disease_name_zn}})
            else:
                return json.dumps({"status":001})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})




















