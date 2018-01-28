#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/21 15:48
"""

from conf import DEBUG

OpenType = ['github', 'coding']


SECRET_KEY = 'wwq44rw3drwkr2o334i34343'

if DEBUG:
    # OAUTH_CALLBACK = 'http://192.168.1.6:8080/api/v2.0/oauths/callback'
    OAUTH_CALLBACK = 'http://imageauth.boxlinker.com/api/v1.0/oauthclient/callback'
    # OAUTH_CALLBACK = 'http://0.0.0.0:8000/api/v2.0/oauths/callback'
    OAUTH_WEBHOOKS = 'http://imageauth.boxlinker.com/api/v1.0/oauthclient/webhoos'

    # github Developer applications
    github_client_id = '9a8c43fa5301c02fb2f4'  # Client ID
    github_client_secret = '7510113c65735c7d3614b2164ba5e698e0c2104a'  # Client Secret

    # coding
    coding_client_id = 'e40b63f1f68c2ac6c8a56393882738f5'  # Client ID
    coding_client_secret = 'e0bedfdb802f3bdb9c28df3ba90ecc909f008e27'  # Client Secret
else:
    OAUTH_CALLBACK = 'http://imageauth.boxlinker.com/api/v1.0/oauthclient/callback'
    # OAUTH_CALLBACK = 'http://0.0.0.0:8000/api/v2.0/oauths/callback'
    OAUTH_WEBHOOKS = 'http://imageauth.boxlinker.com/api/v1.0/oauthclient/webhoos'

    # github Developer applications
    github_client_id = '44df81c41ee415b7debd'  # Client ID
    github_client_secret = '2ee2f93d511b0ba753a8e55e51b94b256ab44b40'  # Client Secret



    # coding
    coding_client_id = 'd624d2f871e8253dc7f947eece312a20'  # Client ID
    coding_client_secret = 'efcfdb0e8b6e87c36c2f35c3a6ebaaa6747e3a13'  # Client Secret


# github_repos_url = 'https://api.github.com/users/{0}/repos'

# state 用于防止垮站点攻击,
# 20170306 githut 权限升级  https://github.com/settings/tokens
user_oauth_url = 'https://github.com/login/oauth/authorize?client_id=' + github_client_id + '&state={0}' \
                 '&scope=user%20repo%20admin:org%20admin:public_key%20admin:repo_hook%20admin:org_hook%20admin:gpg_key%20notifications'



coding_scope = "user,user:email,notification,project,project:depot,project:key"
coding_oauth_url = "https://coding.net/oauth_authorize.html?client_id=" + coding_client_id + \
                   "&response_type=code" \
                   "&state={0}" + \
                   "&fsds=ssss" + \
                   "&scope=" + coding_scope + \
                   "&redirect_uri=" + OAUTH_CALLBACK


# https://imageauth.boxlinker.com/api/v1.0/oauthclient/callback/?code=a2e9490a293cdae96278f4715b9cb35c&scope=user%2Cuser%3Aemail%2Cnotification%2Cproject%2Cproject%3Adepot%2Cproject%3Akey&state=eyJzcmNfdHlwZSI6ICJjb2RpbmciLCAiZXhwaXJlcyI6IDE0OTEzODY3NDcuNTg0ODAxLCAic2FsdCI6ICIwLjYxNjg1NzU2MTkwMSIsICJ0ZWFtX3V1aWQiOiAiMmU4ZTdiMzctYTk1Ny00NzcwLTkwNzUtYWFhNjdlYWE0OWNlIiwgInJlZGlyZWN0X3VybCI6ICJodHRwOi8vdGVzdC5ib3hsaW5rZXIuY29tL2J1aWxkaW5nL2NyZWF0ZSJ9F_pBekZgLBUkhesHDRmjBw