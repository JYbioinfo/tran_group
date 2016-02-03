#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append(r'..')
import ConfigParser
import json
from platform import system
from tools.Mysql_db import DB
from flask import Flask
from flask.ext.login import LoginManager, UserMixin
from flask_wtf.csrf import CsrfProtect

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

env = config.get("Env", "env")
remote_mysql_host = config.get(env, "remote_mysql_host")
web_listen_ip = config.get(env, "web_listen_ip")
web_port = config.get(env, "web_port")
API_service = "http://%s:%s" % (config.get(env, "api_host"), config.get(env, "api_port"))

login_manager = LoginManager()
csrf = CsrfProtect()

db = None
try:
    db = DB()
    db.connect()
except Exception, e:
    print e


class User(UserMixin):
    account = ""
    def get_id(self):
        return self.account


@login_manager.user_loader
def load_user(account):
    db.execute("select password,user_right from account_for_disease where account='%s';" % account)
    data = db.fetchone()
    if data is not None:
        user = User()
        user.account = account
        user.passwd_enc = data[0]
        user.role = data[1]
        return user
    return None

login_manager.login_view = "/login"


def create_app():
    app = Flask("__name__")
    app.secret_key = 'web string'
    login_manager.init_app(app)

    # register blueprint
    from view_list import list_view
    app.register_blueprint(list_view)

    return app

