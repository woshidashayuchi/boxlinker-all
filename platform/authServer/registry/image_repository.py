#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 16/10/12 11:01
@func: 镜像仓库 相关
"""


import time
import json
import uuid

from flask import g, request

from authServer.common.decorate import request_form_get_tokenid_token, get_token_from_headers_check

from authServer.tools.decorate import get_username_uid_by_payload

from authServer.common.oauthclient.githubApi import SetGitHook

from authServer.models.hub_db_meta import ImageRepository, CodeRepo, ImageRepositoryBuild, RepositoryEvents,UserBase

from authServer.pyTools.tools.codeString import request_result


from authServer.v1.repository.RepositoryBuildMsg import get_repository_build

from authServer.oauth.send_build_msg import send_build_rabbit_by_repouuid


# 等到一个镜像的详情
def get_repository_info(user_name, uid, repository_id):
    print 'get_repository_info(user_name, uid, repository_id)'

    print repository_id

    image_repo = g.db_session.query(ImageRepository).filter(
        ImageRepository.uuid == str(repository_id),
        #ImageRepository.uid == str(uid),
        ImageRepository.deleted == 0).first()

    if image_repo is None:
        return request_result(809, ret="Resources does not exist or has been deleted")

    ret_d = dict()
    ret_d['repository'] = image_repo.repository
    ret_d['creation_time'] = image_repo.creation_time
    ret_d['update_time'] = image_repo.update_time
    ret_d['is_public'] = image_repo.is_public
    ret_d['short_description'] = image_repo.short_description
    ret_d['detail'] = image_repo.detail
    ret_d['download_num'] = image_repo.download_num
    ret_d['enshrine_num'] = image_repo.enshrine_num
    ret_d['review_num'] = image_repo.review_num
    ret_d['pushed'] = image_repo.pushed
    ret_d['is_code'] = image_repo.is_code

    ret_d['download_num'] = image_repo.download_num  # 下载次数


    if str(image_repo.is_code) == '1':
        image_repo_build = g.db_session.query(ImageRepositoryBuild).filter(
            ImageRepositoryBuild.image_repository_id == repository_id).first()
        if image_repo_build is not None:
            ret_d['code_repo_id'] = image_repo_build.code_repo_id
            ret_d['repo_branch'] = image_repo_build.repo_branch
            ret_d['dockerfile_path'] = image_repo_build.dockerfile_path
            ret_d['dockerfile_name'] = image_repo_build.dockerfile_name
            ret_d['auto_build'] = image_repo_build.auto_build
            ret_d['image_tag'] = image_repo_build.image_tag
            ret_d['build_status'] = image_repo_build.build_status
            ret_d['use_time'] = image_repo_build.use_time
            ret_d['last_build'] = image_repo_build.last_build

    repo_event = g.db_session.query(RepositoryEvents).filter(RepositoryEvents.repository == image_repo.repository).all()

    repo_tags = list()
    for repo_event_node in repo_event:
        tag_temp = dict()
        tag_temp['url'] = repo_event_node.url
        tag_temp['length'] = repo_event_node.length
        tag_temp['tag'] = repo_event_node.tag
        tag_temp['actor'] = repo_event_node.actor
        tag_temp['action'] = repo_event_node.action
        tag_temp['digest'] = repo_event_node.digest

        tag_temp['repo_id'] = repo_event_node.repo_id

        tag_temp['creation_time'] = repo_event_node.creation_time
        tag_temp['update_time'] = repo_event_node.update_time
        repo_tags.append(tag_temp)

    ret_d['tags'] = repo_tags

    return request_result(0, ret=ret_d)





def request_image_repository_create(func):
    """ 获取新建仓库的名称、公有还是私有、简单描述、详细描述,进行装饰器解析, 并且验证 repositories 是否存在 """
    def _deco(*args, **kwargs):
        try:
            data = request.data
            data_json = json.loads(data)
            is_public = data_json.get('is_public', '').decode('utf-8').encode('utf-8')
            short_description = data_json.get('short_description', '')#.decode('utf-8').encode('utf-8')
            detail = data_json.get('detail', '')#.decode('utf-8').encode('utf-8')
            repository = data_json.get('repository', '').decode('utf-8').encode('utf-8')  # 仓库名称

            # 是否是代码构建的镜像; 0-->手动创建push;  1-->代码自动构建镜像
            is_code = data_json.get('is_code', '').decode('utf-8').encode('utf-8')

            # 自动构建
            repo_name = data_json.get('repo_name', '').decode('utf-8').encode('utf-8')
            repo_branch = data_json.get('repo_branch', '').decode('utf-8').encode('utf-8')
            image_tag = data_json.get('image_tag', '').decode('utf-8').encode('utf-8')  # 镜像标签
            dockerfile_path = data_json.get('dockerfile_path', '').decode('utf-8').encode('utf-8')
            dockerfile_name = data_json.get('dockerfile_name', '').decode('utf-8').encode('utf-8')
            auto_build = data_json.get('auto_build', '').decode('utf-8').encode('utf-8')
            src_type = data_json.get('src_type', '').decode('utf-8').encode('utf-8')

        except Exception as msg:
            return request_result(710, ret=msg.message)


        # 传入的参数有问题
        if str(is_public) != '0' and str(is_public) != '1':
            return request_result(706, ret='is_public is error')

        if str(is_code) != '0' and str(is_code) != '1':
            is_code = '0'
            # 暂时这样处理
            # return request_result(706, ret='is_code is error')

        from authServer.conf.openOauth import OpenType
        if src_type is not OpenType:

            print "ssss-d-sd-s-d-s  src_type"
            print src_type
            print OpenType
            print type(OpenType)
            print type(src_type)
            return request_result(706, ret='src_type not is coding or github')

        if repository is '' or '/' in repository:  # 镜像仓库名不合法
            return request_result(706, ret='repositories is error null or / ' )

        if str(is_code) == '1':  # 属于代码构建项目,代码信息不可以缺少
            if (repo_name and repo_branch and image_tag and
                    dockerfile_path and dockerfile_name and auto_build) is '':
                return request_result(706)

            if (str(auto_build) == '0' or str(auto_build) == '1') is False:
                return request_result(706)

        kwargs['is_public'] = str(is_public)
        kwargs['short_description'] = short_description
        kwargs['detail'] = detail
        kwargs['repository'] = kwargs['user_name'] + '/' + repository  # 前端页面传进来是不含有  用户名 和 /

        kwargs['is_code'] = str(is_code)

        # 代码信息
        kwargs['repo_name'] = repo_name
        kwargs['repo_branch'] = repo_branch
        kwargs['image_tag'] = image_tag

        kwargs['dockerfile_path'] = dockerfile_path
        kwargs['dockerfile_name'] = dockerfile_name
        kwargs['auto_build'] = auto_build
        kwargs['src_type'] = src_type

        return func(*args, **kwargs)
    return _deco


def image_repository_create_check_repo(func):
    """ 新建镜像仓库时检验仓库名是否合法,不存在则合法 """
    def _deco(*args, **kwargs):
        ret = g.db_session.query(ImageRepository).filter(ImageRepository.repository == kwargs['repository']).first()
        if ret is not None:
            return request_result(706, ret='repository_name is exist')
        return func(*args, **kwargs)
    return _deco



from authServer.common.decorate import check_headers, get_userinfo_by_payload
@check_headers
@get_userinfo_by_payload
# @get_token_from_headers_check
# @get_username_uid_by_payload
@request_image_repository_create
@image_repository_create_check_repo
def ImageRepositoryCreate(*args, **kwargs):
    try:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        repo_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, kwargs['repository']).__str__()

        kwargs['image_repo_uuid'] = repo_uuid

        image_repo = ImageRepository(
            uuid=repo_uuid, uid=kwargs['uid'], repository=kwargs['repository'],
            creation_time=now, update_time=now,
            is_public=kwargs['is_public'], short_description=kwargs['short_description'],
            detail=kwargs['detail'], is_code=kwargs['is_code'], src_type=kwargs['src_type'])

        g.db_session.add(image_repo)
        g.db_session.commit()

    except Exception as msg:
        print "is error"
        print msg.message
        print msg.args
        for va in msg.args:
            print va
        return request_result(401, ret=msg.message)

    build_create_ret = ImageRepositoryBuildCreate(*args, **kwargs)
    if build_create_ret['status'] == 0:
        print "ret['status']"
        return request_result(0, ret={"uuid": repo_uuid})

    # 创建 代码构建配置信息错误
    try:
        image_repo_del = ImageRepository(uuid=repo_uuid)
        g.db_session.delete(image_repo_del)
        return request_result(714, ret=build_create_ret)
    except Exception as msg:
        return request_result(404, ret=msg.message)


def ImageRepositoryBuildCreate(*args, **kwargs):
    """ 添加ImageRepositoryBuild 记录"""

    if kwargs['is_code'] == '0':  # 不是代码构建项目
        return request_result(0)

    uid = kwargs['uid']
    user_name = kwargs['user_name']
    images_name = kwargs['repository']  # username/ubuntu ; boxlinker/ubuntu

    from authServer.models.db_opt import git_hub_oauth

    github_oauth = git_hub_oauth(uid=uid)
    if github_oauth is None:
        return request_result(103)

    code_repo = g.db_session.query(CodeRepo).filter(
        CodeRepo.uid == uid, CodeRepo.repo_name == kwargs['repo_name'], CodeRepo.src_type == kwargs['src_type']).first()

    if code_repo is None:
        return request_result(404)

    try:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        image_repo_build = ImageRepositoryBuild(
            # image_repo_uuid
            image_repository_id=kwargs['image_repo_uuid'],
            code_repo_id=code_repo.id,
            repo_branch=kwargs['repo_branch'], dockerfile_path=kwargs['dockerfile_path'],
            dockerfile_name=kwargs['dockerfile_name'], auto_build=kwargs['auto_build'],
            image_tag=kwargs['image_tag'])

        g.db_session.add(image_repo_build)
        g.db_session.commit()
    except Exception as msg:
        print msg.message

        return request_result(403, ret=msg.message)

    if code_repo.is_hook != '1':
        if kwargs['src_type'] == 'github':
            ret = SetGitHook(github_oauth.git_name, kwargs['repo_name'], github_oauth.access_token, uid)
        elif kwargs['src_type'] == 'coding':
            from authServer.common.oauthclient.webhooks import SetWebHook
            SetWebHook(github_oauth.git_name, repo_name=kwargs['repo_name'],
                       access_token=github_oauth.access_token, uid=uid, src_type=kwargs['src_type'])
        else:
            return request_result(706, ret='src_type is error ')

    if str(kwargs['auto_build']) == '1':
        send_build_rabbit_by_repouuid(kwargs['image_repo_uuid'])
    return request_result(0)





@get_token_from_headers_check
@get_username_uid_by_payload
def delete_image_project(user_name, uid):  # 删除镜像
    try:
        image_name = request.args.get('imagename', '').decode('utf-8').encode('utf-8')#.lower()
    except Exception as msg:
        return request_result(706, ret=msg.message)

    if image_name == '':
        return request_result(706)

    try:
        image_repo = g.db_session.query(ImageRepository).filter(ImageRepository.repository == image_name).first()

        if image_repo is None:
            return request_result(809, ret="image no have")

        if image_repo.uid != str(uid):
            return request_result(806)

        g.db_session.query(ImageRepository).filter(ImageRepository.repository == image_name,
                                                   ImageRepository.uid == str(uid)
                                                   ).update({"deleted": '1'})
        g.db_session.commit()
    except Exception as msg:
        return request_result(403, ret=msg.message)

    return request_result(0)




@get_token_from_headers_check
@get_username_uid_by_payload
def list_image_project(user_name, uid):

    # 我的镜像 还是  平台镜像
    try:
        public_a = request.args.get('is_public', '').decode('utf-8').encode('utf-8').lower()
    except Exception as msg:
        return request_result(706, ret=msg.message)

    try:
        # 获取代码构建项目
        is_code_arg = request.args.get('is_code', '').decode('utf-8').encode('utf-8').lower()
        if is_code_arg == 'true':
            print 'is true'
            return get_repository_build(user_name, uid)
    except Exception as msg:
        return request_result(706, ret=msg.message)


    # only=true&repository_id=151d5b0d-146e-3f6b-9283-f4cec260dbd4
    try:
        # 获取代码构建项目
        only_repo = request.args.get('only', '').decode('utf-8').encode('utf-8').lower()

        repository_id = request.args.get('repository_id', '').decode('utf-8').encode('utf-8').lower()
        if only_repo == 'true' and repository_id == '':
            return request_result(706, ret='repository_id is null')
        elif only_repo == 'true' and repository_id != '':
            return get_repository_info(user_name, uid, repository_id)
    except Exception as msg:
        print msg.message
        return request_result(706, ret=msg.message)


    try:

        if public_a == 'true':
            image_repo = g.db_session.query(ImageRepository).filter(
                ImageRepository.deleted == '0',
                ImageRepository.is_public == '1').all()
            # 构建镜像暂时没有 is_public 标记
        else:
            image_repo = g.db_session.query(ImageRepository).filter(
                ImageRepository.uid == uid, ImageRepository.deleted == '0').all()
    except Exception as msg:
        print msg.message
        return request_result(404, ret=msg.message)

    retlist = list()
    for image_project_node in image_repo:
        temp_d = dict()
        temp_d['uuid'] = image_project_node.uuid
        temp_d['repository'] = image_project_node.repository
        temp_d['creation_time'] = image_project_node.creation_time
        temp_d['update_time'] = image_project_node.update_time
        temp_d['is_public'] = image_project_node.is_public
        temp_d['short_description'] = image_project_node.short_description  # 简单描述
        temp_d['detail'] = image_project_node.detail  # #  # 详细描述
        # temp_d['auto_build'] = image_project_node.auto_build  # 是否自动构建
        temp_d['type'] = image_project_node.is_code  # 0-->手动推送;   1-->代码构建
        temp_d['download_num'] = image_project_node.download_num  # 下载次数



        retlist.append(temp_d)

    return request_result(0, ret=retlist)




@get_token_from_headers_check
@get_username_uid_by_payload
def modify_image_project(user_name, uid):
    try:
        data = request.data
        data_json = json.loads(data)
    except Exception as msg:
        return request_result(710, ret=msg.message)

    uuid = data_json.get('uuid', '').decode('utf-8').encode('utf-8')  # 镜像id
    is_public = data_json.get('is_public', '').decode('utf-8').encode('utf-8')
    detail = data_json.get('detail', '')#.decode('utf-8').encode('utf-8')
    short_description = data_json.get('short_description', '')#.decode('utf-8').encode('utf-8')

    if (str(is_public) == '0' or str(is_public) == '1') is False:
        return request_result(706, ret='is_public is 0/1 ')

    if str(uuid) == '':
        return request_result(706, ret='uuid is null ')

    try:
        # 不可以修改他人的镜像详情
        g.db_session.query(ImageRepository).filter(ImageRepository.uid == uid, ImageRepository.uuid == str(uuid)).update(
            {"is_public": is_public, "detail": detail, "short_description": short_description}
        )
        g.db_session.commit()
        ret = request_result(0)
    except Exception as msg:
        ret = request_result(403, ret=msg.message)
    finally:
        return ret

