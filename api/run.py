# -*- coding: utf-8 -*-
# Create Date 2015/12/9
__author__ = 'wubo'

import sys
sys.path.append('..')
from api import api_listen_ip, api_port, env, app


if env != "Production" and env != "Test":
    if __name__ == '__main__':
        app.run(host=api_listen_ip, port=api_port)

# if __name__ == '__main__':
#     app.run(host=api_listen_ip, port=api_port)