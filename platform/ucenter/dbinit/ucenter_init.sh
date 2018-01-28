#!/bin/bash

db_server='127.0.0.1'
db_port=3306
database='ucenter'

v_connect_mysql="/usr/bin/mysql -h $db_server -P $db_port -ucloud -pcloud -D $database -e"

while [ -z $root_pwd ]
do
  read -p '请输入mysql数据库root密码:[password]'
  root_pwd=$REPLY
  if [ -z $root_pwd ]; then
    continue
  fi
#判断输入的root密码是否可以正常登陆
  mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "quit"
  if [ $? -ne 0 ]; then
    echo 'mysql数据库无法登陆，请检查数据库状态和密码输入是否正确。'
    unset -v root_pwd
  fi
done

m_user_check=$(mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "select count(*) from mysql.user where user='cloud'" | tail -n+2)

if [ $m_user_check -eq 0 ]; then

  mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "
  create database $database;
  create user 'cloud'@'%' identified by 'cloud';
  grant all privileges ON $database.* to  'cloud'@'%'; "

else

  mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "
  CREATE DATABASE IF NOT EXISTS $database;
  grant all privileges ON $database.* to  'cloud'@'%'; "

fi


$v_connect_mysql "CREATE TABLE IF NOT EXISTS resources_acl (
        resource_uuid       VARCHAR(64) NULL DEFAULT NULL,
        resource_type       VARCHAR(64) NULL DEFAULT NULL,
        admin_uuid          VARCHAR(64) NULL DEFAULT NULL,
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        project_uuid        VARCHAR(64) NULL DEFAULT NULL,
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (resource_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"
$v_connect_mysql "create index type_project_user_idx on resources_acl(resource_type, project_uuid, user_uuid)"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS users_register (
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        user_name           VARCHAR(64) NULL DEFAULT NULL,
        password            VARCHAR(64) NULL DEFAULT NULL,
        salt                VARCHAR(32) NULL DEFAULT NULL,
        email               VARCHAR(32) NULL DEFAULT NULL,
        mobile              VARCHAR(32) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (user_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS users (
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        user_name           VARCHAR(64) NULL DEFAULT NULL UNIQUE,
        real_name           VARCHAR(64) NULL DEFAULT NULL,
        password            VARCHAR(64) NULL DEFAULT NULL,
        salt                VARCHAR(32) NULL DEFAULT NULL,
        email               VARCHAR(32) NULL DEFAULT NULL UNIQUE,
        mobile              VARCHAR(32) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        sex                 VARCHAR(32) NULL DEFAULT NULL,
        birth_date          DATETIME NULL DEFAULT NULL,
        extra               VARCHAR(1024) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (user_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS roles (
        role_uuid           VARCHAR(64) NULL DEFAULT NULL,
        role_name           VARCHAR(64) NULL DEFAULT NULL,
        role_priv           VARCHAR(64) NULL DEFAULT NULL,
        role_type           VARCHAR(64) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (role_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS tokens (
        token               VARCHAR(64) NULL DEFAULT NULL,
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        project_uuid        VARCHAR(64) NULL DEFAULT NULL,
        expiry_time         DATETIME NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (token)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS teams (
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        team_name           VARCHAR(64) NULL DEFAULT NULL,
        team_owner          VARCHAR(64) NULL DEFAULT NULL,
        team_type           VARCHAR(64) NULL DEFAULT NULL,
        team_desc           VARCHAR(64) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        UNIQUE(team_name),
        PRIMARY KEY (team_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS projects (
        project_uuid        VARCHAR(64) NULL DEFAULT NULL,
        project_name        VARCHAR(64) NULL DEFAULT NULL,
        project_owner       VARCHAR(64) NULL DEFAULT NULL,
        project_team        VARCHAR(64) NULL DEFAULT NULL,
        project_type        VARCHAR(64) NULL DEFAULT NULL,
        project_desc        VARCHAR(64) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        UNIQUE(project_name, project_team),
        PRIMARY KEY (project_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS users_teams (
        id                  INT(11) NOT NULL AUTO_INCREMENT,
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        team_role           VARCHAR(64) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        UNIQUE(user_uuid, team_uuid),
        PRIMARY KEY (id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"
$v_connect_mysql "create index user_uuid_idx on users_teams(user_uuid)"
$v_connect_mysql "create index team_uuid_idx on users_teams(team_uuid)"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS users_projects (
        id                  INT(11) NOT NULL AUTO_INCREMENT,
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        project_uuid        VARCHAR(64) NULL DEFAULT NULL,
        project_role        VARCHAR(64) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        UNIQUE(user_uuid, project_uuid),
        PRIMARY KEY (id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"
$v_connect_mysql "create index user_uuid_idx on users_projects(user_uuid)"
$v_connect_mysql "create index project_uuid_idx on users_projects(project_uuid)"


acl_check=$($v_connect_mysql "select count(*) from resources_acl" | tail -n+2)
if [ $acl_check -eq 0 ]; then

    roles_list="owner admin user"
    for role in $roles_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$role"', 'role', 'global', 'global', 'global', '0', now(), now())"
    done

    admin_api_list="uct_usr_adm_com uct_usr_usr_stu"
    for admin_api in $admin_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$admin_api"', 'api', 'global', '0', '0', '0', now(), now())"
    done

    team_api_list="uct_usr_tem_com uct_rol_rol_crt uct_pro_pro_crt"
    for team_api in $team_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$team_api"', 'api', 'global', 'global', '0', '0', now(), now())"
    done

    project_api_list="uct_usr_pro_com uct_rol_rol_lst"
    for project_api in $project_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$project_api"', 'api', 'global', 'global', 'global', '0', now(), now())"
    done

    user_api_list="uct_usr_usr_com uct_usr_usr_lst uct_tem_tem_crt uct_tem_tem_lst uct_pro_pro_lst"
    for user_api in $user_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$user_api"', 'api', 'global', 'global', 'global', 'global', now(), now())"
    done

fi


role_check=$($v_connect_mysql "select count(*) from roles" | tail -n+2)
if [ $role_check -eq 0 ]; then

    $v_connect_mysql "insert into roles(role_uuid, role_name, role_priv, role_type, status, create_time, update_time)
                      values('owner', 'owner', 'CRUD', 'system', 'enable', now(), now())"

    $v_connect_mysql "insert into roles(role_uuid, role_name, role_priv, role_type, status, create_time, update_time)
                      values('admin', 'admin', 'CRU', 'system', 'enable', now(), now())"

    $v_connect_mysql "insert into roles(role_uuid, role_name, role_priv, role_type, status, create_time, update_time)
                      values('user', 'user', 'C', 'system', 'enable', now(), now())"

fi

user_check=$($v_connect_mysql "select count(*) from users where user_name='admin'" | tail -n+2)
if [ $user_check -eq 0 ]; then

    # team_uuid=$(uuidgen)
    # project_uuid=$(uuidgen)
    team_uuid='sysadmin-team-uuid'
    project_uuid='sysadmin-project-uuid'

    $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                      admin_uuid, team_uuid, project_uuid, user_uuid, \
                      create_time, update_time) \
                      values('sysadmin', 'user', 'sysadmin', '0', '0', '0', now(), now())"

    $v_connect_mysql "insert into users(user_uuid, user_name, real_name, \
                      password, salt, email, mobile, status, sex, birth_date, \
                      create_time, update_time) \
                      values('sysadmin', 'admin', 'sysadmin', 'f560f03b256012365358b319a04f443c', \
                      '7110be8012', 'admin@boxlinker.com', 'None', \
                      'enable', 'man', now(), now(), now())"

    $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                      admin_uuid, team_uuid, project_uuid, user_uuid, \
                      create_time, update_time) \
                      values('"$team_uuid"', 'team', '0', '0', '0', 'sysadmin', now(), now())"

    $v_connect_mysql "insert into teams(team_uuid, team_name, team_owner, team_type, \
                      team_desc, status, create_time, update_time) \
                      values('"$team_uuid"', 'admin', 'sysadmin', 'system', \
                      'user default team', 'enable', now(), now())"

    $v_connect_mysql "insert into users_teams(user_uuid, team_uuid, \
                      team_role, status, create_time, update_time) \
                      values('sysadmin', '"$team_uuid"', 'owner', 'enable', now(), now())"

    $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                      admin_uuid, team_uuid, project_uuid, user_uuid, \
                      create_time, update_time) \
                      values('"$project_uuid"', 'project', '0', '0', '0', 'sysadmin', now(), now())"

    $v_connect_mysql "insert into projects(project_uuid, project_name, \
                      project_owner, project_team, project_type, project_desc, status, \
                      create_time, update_time) \
                      values('"$project_uuid"', 'admin', 'sysadmin', '"$team_uuid"', \
                      'system', 'team default project', 'enable', now(), now())"

    $v_connect_mysql "insert into users_projects(user_uuid, project_uuid, \
                      project_role, status, create_time, update_time) \
                      values('sysadmin', '"$project_uuid"', 'owner', 'enable', now(), now())"

fi

user_check=$($v_connect_mysql "select count(*) from users where user_name='service'" | tail -n+2)
if [ $user_check -eq 0 ]; then

    user_name='service'
    user_uuid=$(uuidgen)
    team_uuid=$(uuidgen)
    project_uuid=$(uuidgen)

    $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                      admin_uuid, team_uuid, project_uuid, user_uuid, \
                      create_time, update_time) \
                      values('"$user_uuid"', 'user', '0', '0', '0', '"$user_uuid"', now(), now())"

    $v_connect_mysql "insert into users(user_uuid, user_name, real_name, \
                      password, salt, email, mobile, status, sex, birth_date, \
                      create_time, update_time) \
                      values('"$user_uuid"', '"$user_name"', '"$user_name"', '59230c9135fc7211fe30eedf8953f0bf', \
                      'e08222a8b6', 'service@boxlinker.com', 'None', \
                      'enable', 'man', now(), now(), now())"

    $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                      admin_uuid, team_uuid, project_uuid, user_uuid, \
                      create_time, update_time) \
                      values('"$team_uuid"', 'team', '0', '0', '0', '"$user_uuid"', now(), now())"

    $v_connect_mysql "insert into teams(team_uuid, team_name, team_owner, team_type, \
                      team_desc, status, create_time, update_time) \
                      values('"$team_uuid"', '"$user_name"', '"$user_uuid"', 'system', \
                      'user default team', 'enable', now(), now())"

    $v_connect_mysql "insert into users_teams(user_uuid, team_uuid, \
                      team_role, status, create_time, update_time) \
                      values('"$user_uuid"', '"$team_uuid"', 'owner', 'enable', now(), now())"

    $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                      admin_uuid, team_uuid, project_uuid, user_uuid, \
                      create_time, update_time) \
                      values('"$project_uuid"', 'project', '0', '0', '0', '"$user_uuid"', now(), now())"

    $v_connect_mysql "insert into projects(project_uuid, project_name, \
                      project_owner, project_team, project_type, project_desc, status, \
                      create_time, update_time) \
                      values('"$project_uuid"', '"$user_name"', '"$user_uuid"', '"$team_uuid"', \
                      'system', 'team default project', 'enable', now(), now())"

    $v_connect_mysql "insert into users_projects(user_uuid, project_uuid, \
                      project_role, status, create_time, update_time) \
                      values('"$user_uuid"', '"$project_uuid"', 'owner', 'enable', now(), now())"

fi

echo "$database数据库初始化完成"
