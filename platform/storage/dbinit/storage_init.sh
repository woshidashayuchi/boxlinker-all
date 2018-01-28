#!/bin/bash

db_server='127.0.0.1'
db_port=3306
database='storage'

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
$v_connect_mysql "create index type_project_idx on resources_acl(resource_type, project_uuid)"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS ceph_hosts (
        host_uuid           VARCHAR(64) NULL DEFAULT NULL,
        host_name           VARCHAR(64) NULL DEFAULT NULL,
        host_ip             VARCHAR(64) NULL DEFAULT NULL,
        host_cpu            INT(8) NULL DEFAULT NULL,
        host_mem            DOUBLE(12, 2) NULL DEFAULT NULL,
        host_disk           TEXT NULL DEFAULT NULL,
        host_nic            TEXT NULL DEFAULT NULL,
        host_status         VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (host_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS host_nics (
        nic_uuid            VARCHAR(64) NULL DEFAULT NULL,
        nic_name            VARCHAR(64) NULL DEFAULT NULL,
        nic_host            VARCHAR(64) NULL DEFAULT NULL,
        nic_mac             VARCHAR(64) NULL DEFAULT NULL,
        nic_role            VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (nic_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS host_disks (
        disk_uuid           VARCHAR(64) NULL DEFAULT NULL,
        disk_name           VARCHAR(64) NULL DEFAULT NULL,
        disk_host           VARCHAR(64) NULL DEFAULT NULL,
        disk_size           VARCHAR(64) NULL DEFAULT NULL,
        disk_used           DOUBLE(8,2) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (disk_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS ceph_clusters (
        cluster_uuid        VARCHAR(64) NULL DEFAULT NULL,
        cluster_name        VARCHAR(64) NULL DEFAULT NULL UNIQUE,
        cluster_auth        VARCHAR(32) NULL DEFAULT NULL,
        service_auth        VARCHAR(32) NULL DEFAULT NULL,
        client_auth         VARCHAR(32) NULL DEFAULT NULL,
        ceph_pgnum          INT(8) NULL DEFAULT NULL,
        ceph_pgpnum         INT(8) NULL DEFAULT NULL,
        public_network      VARCHAR(64) NULL DEFAULT NULL,
        cluster_network     VARCHAR(64) NULL DEFAULT NULL,
        osd_full_ratio      VARCHAR(64) NULL DEFAULT NULL,
        osd_nearfull_ratio  VARCHAR(64) NULL DEFAULT NULL,
        journal_size        INT(8) NULL DEFAULT NULL,
        ntp_server          VARCHAR(64) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (cluster_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS ceph_mons (
        mon_uuid            VARCHAR(64) NULL DEFAULT NULL,
        cluster_uuid        VARCHAR(64) NULL DEFAULT NULL,
        mon_id              VARCHAR(32) NULL DEFAULT NULL,
        host_uuid           VARCHAR(64) NULL DEFAULT NULL,
        storage_ip          VARCHAR(64) NULL DEFAULT NULL,
        status              VARCHAR(8) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (mon_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS ceph_osds (
        osd_uuid            VARCHAR(64) NULL DEFAULT NULL,
        cluster_uuid        VARCHAR(64) NULL DEFAULT NULL,
        osd_id              VARCHAR(32) NULL DEFAULT NULL,
        host_uuid           VARCHAR(64) NULL DEFAULT NULL,
        storage_ip          VARCHAR(64) NULL DEFAULT NULL,
        jour_disk           VARCHAR(32) NULL DEFAULT NULL,
        data_disk           VARCHAR(32) NULL DEFAULT NULL,
        disk_type           VARCHAR(32) NULL DEFAULT NULL,
        weight              VARCHAR(32) NULL DEFAULT NULL,
        status              VARCHAR(8) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (osd_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS ceph_pools (
        pool_uuid           VARCHAR(64) NULL DEFAULT NULL,
        cluster_uuid        VARCHAR(64) NULL DEFAULT NULL,
        pool_name           VARCHAR(64) NULL DEFAULT NULL,
        pool_size           VARCHAR(32) NULL DEFAULT NULL,
        used                VARCHAR(32) NULL DEFAULT NULL,
        avail               VARCHAR(32) NULL DEFAULT NULL,
        used_rate           DOUBLE(8,2) NULL DEFAULT NULL,
        pool_type           VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (pool_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


$v_connect_mysql "CREATE TABLE IF NOT EXISTS volumes (
        volume_uuid         VARCHAR(64) NULL DEFAULT NULL,
        cluster_uuid        VARCHAR(64) NULL DEFAULT NULL,
        pool_name           VARCHAR(32) NULL DEFAULT NULL,
        volume_name         VARCHAR(64) NULL DEFAULT NULL,
        volume_size         INT(8) NULL DEFAULT NULL,
        volume_type         VARCHAR(32) NULL DEFAULT NULL,
        volume_status       VARCHAR(32) NULL DEFAULT NULL,
        disk_name           VARCHAR(128) NULL DEFAULT NULL,
        fs_type             VARCHAR(32) NULL DEFAULT NULL,
        mount_point         VARCHAR(32) NULL DEFAULT NULL,
        create_time         DATETIME NULL DEFAULT NULL,
        update_time         DATETIME NULL DEFAULT NULL,
        PRIMARY KEY (volume_uuid)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB"


acl_check=$($v_connect_mysql "select count(*) from resources_acl" | tail -n+2)
if [ $acl_check -eq 0 ]; then

    admin_api_list="stg_stg_adm_com"
    for admin_api in $admin_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$admin_api"', 'api', 'global', '0', '0', '0', now(), now())"
    done

    team_api_list="stg_stg_tem_com"
    for team_api in $team_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$team_api"', 'api', 'global', 'global', '0', '0', now(), now())"
    done

    project_api_list="stg_stg_pro_com stg_ceh_dsk_add"
    for project_api in $project_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$project_api"', 'api', 'global', 'global', 'global', '0', now(), now())"
    done

    user_api_list="stg_stg_usr_com stg_ceh_dsk_lst"
    for user_api in $user_api_list
    do
        $v_connect_mysql "insert into resources_acl(resource_uuid, resource_type, admin_uuid, team_uuid, project_uuid, user_uuid, create_time, update_time)
                          values('"$user_api"', 'api', 'global', 'global', 'global', 'global', now(), now())"
    done

fi

echo "$database数据库初始化完成"
