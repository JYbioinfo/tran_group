# -*- coding: utf-8 -*-
# Create Date 2015/12/14
__author__ = 'wubo'
import ConfigParser, re, xlrd, MySQLdb
from tools.Mysql_db import DB
db = DB()
def testConfig():
    config = ConfigParser.ConfigParser()
    config.read("../config.conf")
    env = config.get("Env", "env")
    h = config.get(env, "api_host")
    p = config.get(env, "api_port")
    print type(h)
    print h
    print type(p)
    print p
    API_service = "http://%s:%s" % (config.get(env, "api_host"), config.get(env, "api_port"))
    print type(API_service)


def test():
    sel_sql = "SELECT text FROM disease_detail limit 10;"
    db.execute(sel_sql)
    l = map(lambda s : s[0], db.fetchall())
    print l

def testf():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='rootsql', db='tran_web', port=3306)
    cursor = conn.cursor()
    with open(r"test_id.txt") as file:
        for line in file:
            line = line.strip("\n")
            sel_sql = "SELECT disease_name,text FROM disease_detail WHERE sys_no=%s;" % line
            cursor.execute(sel_sql)
            one = cursor.fetchone()
            ins_sql = "INSERT INTO disease_detail_short(disease_name,text) VALUES(%s,%s)" % (one[0], one[1])
            cursor.execute(ins_sql)
            conn.commit()
    print "insert success"
    with open(r"C:\Users\guhongjie\Desktop\test_id.txt") as f:
        for line in f:
            line = line.strip("\n")
            cursor.execute("DELETE FROM disease_detail WHERE sys_no=%s;") % line
            conn.commit()
    print "delete success!"


def insert2db():
    file = xlrd.open_workbook(r"C:\Users\guhongjie\Desktop\disease_detail.xlsx")
    sheet = file.sheet_by_index(1)
    print sheet.name
    print sheet.nrows
    disease_name = sheet.row(15)[1].value+u";"+sheet.row(16)[1].value+u";"+sheet.row(17)[1].value
    disease_text = sheet.row(15)[2].value+u"\n"+sheet.row(16)[2].value+u"\n"+sheet.row(17)[2].value+u"\n"+sheet.row(15)[3].value
    # in_sql = "INSERT INTO disease_detail(disease_id,disease_name_zn,text_zn,flag,account,score) " \
    #          "VALUES ('%s','%s','%s',4,'JingYun','5')" % (int(t[0].value), t[1].value, t[2].value)
    # db.execute(in_sql)
    # print "insert success"

    update_sql = "UPDATE disease_detail SET disease_name_zn = '%s',text_zn = '%s',account ='JingYun', " \
                 "flag = 4, score = '5' WHERE disease_id = '%s';" % (disease_name,disease_text,'117000')
    print db.execute(update_sql)

    # for i in range(1, sheet.nrows):
    #     disease_id = int(sheet.row(i)[0].value)
    #     disease_name = sheet.row(i)[1].value
    #     disease_text = sheet.row(i)[2].value+sheet.row(i)[3].value
    #     update_sql = "UPDATE disease_detail SET disease_name_zn = '%s',text_zn = '%s',account ='JingYun', " \
    #                  "flag = 4, score = '5' WHERE disease_id = '%s';" % (disease_name,disease_text,disease_id)
    #     if db.execute(update_sql) > 0:
    #         print "insert success %s" %disease_id
    #     else:
    #         print "fail %d" % disease_id


def classify_name():
    sel_sql = "SELECT disease_id,disease_name FROM disease_detail_copy;"
    db.execute(sel_sql)
    l = db.fetchall()
    result_list = []
    t_list = []
    for item in l:
        temp_list = re.findall(r"[a-zA-Z0-9]+", item[1])
        t_list.append([item[0], item[1], temp_list])

    file = open(r"C:\Users\guhongjie\Desktop\classified.tsv", "w")

    for record in t_list:
        group_flag = False
        for group in result_list:
            flag = False
            for item in group:
                count = 0
                for word in record[2]:
                    if word in item[2]:
                        count += 1
                if count >= 3:
                    group.append(record)
                    group_flag = True
                    flag = True
                    break
            if flag:
                print "add into a group"
                break
        if not group_flag:
            result_list.append([record])
            print "create a group"

    group_no = 1
    for group in result_list:
        for item in group:
            s = item[0]+u'\t'+item[1]+u'\t'+str(group_no).encode("utf-8")+u"\n"
            file.write(s)
        group_no += 1
    print "done"


def classify_name2():
    sel_sql = "SELECT disease_id,disease_name FROM disease_detail_copy;"
    db.execute(sel_sql)
    l = db.fetchall()
    result_list = []
    t_list = []
    for item in l:
        temp_list = re.findall(r"[a-zA-Z0-9]+", item[1])
        t_list.append([item[0], item[1], temp_list])

    file = open(r"C:\Users\guhongjie\Desktop\classified2.tsv", "w")

    for record in t_list:
        group_flag = False
        for group in result_list:
            flag = False
            for item in group:
                f = True
                if len(record[2]) == 0 or len(item[2]) == 0:
                    f = False
                    break
                if len(record[2]) < 3 or len(item[2]) < 3:


                    for i in range(min(len(record[2]),len(item[2]))):
                        if record[2][i] != item[2][i]:
                            f = False
                            break
                else:
                    for i in range(3):
                        if record[2][i] != item[2][i]:
                            f = False
                            break
                if f:
                    group.append(record)
                    group_flag = True
                    flag = True
                    break
            if flag:
                print "add into a group"
                break
        if not group_flag:
            result_list.append([record])
            print "create a group"

    group_no = 1
    for group in result_list:
        for item in group:
            s = item[0]+u'\t'+item[1]+u'\t'+str(group_no).encode("utf-8")+u"\n"
            file.write(s)
        group_no += 1
    print "done"


def hide_table():
    dic = {}
    with open(r"C:\Users\guhongjie\Desktop\classified2.tsv") as file:
        for line in file:
            items = line.strip("\n").split("\t")
            if dic.get(items[2]):
                dic[items[2]].append(items[0])
            else:
                dic[items[2]] = [items[0]]
    l = 0
    for k,vlist in dic.items():
        if len(vlist) > 1:
            l+=len(vlist)
            for disease_id in vlist:
                up_sql = "UPDATE disease_detail SET flag = 99 WHERE disease_id = '%s' AND flag < 2;" % disease_id
                db.execute(up_sql)
    print l

def into_table():
    dic = {}
    with open(r"C:\Users\guhongjie\Desktop\classified2.tsv") as file:
        for line in file:
            items = line.strip("\n").split("\t")
            if dic.get(items[2]):
                dic[items[2]].append(items[0])
            else:
                dic[items[2]] = [items[0]]
    l = 0
    for k,vlist in dic.items():
        if len(vlist) > 1:
            l += len(vlist)
            for disease_id in vlist:
                sel_sql = "SELECT disease_name,text FROM disease_detail_copy WHERE disease_id = '%s';" % disease_id
                db.execute(sel_sql)
                t = db.fetchone()
                text = t[1].replace("'", "\\'")
                ins_sql = 'INSERT INTO group_disease(group_no,disease_no,disease_name,text)' \
                          ' VALUES(%s,"%s","%s","%s");' % (k, disease_id, t[0], text)
                print db.execute(ins_sql)
    print l


if __name__ == '__main__':
    # classify_name2()
    into_table()

    

