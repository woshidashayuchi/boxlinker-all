#!/bin/bash

db_server='127.0.0.1'
db_port=3306
database='billing'

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
  CREATE DATABASE IF NOT EXISTS $database;
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
$v_connect_mysql "create index type_team_idx on resources_acl(resource_type, team_uuid)"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS levels (
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        level               INT(8) NULL DEFAULT NULL,
        experience          INT(16) NULL DEFAULT NULL,
        up_required         INT(16) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (team_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS balances (
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        total               INT(16) NULL DEFAULT NULL,
        balance             DOUBLE(16,6) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (team_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS recharge_records (
        recharge_uuid       VARCHAR(64) NULL DEFAULT NULL,
        recharge_amount     INT(8) NULL DEFAULT NULL,
        recharge_type       VARCHAR(32) NULL DEFAULT NULL,
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        user_name           VARCHAR(64) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (recharge_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS limits (
        team_level          INT(8) NULL DEFAULT NULL,
        teams               INT(8) NULL DEFAULT NULL,
        teamusers           INT(8) NULL DEFAULT NULL,
        projects            INT(8) NULL DEFAULT NULL,
        projectusers        INT(8) NULL DEFAULT NULL,
        roles               INT(8) NULL DEFAULT NULL,
        images              INT(8) NULL DEFAULT NULL,
        services            INT(8) NULL DEFAULT NULL,
        volumes             INT(8) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (team_level)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS resources (
        resource_uuid       VARCHAR(64) NULL DEFAULT NULL,
        resource_name       VARCHAR(64) NULL DEFAULT NULL,
        resource_conf       VARCHAR(64) NULL DEFAULT NULL,
        resource_status     VARCHAR(64) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (resource_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS orders (
        orders_uuid         VARCHAR(64) NULL DEFAULT NULL,
        resource_uuid       VARCHAR(64) NULL DEFAULT NULL,
        cost                DOUBLE(10,2) NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (orders_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS resources_paid (
        resource_uuid       VARCHAR(64) NULL DEFAULT NULL,
        paid_mode           VARCHAR(32) NULL DEFAULT NULL,
        paid_time           DATETIME NULL DEFAULT NULL,
        end_time            DATETIME NULL DEFAULT NULL,
        remain_time         INT(12) NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (resource_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS vouchers (
        vouchers_uuid       VARCHAR(64) NULL DEFAULT NULL,
        createuser_uuid     VARCHAR(64) NULL DEFAULT NULL,
        denomination        DOUBLE(5,2) NULL DEFAULT NULL,
        balance             DOUBLE(9,6) NULL DEFAULT NULL,
        active_time         DATETIME NULL DEFAULT NULL,
        invalid_time        DATETIME NULL DEFAULT NULL,
        status              VARCHAR(32) NULL DEFAULT NULL,
        accepter            VARCHAR(64) NULL DEFAULT NULL,
        activator           VARCHAR(64) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (vouchers_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS bills (
        id                  INT(11) NOT NULL AUTO_INCREMENT,
        resource_uuid       VARCHAR(64) NULL DEFAULT NULL,
        resource_cost       DOUBLE(12,6) NULL DEFAULT NULL,
        voucher_cost        DOUBLE(12,6) NULL DEFAULT NULL,
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        project_uuid        VARCHAR(64) NULL DEFAULT NULL,
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        insert_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"
$v_connect_mysql "create index resource_uuid_idx on bills(resource_uuid)"
$v_connect_mysql "create index team_idx on bills(team_uuid)"
$v_connect_mysql "create index insert_time_idx on bills(insert_time)"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS bills_days (
        id                  INT(11) NOT NULL AUTO_INCREMENT,
        resource_uuid       VARCHAR(64) NULL DEFAULT NULL,
        resource_cost       DOUBLE(12,6) NULL DEFAULT NULL,
        voucher_cost        DOUBLE(12,6) NULL DEFAULT NULL,
        team_uuid           VARCHAR(64) NULL DEFAULT NULL,
        project_uuid        VARCHAR(64) NULL DEFAULT NULL,
        user_uuid           VARCHAR(64) NULL DEFAULT NULL,
        insert_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"
$v_connect_mysql "create index resource_uuid_idx on bills_days(resource_uuid)"
$v_connect_mysql "create index team_idx on bills_days(team_uuid)"
$v_connect_mysql "create index insert_time_idx on bills_days(insert_time)"


acl_check=$($v_connect_mysql "select count(*) from resources_acl" | tail -n+2)
if [ $acl_check -eq 0 ]; then

    admin_api_list="bil_bil_adm_com bil_lmt_lmt_lst bil_lmt_lmt_udt bil_voc_voc_crt"
    for admin_api in $admin_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                          admin_uuid, team_uuid, project_uuid, user_uuid, \
                          create_time, update_time)
                          values('"$admin_api"', 'api', 'global', '0', '0', '0', now(), now())"
    done

    team_api_list="bil_bil_tem_com bil_rcg_rcg_lst"
    for team_api in $team_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                          admin_uuid, team_uuid, project_uuid, user_uuid, \
                          create_time, update_time)
                          values('"$team_api"', 'api', 'global', 'global', '0', '0', now(), now())"
    done

    project_api_list=""
    for project_api in $project_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                          admin_uuid, team_uuid, project_uuid, user_uuid, \
                          create_time, update_time)
                          values('"$project_api"', 'api', 'global', 'global', 'global', '0', now(), now())"
    done

    user_api_list="bil_lvl_lvl_ini bil_lvl_lvl_inf bil_blc_blc_add bil_blc_blc_inf
                   bil_rss_rss_crt bil_rss_rss_lst bil_odr_odr_crt bil_odr_odr_lst
                   bil_voc_voc_act bil_voc_voc_lst bil_bls_bls_lst bil_cst_cst_inf
                   bil_lmt_lmt_chk bil_bil_usr_com"
    for user_api in $user_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, \
                          admin_uuid, team_uuid, project_uuid, user_uuid, \
                          create_time, update_time)
                          values('"$user_api"', 'api', 'global', 'global', 'global', 'global', now(), now())"
    done

fi


limit_check=$($v_connect_mysql "select count(*) from limits" | tail -n+2)
if [ $acl_check -eq 0 ]; then

    $v_connect_mysql "insert into limits(team_level, teams, teamusers, \
                      projects, projectusers, roles, images, services, volumes, \
                      create_time, update_time)
                      values(1, 1, 5, 3, 5, 2, 5, 5, 5, now(), now())"

    $v_connect_mysql "insert into limits(team_level, teams, teamusers, \
                      projects, projectusers, roles, images, services, volumes, \
                      create_time, update_time)
                      values(2, 2, 10, 3, 10, 2, 30, 30, 30, now(), now())"

    $v_connect_mysql "insert into limits(team_level, teams, teamusers, \
                      projects, projectusers, roles, images, services, volumes, \
                      create_time, update_time)
                      values(3, 4, 60, 4, 60, 4, 300, 300, 300, now(), now())"

    $v_connect_mysql "insert into limits(team_level, teams, teamusers, \
                      projects, projectusers, roles, images, services, volumes, \
                      create_time, update_time)
                      values(4, 6, 160, 5, 160, 6, 1120, 1120, 1120, now(), now())"

    $v_connect_mysql "insert into limits(team_level, teams, teamusers, \
                      projects, projectusers, roles, images, services, volumes, \
                      create_time, update_time)
                      values(5, 10, 400, 6, 400, 8, 3600, 3600, 3600, now(), now())"

fi


level_check=$($v_connect_mysql "select count(*) from levels" | tail -n+2)
if [ $level_check -eq 0 ]; then

    $v_connect_mysql "insert into levels(team_uuid, level, experience, \
                      up_required, create_time, update_time)
                      values('sysadmin-team-uuid', 5, 10000, 0, now(), now())"

fi


balance_check=$($v_connect_mysql "select count(*) from balances" | tail -n+2)
if [ $balance_check -eq 0 ]; then

    $v_connect_mysql "insert into balances(team_uuid, total, balance, \
                      create_time, update_time)
                      values('sysadmin-team-uuid', 100, 100, now(), now())"

fi


echo "$database数据库初始化完成"
