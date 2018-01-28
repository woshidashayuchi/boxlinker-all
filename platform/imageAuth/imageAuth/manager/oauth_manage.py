#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/21 15:40
"""

import time

from pyTools.token.token import gen_token, make_random_key

import conf.oauthConf as openOauth

from common.code import request_result
from common.logs import logging as log

import imageAuth.manager.githubApi as githubApi
import imageAuth.manager.CodingApi as CodingApi
import imageAuth.db.oauth_db as DBMG

class CodeOauthManager(object):
    def __init__(self):
        self.oauthdb = DBMG.OauthDbManager()

    def DelOauthStatus(self, team_uuid, src_type):
        """ 取消绑定 """

        retbool, oauthret = self.oauthdb.get_code_oauth(team_uuid=team_uuid, src_type=src_type)
        if retbool is False:
            return request_result(0)

        code_repo = self.oauthdb.get_code_repo(team_uuid=team_uuid, src_type=src_type)
        if code_repo is None:
            return request_result(0)

        for node in code_repo:
            if '1' == node.is_hook:
                # user_name, project_name, access_token, hook_url_del
                CodingApi.DellAllWebHooksByProjectName(oauthret.git_name, node.repo_name,
                                                       oauthret.access_token, node.hook_url)

        self.oauthdb.del_code_repo(team_uuid=team_uuid, src_type=src_type)
        self.oauthdb.del_code_oauth(team_uuid=team_uuid, src_type=src_type)

        return request_result(0)

    def OauthStatue(self, team_uuid):
        """ 获取Oauth绑定状态 """
        src_type_dict = self.oauthdb.get_code_oauth_type(team_uuid=team_uuid)
        return request_result(0, ret=src_type_dict)

    def update_code_oauth(self, team_uuid, token, src_type, update_token=False):
        """更新  CodeOauth 中的用户信息"""
        if src_type == 'github':
            retbool, git_name, git_uid, git_emain = githubApi.get_github_user_some_info(token=token)
        elif src_type == 'coding':
            retbool, git_name, git_uid, git_emain = CodingApi.get_coding_user_some_info(access_token=token)
        else:
            return False, None

        if retbool is False:
            return False, None

        if update_token:
            retbool = self.oauthdb.update_code_oauth(team_uuid=team_uuid, src_type=src_type, git_name=git_name,
                                                     git_emain=git_name, git_uid=git_uid, access_token=token)
        else:
            retbool = self.oauthdb.update_code_oauth_only_user(team_uuid=team_uuid, src_type=src_type,
                                                               git_name=git_name, git_emain=git_name, git_uid=git_uid)

        if retbool is False:
            return False, None
        return True, (git_name, git_uid, git_emain)


    def get_code_oauth_info(self, team_uuid, src_type):
        """ 根据组织uuid 和 第三方类型, 获取 CodeOauth , 返回"""
        retbool, oauthret = self.oauthdb.get_code_oauth(team_uuid=team_uuid, src_type=src_type)

        if retbool is False:
            return False, None
        access_token = oauthret.access_token
        if access_token is None or '' == access_token:
            return False, None

        git_name = oauthret.git_name
        git_uid = oauthret.git_uid
        git_emain = oauthret.git_emain

        # 还没有获取用户信息,需要获取用户信息并更新到数据表
        # if git_name is None or ret.git_emain is None or git_uid is None:
        if git_name is None or git_uid is None:  # 对于不显示email的用户设置，无法得到用户邮箱
            retbool, git_name, git_uid, git_emain = self.update_code_oauth(team_uuid=team_uuid,
                                              src_type=src_type, token=access_token)
        return retbool, (access_token, git_name, git_uid, git_emain)




class OauthUrlManager(object):
    def __init__(self):
        log.info('OauthUrlManager __init__')

    def create_oauth_url(self, team_uuid, src_type, redirect_url):
        """ 生成带有用户信息的url认证地址, state 码 """
        state_msg = {
            'team_uuid': str(team_uuid),  # 组织uuid
            'src_type': src_type,  # 第三方平台类型, github, coding
            'redirect_url': redirect_url,
            'expires': time.time() + 30 * 24 * 60 * 60
        }

        state_ret = gen_token(key=openOauth.SECRET_KEY, data=state_msg)

        state_ret = state_ret.replace('=', '.')  # coding 无故吃掉 =

        log.info('create_oauth_url state_ret: %s' % (state_ret))

        if src_type == "github":
            return openOauth.user_oauth_url.format(state_ret)
        elif 'coding' == src_type:
            return openOauth.coding_oauth_url.format(state_ret)
        else:
            return None

    def get_oauth_url(self, team_uuid, src_type, redirect_url):
        url_state = self.create_oauth_url(team_uuid, src_type, redirect_url)
        if url_state is None:
            return request_result(101)
        return request_result(0, ret=url_state)


class CallBackManager(object):
    def __init__(self):
        self.CodeOauthManager = CodeOauthManager()
        self.oauthdb = DBMG.OauthDbManager()

    # coding 回调
    def callback_coding(self, code):

        token = CodingApi.get_token_by_code(client_id=openOauth.coding_client_id,
                                            client_secret=openOauth.coding_client_secret, code=code)
        return token

    def callback_git(self, code):
        token = githubApi.get_token_by_code(code=code, client_id=openOauth.github_client_id,
                                            client_secret=openOauth.github_client_secret)
        return token

    def callback(self, src_type, code, team_uuid):
        if 'github' == src_type:
            token = self.callback_git(code=code)
        elif 'coding' == src_type:
            token = self.callback_coding(code=code)
        else:
            return request_result(101)

        retbool, oauthret = self.oauthdb.get_code_oauth(team_uuid=team_uuid, src_type=src_type)
        if retbool is False:  # 把 token 存起来
            self.oauthdb.save_access_token(team_uuid=team_uuid, src_type=src_type, access_token=token)
            ret = self.CodeOauthManager.update_code_oauth(team_uuid=team_uuid, token=token, src_type=src_type)
        else:
            ret = self.CodeOauthManager.update_code_oauth(team_uuid=team_uuid, token=token, src_type=src_type, update_token=True)

        return ret


class WebHookManager(object):
    """ Web Hook 管理 """
    def __init__(self):
        self.oauthdb = DBMG.OauthDbManager()
        self.CodeOauthManager = CodeOauthManager()
        self.callback = CallBackManager()


    def SetCodingHook(self, git_name, repo_name, team_uuid, access_token, del_hooks=True):
        """ 设置 coding web hooks """

        # 暂时不删除
        if del_hooks:
            CodingApi.DellAllWebHooksByProjectName(git_name, repo_name, access_token, hook_url_del=openOauth.OAUTH_WEBHOOKS)

        random_key = make_random_key()

        retbool, result = CodingApi.WebHookAdd(
            user_name=git_name, project_name=repo_name,
            access_token=access_token, hook_url=openOauth.OAUTH_WEBHOOKS, hook_token=random_key)

        if retbool is False:
            return request_result(100, ret=result)

        log.info("--->result: %s" % (result))
        log.info("--->team_uuid: %s" % (team_uuid))
        log.info("--->repo_name: %s" % (repo_name))
        log.info("--->random_key: %s" % (random_key))

        self.oauthdb.update_code_repo_web_hook(team_uuid=team_uuid, repo_name=repo_name,
                                               repo_hook_token=random_key, hook_url=openOauth.OAUTH_WEBHOOKS, src_type='coding')
        log.info(" update_code_repo_web_hook is ok")


        try:
            # 设置部署公钥
            retbool, result = CodingApi.RsaKeyAdd(user_name=git_name, project_name=repo_name, access_token=access_token)
            if retbool is False:
                return request_result(100, ret=result)
            return request_result(0)
        except Exception, e:
            log.error(' RsaKeyAdd is error: %s' % (e))
            return request_result(403)

        return request_result(0)




    def create_web_hook(self, team_uuid, src_type, repo_name):
        retbool, result = self.CodeOauthManager.get_code_oauth_info(team_uuid=team_uuid, src_type=src_type)
        if retbool is False:
            return request_result(601)
        access_token, git_name, git_uid, git_emain = result

        self.SetCodingHook(git_name, repo_name, team_uuid, access_token, del_hooks=True)
        return request_result(0)


class OauthCodeRepoManager(object):
    """ 代码项目管理 """
    def __init__(self):
        self.oauthdb = DBMG.OauthDbManager()
        self.CodeOauthManager = CodeOauthManager()

    def GetCodeRepoList(self, src_type, team_uuid, refresh=False):
        """ 从数据库中, 获取代码项目 """


        retbool, oauthret = self.oauthdb.get_code_oauth(team_uuid=team_uuid, src_type=src_type)
        if retbool is False:
            return request_result(0)


        code_repo = self.oauthdb.get_code_repo(team_uuid=team_uuid, src_type=src_type)
        if code_repo is None and refresh:
            return request_result(0)

        if refresh is False:
            return self.refresh_repos(team_uuid=team_uuid, src_type=src_type)
        repo_list = list()
        for node in code_repo:
            repo_list.append(
                {'repo_name': node.repo_name, 'git_uid': node.repo_uid, 'is_hook': node.is_hook,
                 'id': node.code_repo_uuid, 'html_url': node.html_url, 'ssh_url': node.ssh_url,
                 'url': node.git_url, 'description': node.description, 'git_name': oauthret.git_name})
        return request_result(0, ret=repo_list)

    def refresh_repos(self, team_uuid, src_type='coding'):
        """ 刷新 github 代码列表 """
        retbool, codeOauth = self.oauthdb.get_code_oauth(team_uuid, src_type)
        if retbool is False:
            return request_result(701)
        access_token = codeOauth.access_token
        git_name = codeOauth.git_name

        code, ret_json = CodingApi.GetRepoList(access_token=access_token)
        if code is False:
            return ret_json
        ret_json = ret_json['data']['list']  # coding 和 github 结构不一样

        ret, codeOauth = self.oauthdb.get_code_repo_repo_id(team_uuid=team_uuid, src_type=src_type)
        self.oauthdb.set_all_code_repo_deleted(team_uuid=team_uuid, src_type=src_type)
        for node in ret_json:
            log.info("node--> %s" % (node))
            temp = dict()
            repo_id = str(node['id'])
            default_branch = ''
            html_url = node['https_url']
            temp['team_uuid'] = team_uuid
            temp['repo_uid'] = node['owner_id']
            temp['repo_id'] = repo_id
            temp['repo_name'] = node['name']

            temp['repo_branch'] = default_branch
            temp['html_url'] = html_url
            temp['ssh_url'] = node['ssh_url']
            temp['git_url'] = node['git_url']
            temp['src_type'] = src_type
            temp['description'] = node['description']
            try:
                if codeOauth is not None and str(repo_id) in codeOauth:
                    log.info('old data do modify')
                    self.oauthdb.modify_code_repo_dict(temp)  # 修改
                else:
                    log.info('new data do insert')
                    self.oauthdb.add_code_repo_dict(temp)
            except Exception, e:
                log.error('refresh_repos is error: %s' % (e))
                return request_result(403)

        self.oauthdb.del_code_repo_deleted(team_uuid=team_uuid, src_type=src_type)
        return self.GetCodeRepoList(team_uuid=team_uuid, src_type=src_type, refresh=True)

if __name__ == '__main__':
    OUM = OauthCodeRepoManager()

    ret = OUM.GetCodeRepoList(team_uuid='2e8e7b37-a957-4770-9075-aaa67eaa49ce', src_type='coding')
    print ret

    # HOOKS = WebHookManager()
    # HOOKS.create_web_hook(team_uuid='2e8e7b37-a957-4770-9075-aaa67eaa49ce', src_type='github', repo_name='3des')