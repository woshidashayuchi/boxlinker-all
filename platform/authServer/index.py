#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/11 上午10:46
"""

import platform

from flask import Flask, g, jsonify, render_template, request
from flask_cors import CORS

from pyTools.tools.codeString import request_result

from authServer.models.hub_db_meta import Session, init_create_hub_db
from authServer.tools.logs import logging as log
from authServer.view.oauth import oauth
from authServer.view.registry import registry
from authServer.view.user import user
from authServer.view.v1.usercenter import usercenter
from authServer.view.v1.repository import repository
from authServer.view.v1.oauthclient import oauthclient

from authServer.view.v2.oauthclient import oauthv2

app = Flask(__name__)

app.register_blueprint(registry, url_prefix='/registry')

app.register_blueprint(user, url_prefix='/user')

app.register_blueprint(oauth, url_prefix='/oauth')   # 第三方认证

app.register_blueprint(usercenter, url_prefix='/api/v1.0/usercenter')   # 组织相关

app.register_blueprint(repository, url_prefix='/api/v1.0/repository')   # 镜像相关

app.register_blueprint(oauthclient, url_prefix='/api/v1.0/oauthclient')   # 第三方代码


app.register_blueprint(oauthv2, url_prefix='/api/v2.0/oauths')   # 第三方代码;v2版本


from authServer.view.v1.otherServer import otherserver
app.register_blueprint(otherserver, url_prefix='/api/v1.0/otherserver')   # 其他服务




app.debug = True  # apache 中 main 的设置无效
CORS(app=app)   # 全局跨域访问

# init_create_hub_db()


app.config['SECRET_KEY'] = "wq1oipej1lej"


@app.before_request
def before_request():
    g.secret_key = app.secret_key
    g.db_session = Session()

    print request.url


    log.info('--------- before_request ---------')


# @app.after_request
# def after_request():
#     print 'dddddd---after_request'
# #     g.db.__del__()


@app.teardown_request
def teardown_request(exception):
    print 'teardown_request  error'
    g.db_session.close()

    return jsonify({'teardown_request': 'index teardown_request'})

@app.route('/test', methods=['GET', 'POST'])
def main_test():
    print "http://hostname/test"
    return "index test"
    # return render_template('github.html', item='http://boxlinker.com')

# api不存在
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(request_result(804))



@app.route('/login', methods=['GET', 'POST'])
def main_login():
    return render_template('github.html', item='http://boxlinker.com/login')


def run_server():
    sysstr = platform.system()  # Windows测试模式
    if 'Windows' == sysstr:
        app.run(debug=True, threaded=True)
    elif 'Darwin' == sysstr:  # mac
        app.run(debug=True, port=8110, host='0.0.0.0', threaded=True)
    elif 'Linux' == sysstr:
        app.run(debug=False, port=80, host='0.0.0.0', threaded=True)

        # 不显示详细错误信息

if __name__ == '__main__':
    run_server()
