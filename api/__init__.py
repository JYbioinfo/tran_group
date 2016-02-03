# encoding: utf-8
# !/usr/bin/python
import sys

sys.path.append(r'..')

__author__ = 'wubo'

import sys
from flask import Flask, request
import ConfigParser
import json

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET FOR JY STRING'

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

env = config.get("Env", "env")

api_listen_ip = config.get(env, "api_listen_ip")

api_port = config.getint(env, "api_port")


@app.route('/hello/', methods=["GET"])
def hello():
    return "HELLO"

from api_task import task_api
app.register_blueprint(task_api, url_prefix='/api')


@app.before_request
def before_request():
    if request.method == "OPTIONS" and "geneacdms" in request.args and request.args["geneacdms"] == "test":
        return json.dumps({"status": 001, "message": "test success"})


@app.after_request
def after_request(response):
    if "geneacdms" in request.args and request.args["geneacdms"] == "test":
        response.headers["Access-Control-Allow-Methods"] = "POST,GET,PUT,DELETE"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "content-type,Authorization"
    return response
    

