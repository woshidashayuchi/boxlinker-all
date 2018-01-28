#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/2/28 14:07
@ orm 数据结构
"""




import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 资源的acl控制
class ResourcesAcl(Base):
    """ 资源的acl控制 """
    __tablename__ = 'resources_acl'
    resource_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)
    resource_type = sa.Column(sa.String(64), primary_key=True, nullable=False)
    admin_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)
    team_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)
    project_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)
    user_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)

    create_time = sa.Column(mysql.TIMESTAMP, nullable=True)
    update_time = sa.Column(mysql.TIMESTAMP, nullable=True)



class ImageRepository(Base):
    """ 镜像仓库 Repository, 无论构建镜像还是用户终端之间上传镜像都要注册在该表中 """
    __tablename__ = 'image_repository'
    image_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)  # 镜像uuid

    team_uuid = sa.Column(sa.String(64), nullable=False, index=True)  # 组织uuid
    repository = sa.Column(sa.String(126), nullable=False, primary_key=True, index=True)  # 镜像名 boxlinker/xxx
    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 是否被删除
    creation_time = sa.Column(mysql.TIMESTAMP, nullable=True)  # 创建时间
    update_time = sa.Column(mysql.TIMESTAMP, nullable=True)  # 更新时间
    is_public = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 是否公开
    short_description = sa.Column(sa.String(256))  # 简单描述
    detail = sa.Column(sa.Text)  # 详细描述
    download_num = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 下载次数
    enshrine_num = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 收藏次数
    review_num = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))    # 评论次数
    version = sa.Column(sa.String(64))  # 版本,[字典格式存储]
    latest_version = sa.Column(sa.String(30))  # 最新版本
    pushed = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))   # 是否已经被推送,0->还没; 1->已经
    is_code = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 是否是代码构建的镜像仓库

    logo = sa.Column(sa.String(126), server_default='')  # 头像

    src_type = sa.Column(sa.String(30))  # 代码类型


class RepositoryEvents(Base):
    """ 仓库事件通知,记录镜像的push/delete操作 """
    __tablename__ = 'repository_events'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    repository = sa.Column(sa.String(128))  # 镜像名
    url = sa.Column(sa.String(256))
    lengths = sa.Column(sa.String(24))
    tag = sa.Column(sa.String(60))
    actor = sa.Column(sa.String(128))
    actions = sa.Column(sa.String(24), server_default="push")

    digest = sa.Column(sa.String(256))
    sizes = sa.Column(sa.String(256))
    repo_id = sa.Column(sa.String(256))
    source_instanceID = sa.Column(sa.String(256))
    source_addr = sa.Column(sa.String(256))

    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    creation_time = sa.Column(mysql.TIMESTAMP)
    update_time = sa.Column(mysql.TIMESTAMP)




# 第三方认证, 用户认证表
class CodeOauth(Base):
    __tablename__ = 'code_oauth'
    code_oauth_uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)
    team_uuid = sa.Column(sa.String(64), nullable=False)  # 和组织相关, 不要绑定用户
    src_type = sa.Column(sa.String(20), nullable=False)  # 代码来源

    git_name = sa.Column(sa.String(64))
    git_emain = sa.Column(sa.String(64))
    git_uid = sa.Column(sa.String(20))
    access_token = sa.Column(sa.String(60))

# code_oauth  code_repo


# 20160928 代码源
class CodeRepo(Base):

    __tablename__ = 'code_repo'
    code_repo_uuid = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    team_uuid = sa.Column(sa.String(64), nullable=False)

    repo_uid = sa.Column(sa.String(64))  # github 用户id
    repo_id = sa.Column(sa.String(64))  # 项目id
    repo_name = sa.Column(sa.String(64))  # 项目名
    repo_branch = sa.Column(sa.String(64))  # 项目名,分支
    repo_hook_token = sa.Column(sa.String(64))  # web hooks token

    hook_id = sa.Column(sa.String(256))  # web hook id,删除和修改时用

    html_url = sa.Column(sa.String(256))  # 项目 url
    ssh_url = sa.Column(sa.String(256))   # 项目 git clone 地址
    git_url = sa.Column(sa.String(256))
    description = sa.Column(sa.String(256))

    is_hook = sa.Column(sa.String(1), nullable=False, server_default='0')  # 是否已经被授权hook


    src_type = sa.Column(sa.String(20), nullable=False, server_default='github')  # 代码来源

    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    creation_time = sa.Column(mysql.TIMESTAMP, nullable=True)
    update_time = sa.Column(mysql.TIMESTAMP, nullable=True)