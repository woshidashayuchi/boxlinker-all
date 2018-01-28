#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/12/8 18:54
"""

import requests

url = "http://email.boxlinker.com/send"

payload = """{"to": "liuzhangpei@126.com",
 "title": "sss", "text": "sdsd",
 "html": "sdsdsdsdsd"}"""
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "775945b1-b4fa-ef84-40dd-212e0a4e5036"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)