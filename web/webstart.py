#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create Date 2015/12/9
import sys
sys.path.append(r'..')
from web import create_app, web_listen_ip, web_port, env
app = create_app()
if env != "Production" and env != "Test":
    if __name__ == '__main__':
        print "http://%s:%s" %( web_listen_ip, int(web_port))
        app.run(host=web_listen_ip, threaded=True, debug=True, port=int(web_port))

# if __name__ == '__main__':
#     print "http://%s:%s" %( web_listen_ip, int(web_port))
#     app.run(host=web_listen_ip, threaded=True, debug=True, port=web_port)

