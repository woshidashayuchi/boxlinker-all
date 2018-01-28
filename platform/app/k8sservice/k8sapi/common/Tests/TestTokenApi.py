#!/usr/bin/env python

import requests

token = 'eyJ1aWQiOiAzLCAidXNlcl9vcmFnIjogImJveGxpbmtlciIsICJ0b2tlbmlkIjogIjg4NWZlZDcyZjUyYTkwNWRiOGM0NjY1ZSIsICJ1c2VyX25hbWUiOiAiYm94bGlua2VyIiwgImV4cGlyZXMiOiAxNDcyNjMzMDYzLjgwNjQzLCAidXNlcl9yb2xlIjogIjEiLCAidXNlcl9pcCI6ICIxMjcuMC4wLjEiLCAic2FsdCI6ICJlZjlmMDc4YzAxNTAwMDVkNjc5NGM1OTEiLCAiZW1haWwiOiAibGl2ZW5vd2h5QDEyNi5jb20ifbVUnbMQdSQGXCbw7MPb8H0='

url = 'http://auth.boxlinker.com/user/check_token_get'
headers = {'token': token}

r = requests.get(url, headers=headers)

print('r.url = %s' % (r.url))

print('r.text = %s' % (r.text))

print('r.json = %s' % (r.json()))

print('ret = %d' % (r.json()['status']))
