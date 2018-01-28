#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/21 10:31
"""


"""
@apiDefine CODE_IMAGE_REPO_0
@apiSuccessExample 返回:
{
    "msg": "OK",
    "result": "4bd1ca3f-1752-33e6-b8d0-b9348a58ced7",
    "status": 0
}

失败

{
    "msg": "There is no resources",
    "result": {},
    "status": 701
}

"""

# 平台镜像返回
"""
@apiDefine CODE_IMAGE_REPO_PUB_LIST_0
@apiSuccessExample 返回:
{
    "msg": "OK",
    "result": {
        "count": 1,
        "current_size": 1,
        "page": 1,
        "page_size": 2,
        "result": [
            {
                "creation_time": "2017-02-20 10:57:15",
                "detail": "Push the mirror between terminals",
                "download_num": 7,
                "is_public": 1,
                "logo": "https://boxlinker-images.oss-cn-beijing.aliyuncs.com/repository/1487560040234pause.png",
                "repository": "zhangsan/pause",
                "short_description": "Push the mirror between terminals",
                "type": 0,
                "update_time": "2017-02-20 10:57:15",
                "uuid": "4bd1ca3f-1752-33e6-b8d0-b9348a58ced7"
            },
            ... ...
        ]
    },
    "status": 0
}
"""


""" 镜像详情 """
"""
@apiDefine CODE_IMAGE_REPO_DETAIL_0
@apiSuccessExample 返回:
{
    "msg": "OK",
    "result": {
        "creation_time": "2017-02-20 17:32:25",
        "detail": "Push the mirror between terminals",
        "download_num": 1,
        "enshrine_num": 0,
        "is_code": 0,
        "is_public": 0,
        "logo": "https://boxlinker-images.oss-cn-beijing.aliyuncs.com/repository/default.png",
        "pushed": 0,
        "repository": "zhangsan/pause",
        "review_num": 0,
        "short_description": "Push the mirror between terminals",
        "tags": [
            {
                "action": "push",
                "actor": "liuzhangpei",
                "creation_time": "2017-02-20 17:32:21",
                "digest": "sha256:f08f3ef4886ad27a80682c1e55ede2dbe8a801c521db07859b829101488f7d83",
                "length": "733",
                "repo_id": "f78ed339-f5c6-4072-a55d-768960d35a44",
                "tag": "2.0",
                "update_time": "2017-02-20 17:32:21",
                "url": "https://index.boxlinker.com/v2/zhangsan/pause/manifests/sha256:f08f3ef4886ad27a80682c1e55ede2dbe8a801c521db07859b829101488f7d83"
            }
        ],
        "update_time": "2017-02-20 17:32:25"
    },
    "status": 0
}

"""

""" 操作成功,只需要返回成功码"""
"""
@apiDefine CODE_IS_OK_0
@apiSuccessExample 返回:
{
    "msg": "OK",
    "result": {},
    "status": 0
}
"""


# 公开信息的获取
"""
@apiDefine CODE_IMAGE_REPO_DETAIL_1
@apiSuccessExample 返回:
{
    "msg": "OK",
    "result":
    {
        "image_uuid': "4bd1ca3f-1752-33e6-b8d0-b9348a58ced7",
         "tag": "2.0",
         "image_name": "zhangsan/pause"
    },
    "status": 0
}

"""

"""
@api {put} https://imageauth.boxlinker.com  0.1
@apiName host
@apiGroup Global Setup
@apiVersion 1.0.0
@apiDescription 修改镜像详情
"""




""" 操作成功,获取代码列表"""
"""
@apiDefine LIST_CODE_REPO
@apiSuccessExample 返回:
{
    "msg": "OK",
    "status": 0,
    "result": [
        {
            "git_name": "ss", 
            "description": "Docker Official Image packaging for WordPress () test"
            "url": "git://github.com/liuzhangpei/wordpress.git"
            "html_url": "https://github.com/liuzhangpei/wordpress"
            "git_uid": "6070423"
            "ssh_url": "git@github.com:liuzhangpei/wordpress.git"
            "is_hook": "0"
            "id": 28,
            "repo_name": "wordpress'
        },
    ]
}
"""