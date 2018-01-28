define({ "api": [  {    "description": "<p>获取用户授权跳转链接</p>",    "version": "1.0.0",    "header": {      "fields": {        "Header": [          {            "group": "Header",            "type": "String",            "optional": false,            "field": "token",            "description": "<p>请求接口的token,放在请求头中</p>"          }        ]      }    },    "type": "get",    "url": "/oauth/oauthurl",    "title": "",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "status 为 0 成功,其中result-->msg中即用户需要点击进行授权的地址\n{\n    \"msg\": \"OK\",\n    \"result\":\n    {\n        \"msg\": \"https://github.com/login/oauth/authorize?client_id=44df81c41ee415b7debd&scope=user%20repo&state=eyJleHBpcmVzIjogMTQ3NTgzNzAxNi4wNzg2ODksICJzYWx0IjogIjAuMjQwNjIyOTU2NjgyIiwgInVpZCI6ICIzIn2ag7sMa7sSf6-vmhEMykRL\"\n    },\n    \"status\": 0\n}",          "type": "json"        }      ]    },    "error": {      "examples": [        {          "title": "Error-Response:",          "content": "{\n    \"msg\": \"An exception occurs\",\n    \"result\":\n    {\n        \"msg\": \"Incorrect padding\"\n    },\n    \"status\": 602\n}",          "type": "json"        }      ]    },    "filename": "oauth/github.py",    "group": "_Users_lzp_Desktop_PythonTools_authServer_oauth_github_py",    "groupTitle": "_Users_lzp_Desktop_PythonTools_authServer_oauth_github_py",    "name": "GetOauthOauthurl"  },  {    "description": "<p>获取github 项目列表</p>",    "version": "1.0.0",    "header": {      "fields": {        "Header": [          {            "group": "Header",            "type": "String",            "optional": false,            "field": "token",            "description": "<p>请求接口的token,放在请求头中</p>"          }        ]      }    },    "type": "get",    "url": "/oauth/githubrepo",    "title": "",    "name": "GithubRepo",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "String",            "optional": false,            "field": "refresh",            "description": "<p>默认没有该参数;强制从github获取数据,并更新数据库请求地址:/oauth/githubrepo?refresh=true</p>"          }        ]      }    },    "error": {      "examples": [        {          "title": "Error-Response:",          "content": "{\n  \"msg\": \"OK\",\n  \"result\": [\n    {\n      \"git_uid\": \"6070423\",\n      \"id\": 14,\n      \"is_hook\": 0,\n      \"repo_name\": \"beego\"\n    },\n    {\n      \"git_uid\": \"6070423\",\n      \"id\": 15,\n      \"is_hook\": 0,\n      \"repo_name\": \"crawler\"\n    }\n  ],\n  \"status\": 0\n}\n    成功:result 是一个列表,每一个元素数据是一个代码项目工程,其中 repo_name 是项目名:",          "type": "json"        }      ]    },    "filename": "oauth/github.py",    "group": "_Users_lzp_Desktop_PythonTools_authServer_oauth_github_py",    "groupTitle": "_Users_lzp_Desktop_PythonTools_authServer_oauth_github_py"  },  {    "description": "<p>授权平台可以对某个项目具有 hooks 权限</p>",    "version": "1.0.0",    "header": {      "fields": {        "Header": [          {            "group": "Header",            "type": "String",            "optional": false,            "field": "token",            "description": "<p>请求接口的token,放在请求头中</p>"          },          {            "group": "Header",            "type": "String",            "optional": false,            "field": "varbox",            "description": "<p>需要授权的用户项目</p>"          }        ]      }    },    "type": "post",    "url": "/oauth/githubhooks",    "title": "",    "success": {      "examples": [        {          "title": "Success-Response:",          "content": "{\n  \"msg\": \"OK\",\n  \"result\": {\n    \"active\": true,\n    \"config\": {\n      \"content_type\": \"json\",\n      \"secret\": \"********\",\n      \"url\": \"http://index.boxlinker.com:8080/oauth/webhook\"\n    },\n    \"created_at\": \"2016-10-08T07:24:49Z\",\n    \"events\": [\n      \"push\",\n      \"pull_request\"\n    ],\n    \"id\": 10236269,\n    \"last_response\": {\n      \"code\": null,\n      \"message\": null,\n      \"status\": \"unused\"\n    },\n    \"name\": \"web\",\n    \"ping_url\": \"https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10236269/pings\",\n    \"test_url\": \"https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10236269/test\",\n    \"type\": \"Repository\",\n    \"updated_at\": \"2016-10-08T07:24:49Z\",\n    \"url\": \"https://api.github.com/repos/liuzhangpei/Dockerfile-back/hooks/10236269\"\n  },\n  \"status\": 0\n}",          "type": "json"        }      ]    },    "filename": "oauth/github.py",    "group": "_Users_lzp_Desktop_PythonTools_authServer_oauth_github_py",    "groupTitle": "_Users_lzp_Desktop_PythonTools_authServer_oauth_github_py",    "name": "PostOauthGithubhooks"  }] });
