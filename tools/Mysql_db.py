# encoding: utf-8


import MySQLdb
import logging
import time
import threading
import ConfigParser
import sys
import os
import platform

__author__ = 'wubo'
# 2015/12/7

"""
Usage:
    from Mysql_db import DB
     db = DB()
     db.execute(sql)
     db.fetchone()
     db.fetchall()
     :return same as MySQLdb
"""
my_os = platform.platform().split('-')[0]
if my_os == "Windows":
    pass
else:
    pass
    # current_filename = sys.argv[0][sys.argv[0].rfind(os.sep) + 1:sys.argv[0].rfind(os.extsep)]
    # logging.basicConfig(filename=current_filename + '_DB.log', filemode='w')

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

env = config.get("Env", "env")


local_host = config.get(env, "service_mysql_host")
remote_host = config.get(env, "remote_mysql_host")


class DB(object):
    conn = None
    cursor = None
    _sock_file = ''

    def __init__(self, local=False, readonly=False):
        self.readonly = readonly
        try:
            if local is True:
                self.host = local_host
            else:
                self.host = remote_host
            config = ConfigParser.ConfigParser()
            config.read('/etc/my.cnf')
            self._sock_file = ""  # config.get('mysqld', 'socket')
        except ConfigParser.NoSectionError:
            self._sock_file = ''

    def connect(self):
        logging.info(time.ctime() + " : connect to mysql server..")
        if self.readonly is False:
            sql_user = 'traner'
            sql_passwd = "genetraner"
        else:
            sql_user = "traner"
            sql_passwd = "genetraner"
        if self._sock_file != '':
            self.conn = MySQLdb.connect(host=self.host, port=3306, user=sql_user,
                                        passwd='genetraner', db='tran_web', charset='utf8',
                                        unix_socket=self._sock_file)
            self.cursor = self.conn.cursor()
        else:
            self.conn = MySQLdb.connect(host=self.host, port=3306, user=sql_user,
                                        passwd=sql_passwd, db='tran_web', charset='utf8')
            self.cursor = self.conn.cursor()
        # self.conn = MySQLdb.connect(host='localhost', port=3306, user='root',
        #                             passwd='root1256', db='clinic', charset='utf8')

        # self.conn = MySQLdb.connect(host='192.168.120.105', port=3306, user='gpo',
        #                             passwd='btlc123', db='clinic', charset='utf8')

        self.conn.autocommit(True)

    # 线程函数
    def thread(self):
        t = threading.Thread(target=self.conn.ping, args=())
        t.setDaemon(True)
        t.start()
        t.join(4)
        if t.isAlive():
            return 0
        else:
            return 1

    def execute(self, sql_query):
        try:
            logging.info(time.ctime() + " : " + sql_query)
            # 重启超过五次则不再重启
            i = 0
            while i < 3 and self.thread() != 1:
                self.close()
                self.connect()
                self.cursor = self.conn.cursor()
                i += 1
            if i == 3:
                return logging.error(time.ctime() + "execute failed")
            handled_item = self.cursor.execute(sql_query)
        except Exception, e:
            logging.error(e.args)
            logging.info("Reconnecting..---------------")
            self.connect()
            self.cursor = self.conn.cursor()
            logging.info(time.ctime() + " : " + sql_query)
            handled_item = self.cursor.execute(sql_query)
        return handled_item

    def execute_transaction(self, array_sql_action):
        """
        CRUD 操作 使用时，加入事务的处理。
        :param array_sql_action:
        :return:
        """
        try:
            logging.info(" %s : %s" % (time.ctime(), array_sql_action))
            # 重启超过五次则不再重启
            i = 0
            while i < 3 and self.thread() != 1:
                self.close()
                self.connect()
                self.cursor = self.conn.cursor()

                i += 1
            if i == 3:
                return logging.error(time.ctime() + "数据库连接失败！----------")
            try:
                if type(array_sql_action) is list:
                    self.conn.autocommit(False)
                    n = 0
                    for j in range(0, len(array_sql_action)):
                        print array_sql_action[j]['sql']
                        n = n + self.cursor.execute(array_sql_action[j]['sql'])
                else:
                    n = self.cursor.execute(array_sql_action)
                self.cursor.close()
            except Exception, e:
                logging.info("Reconnecting..---------------")
                # logging.error("数据库执行错误，数据已经回滚！..%s----%s---%s" % (e.args, e.message, array_sql_action))
                self.conn.rollback()
                error_sql = ''
                try:
                    self.connect()
                    self.cursor = self.conn.cursor()
                    if type(array_sql_action) is list:
                        self.conn.autocommit(False)
                        n = 0
                        for j in range(0, len(array_sql_action)):
                            error_sql = array_sql_action[j]['sql']
                            n = n + self.cursor.execute(array_sql_action[j]['sql'])
                    else:
                        n = self.cursor.execute(array_sql_action)
                    self.cursor.close()
                except Exception, e:
                    self.conn.rollback()
                    logging.error("数据库执行错误，数据已经回滚！..%s----%s---%s" % (e.args, e.message, error_sql))
                    n = 0
            finally:
                logging.info("数据库执行完毕！sql:%s" % array_sql_action)
                self.conn.commit()
                return n
        except Exception, e:
            logging.error("数据库链接失败！..%s----%s---%s" % (e.args, e.message, array_sql_action))
            return 0

    def fetchone(self):
        try:
            logging.info(time.ctime() + " : fetchone")
            one_item = self.cursor.fetchone()
        except Exception, e:
            logging.error(e.args)
            logging.info(time.ctime() + " : fetchone failed, return ()")
            one_item = ()
        return one_item

    def fetchall(self):
        try:
            logging.info(time.ctime() + " : fetchall")
            all_item = self.cursor.fetchall()
        except Exception, e:
            logging.error(e.args)
            logging.info(time.ctime() + " : fetchall failed, return ()")
            all_item = ()
        return all_item

    def close(self):
        logging.info(time.ctime() + " : close connect")
        if self.cursor:
            self.cursor.close()
        self.conn.close()

    def create_table(self, table_name, table_desc, force=False, table_comment=""):
        try:
            show_sql = "SHOW TABLES LIKE '%s';" % table_name
            result = self.execute(show_sql)
            execute_message = ""
            if result == 1:
                if force:
                    del_sql = "DROP TABLE  %s;" % table_name
                    self.execute(del_sql)
                    execute_message += "Delete The Original Table %s \n" % table_name
                else:
                    return False, "%s Table Already Exists" % table_name
            create_table_sql = "CREATE TABLE %s (" % table_name
            primary_key = []
            for value in table_desc:
                create_table_sql += "%s %s" % (value[0], value[1])
                if value[2] == "NO":
                    create_table_sql += " NOT NULL"
                if value[3] == "PRI":
                    primary_key.append(value[0])
                    # create_table_sql += " PRIMARY KEY"
                if value[4] is not None and value[4] != "None":
                    create_table_sql += " default %s" % value[4]
                if value[5] != "":
                    create_table_sql += " %s" % value[5]
                if len(value) >= 7:
                    create_table_sql += " COMMENT '%s'" % value[6]
                create_table_sql += ","
            if primary_key != []:
                create_table_sql += " PRIMARY KEY (%s)," % ",".join(primary_key)
            if table_comment != "":
                create_table_sql = create_table_sql[:-1] + ") COMMENT '%s';" % table_comment
            else:
                create_table_sql = create_table_sql[:-1] + ");"
            self.execute(create_table_sql)
            execute_message += "CREATE TABLE %s Success \n" % table_name
            return True, execute_message
        except Exception, e:
            error_message = str(e.args)
            return False, "fail:%s." % error_message

    def check_table(self, table_name, table_desc):
        try:
            check_sql = "DESC %s;" % table_name
            self.execute(check_sql)
            # desc = self.fetchall()
            # if len(desc) != len(table_desc):
            #     return False
            # for i in range(0, len(desc)-1):
            #     desc_item = desc[i]
            #     table_desc_item = table_desc[i]
            #     if len(desc_item) != len(table_desc_item):
            #         return False
            #     for j in range(0, len(desc_item)-1):
            #         if desc_item[j] != table_desc_item[j]:
            #             return False
            return True
        except Exception, e:
            error_message = str(e.args)
            print(error_message)
            return False

