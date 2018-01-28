#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/11 上午10:46
"""

import platform

from flask import Flask, g, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)



app.debug = True  # apache 中 main 的设置无效

CORS(app=app)   # 全局跨域访问



app.config['SECRET_KEY'] = "wq1oipej1lej"

@app.route('/', methods=['GET', 'POST'])
def main_test():
    print "http://hostname/test"
    return "ssss"


def run_server():
    app.run(debug=True, port=80, host='0.0.0.0', threaded=True)

if __name__ == '__main__':
    run_server()
