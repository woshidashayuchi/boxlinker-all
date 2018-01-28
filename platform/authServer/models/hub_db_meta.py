#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/8/15 下午6:31
"""



import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import authServer.conf.db as DB



# 创建对象的基类:
Base = declarative_base()


class UserBase(Base):
    __tablename__ = 'user'
    user_id = sa.Column(sa.String(64), primary_key=True, nullable=False)  # 用户uuid
    username = sa.Column(sa.String(64), unique=True)
    email = sa.Column(sa.String(64), unique=True)
    password = sa.Column(sa.String(40), nullable=False)
    logo = sa.Column(sa.String(126))  # 头像

    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    is_active = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 是否激活
    salt = sa.Column(sa.String(40), default=None)
    sysadmin_flag = sa.Column(sa.Integer)

    creation_time = sa.Column(mysql.TIMESTAMP)
    update_time = sa.Column(mysql.TIMESTAMP)


class ActionCode(Base):
    """ 操作确认码,找回密码,验证码,邮箱注册确认码 """
    __tablename__ = 'action_code'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    user_id = sa.Column(sa.String(64), nullable=False)  # 用户uuid
    opcode = sa.Column(sa.String(32), nullable=False)   # 操作确认码,找回密码,验证码,邮箱注册确认码
    action = sa.Column(sa.String(32), nullable=False)    # 操作类型;动作, 修改密码还是验证邮箱

    creation_time = sa.Column(mysql.TIMESTAMP, nullable=True)  # 添加该记录时间
    expire_time = sa.Column(mysql.TIMESTAMP, nullable=True)    # 过期时间



# class Visit_Token(Base):
#     """ 用户登录token """
#     __tablename__ = 'visit_token'
#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
#
#     tokenid = sa.Column(sa.String(64), nullable=False)  # 随机字符串
#
#     user_id = sa.Column(sa.String(64), nullable=False)  # 用户uuid
#     org_id = sa.Column(sa.String(64), nullable=False)  # 组织 id
#
#     token = sa.Column(sa.Text, nullable=False)
#
#     # 0 token没有进行退出操作,  1进行了操作退出操作,已经失效
#     deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
#
#     creation_time = sa.Column(mysql.TIMESTAMP, nullable=True)  # 添加该记录时间
#     update_time = sa.Column(mysql.TIMESTAMP, nullable=True)    # 更新该记录时间



# 20161223 重新设计
class AccessToken(Base):
    """ 用户登录token """
    __tablename__ = 'access_token'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    user_id = sa.Column(sa.String(64), nullable=False)  # 用户uuid
    user_name = sa.Column(sa.String(64), nullable=False)  # 用户名  new add

    org_id = sa.Column(sa.String(64), nullable=False)  # 组织 id
    org_name = sa.Column(sa.String(64), nullable=False)  # 组织名  new add

    token_uuid = sa.Column(sa.String(64), nullable=False)  # 随机字符串
    token = sa.Column(sa.Text, nullable=False)  # 随机字符串
    role_uuid = sa.Column(sa.Integer, nullable=False)  # add lzp

    create_time = sa.Column(mysql.TIMESTAMP, nullable=True)  # 添加该记录时间
    update_time = sa.Column(mysql.TIMESTAMP, nullable=True)    # 更新该记录时间

    expiration = sa.Column(sa.Integer, nullable=False)    # new add 过期时间; 多长时间之后过期

    #  0 token没有进行退出操作,  1进行了操作退出操作,已经失效
    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))






# 角色表
class Role(Base):
    __tablename__ = 'role'
    role_id = sa.Column(sa.Integer, primary_key=True)
    role_mask = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 角色权限 数字表示
    role_code = sa.Column(sa.String(20))      # 角色权限 字符表示
    role_describe = sa.Column(sa.String(20))  # 角色描述


# 操作行为
class Access(Base):
    __tablename__ = 'access'
    access_id = sa.Column(sa.Integer(), primary_key=True)
    access_code = sa.Column(sa.String(1))
    comment = sa.Column(sa.String(30))

# github 用户认证表
class GitHubOauth(Base):
    __tablename__ = 'github_oauth'
    id = sa.Column(sa.String(64), primary_key=True, nullable=False)

    uid = sa.Column(sa.String(64), nullable=False)
    git_name = sa.Column(sa.String(64))
    git_emain = sa.Column(sa.String(64))
    git_uid = sa.Column(sa.String(20))
    access_token = sa.Column(sa.String(60), nullable=False)
    src_type = sa.Column(sa.String(20), nullable=False)  # 代码来源

    sa.ForeignKeyConstraint(['uid'], [u'user.user_id'], ),

# 20160928 代码源
class CodeRepo(Base):

    __tablename__ = 'code_repo'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    uid = sa.Column(sa.String(64), nullable=False)

    repo_uid = sa.Column(sa.String(64))  # github 用户id
    repo_id = sa.Column(sa.String(64))  # 项目id
    repo_name = sa.Column(sa.String(64))  # 项目名
    repo_branch = sa.Column(sa.String(64))  # 项目名,分支
    repo_hook_token = sa.Column(sa.String(64))  # web hooks token

    html_url = sa.Column(sa.String(256))  # 项目url
    ssh_url = sa.Column(sa.String(256))   # 项目 git clone 地址
    url = sa.Column(sa.String(256))
    description = sa.Column(sa.String(256))

    is_hook = sa.Column(sa.String(1), nullable=False, server_default='0')  # 是否已经被授权hook

    src_type = sa.Column(sa.String(20), nullable=False, server_default='github')  # 代码来源

    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    creation_time = sa.Column(mysql.TIMESTAMP, nullable=True)

    update_time = sa.Column(mysql.TIMESTAMP, nullable=True)

    sa.ForeignKeyConstraint(['uid'], [u'user.user_id'], ),
    sa.ForeignKeyConstraint(['repo_uid'], [u'github_oauth.git_uid'], ),


class ImageRepository(Base):
    """ 镜像仓库 Repository, 无论构建镜像还是用户终端之间上传镜像都要注册在该表中 """
    __tablename__ = 'image_repository'
    uuid = sa.Column(sa.String(64), primary_key=True, nullable=False)  # 镜像uuid

    # uid = sa.Column(sa.ForeignKey(u'user.user_id'), nullable=False, index=True)  # 用户id; 应该用组织id
    uid = sa.Column(nullable=False, index=True)  # 用户id; 应该用组织id
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


class ImageRepositoryBuild(Base):
    """ 代码构建的镜像 """
    __tablename__ = 'image_repository_build'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    image_repository_id = sa.Column(sa.ForeignKey(u'image_repository.uuid'), nullable=False, index=True)  # 镜像仓库id

    # 自动构建
    code_repo_id = sa.Column(sa.ForeignKey(u'code_repo.id'), nullable=False, index=True)  # 关联代码id
    repo_branch = sa.Column(sa.String(20))  # 项目名,分支
    dockerfile_path = sa.Column(sa.String(128))
    dockerfile_name = sa.Column(sa.String(20))
    auto_build = sa.Column(sa.String(20))
    image_tag = sa.Column(sa.String(20))

    # # 构建状态 1:构建成功, 2:构建构建中,  3:构建失败  0: 还未构建
    build_status = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    use_time = sa.Column(sa.String(20))  # 上次构建用时
    last_build = sa.Column(mysql.TIMESTAMP, nullable=True)  # 上次构建时间


class RepositoryEvents(Base):
    """ 仓库事件通知,记录镜像的push/delete操作 """
    __tablename__ = 'repository_events'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    repository = sa.Column(sa.String(128))  # 镜像名
    url = sa.Column(sa.String(256))
    length = sa.Column(sa.String(24))
    tag = sa.Column(sa.String(60))
    actor = sa.Column(sa.String(128))
    action = sa.Column(sa.String(24), server_default="push")

    digest = sa.Column(sa.String(256))
    size = sa.Column(sa.String(256))
    repo_id = sa.Column(sa.String(256))
    source_instanceID = sa.Column(sa.String(256))
    source_addr = sa.Column(sa.String(256))

    deleted = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    creation_time = sa.Column(mysql.TIMESTAMP)
    update_time = sa.Column(mysql.TIMESTAMP)


# class RepositoryEnshrine(Base):
#     """ 镜像收藏列表, 用户id 对应收藏的镜像id """
#     __tablename__ = 'repository_enshrine'
#
#     uid = sa.Column(sa.ForeignKey(u'user.user_id'), nullable=False, index=True)  # 用户id
#     image_repository_id = sa.Column(sa.ForeignKey(u'image_repository.uuid'), nullable=False, index=True)  # 镜像仓库id



class RepositoryPull(Base):
    """ 仓库事件通知,记录镜像的pull操作 """
    __tablename__ = 'repository_pull'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    repository = sa.Column(sa.String(128))  # 镜像名
    url = sa.Column(sa.String(256))
    length = sa.Column(sa.String(24))
    tag = sa.Column(sa.String(60))

    actor = sa.Column(sa.String(128))
    action = sa.Column(sa.String(24), server_default="pull")

    digest = sa.Column(sa.String(256))
    size = sa.Column(sa.String(256))
    repo_id = sa.Column(sa.String(256))
    source_instanceID = sa.Column(sa.String(256))
    source_addr = sa.Column(sa.String(256))

    timestamp = sa.Column(mysql.TIMESTAMP)





# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#connecting  ORM文档



# 镜像资源管理
class ProjectRegistry(Base):
    __tablename__ = 'project_registry'
    project_id = sa.Column(sa.Integer(), primary_key=True)
    project_name = sa.Column(sa.String(20))

    user_id = sa.Column(sa.Integer(), primary_key=True)
    role = sa.Column(sa.Integer(), nullable=False)
    is_admin = sa.Column(sa.Integer, nullable=False, default=1)
    creation_time = sa.Column(mysql.TIMESTAMP, nullable=True)
    sa.ForeignKeyConstraint(['role'], [u'role.role_id'], ),
    sa.ForeignKeyConstraint(['user_id'], [u'user.user_id'], ),



class ImageProjectTeam(Base):
    """镜像项目组,对不同用户授权对私有镜像的访问权限"""
    __tablename__ = 'image_project_team'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    # repositories = sa.Column(sa.ForeignKey(u'image_project.repositories'), nullable=False, index=True)  # 镜像名
    # user_name = sa.Column(sa.ForeignKey(u'user.username'), nullable=False, index=True)  # 用户名
    # role = sa.Column(sa.ForeignKey(u'role.role_code'), nullable=False)  # 角色,权限

    user_note = sa.Column(sa.Text)  # 对于添加组用户的用户备注

    creation_time = sa.Column(mysql.TIMESTAMP)
    update_time = sa.Column(mysql.TIMESTAMP)


class OrgsBase(Base):
    __tablename__ = 'orgs_base'
    org_id = sa.Column(sa.String(64), primary_key=True, nullable=False)  # 组织 id
    org_name = sa.Column(sa.String(64))   # 组织名


    org_detail = sa.Column(sa.Text)       # 组织描述

    # 是否公开;
    # 1-> 公开,     允许非组织成员使用组织名进行搜索,主动提交加入申请(需要,群主或管理员同意)
    # 0-> 完全私有, 只能群主和管理员主动拉去成员加入,而且不允许非组织成员查看组织描述信息
    is_public = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))
    is_delete = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))

    creation_time = sa.Column(mysql.TIMESTAMP)
    delete_time = sa.Column(mysql.TIMESTAMP)



class OrgsUser(Base):
    __tablename__ = 'orgs_user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)

    org_id = sa.Column(sa.ForeignKey(u'orgs_base.org_id'), nullable=False, index=True)  # 组织id
    uid = sa.Column(sa.ForeignKey(u'user.user_id'), nullable=False, index=True)    # 用户id
    username = sa.Column(sa.String(56))    # 用户id

    # access
    role = sa.Column(sa.String(8))  # 权限角色

    confirm_url = sa.Column(sa.String(256))  # 确认加入组织的url链接

    is_confirm = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 用户已经确认加入该组织

    # 组织拥有者具有最高权限: MRWDS
    # 组织一般管理员具有: MRWS 权限(具有处理删除组织以外的所有权限)
    # 组织开发者: RWS 权限

    is_delete = sa.Column(sa.Integer, nullable=False, server_default=sa.text("'0'"))  # 成员是否被删除

    creation_time = sa.Column(mysql.TIMESTAMP)
    update_time = sa.Column(mysql.TIMESTAMP)


def init_data(user_name, email, password, role):
    import uuid
    import authServer.pyTools.token.token as TK
    from authServer.pyTools.tools.timeControl import get_now_time

    try:

        salt = TK.GenerateRandomString(randlen=32)
        save_password = TK.encrypy_pbkdf2(password=password, salt=salt)
        uuid = uuid.uuid3(uuid.NAMESPACE_DNS, user_name).__str__()

        now_time = get_now_time()

        db_session = Session()



        user_base = UserBase(user_id=uuid, username=user_name, email=email,
                             password=save_password, creation_time=now_time,
                             update_time=now_time, salt=salt)
        db_session.add(user_base)
        db_session.commit()
    except Exception as msg:
        print msg.message
        return False


    try:
        # 默认组织名和用户名一样
        org_base = OrgsBase(org_id=uuid, org_name=user_name, creation_time=now_time)
        db_session.add(org_base)
        db_session.commit()
    except Exception as msg:
        user_b = UserBase(user_id=uuid)
        db_session.delete(user_b)
        db_session.commit()
        db_session.close()
        return False

    try:
        org_user = OrgsUser(org_id=uuid, uid=uuid, username=user_name,
                            role=role, creation_time=now_time, update_time=now_time)
        db_session.add(org_user)
        db_session.commit()
        return True
    except Exception as msg:
        org_base = OrgsBase(org_id=uuid)
        db_session.delete(org_base)
        db_session.commit()

        user_b = UserBase(user_id=uuid)
        db_session.delete(user_b)
        db_session.commit()
        db_session.close()
        return False



print "create_engine begin"
engine = create_engine(DB.hub_db.mysql_engine, echo=True)  # , encoding='utf8', pool_size=30, max_overflow=20)
Session = sessionmaker(bind=engine)
print "create_engine sessionmaker end"

def init_create_hub_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
    # 否则你就必须在调用 init_db() 之前导入它们。
    print "init_create_hub_db"
    Base.metadata.create_all(bind=engine, checkfirst=True)



