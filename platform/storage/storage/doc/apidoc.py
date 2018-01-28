#! /usr/bin python
# -*- coding:utf8 -*-
# Date:2016-08-31
# Author: YanHua


"""
@apiDefine CODE_DELETE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {}
}
"""


"""
@apiDefine CODE_CLUSTER_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_uuid": "string",
        "cluster_name": "string",
        "cluster_auth": "string",
        "service_auth": "string",
        "client_auth": "string",
        "ceph_pgnum": int,
        "ceph_pgpnum": int,
        "public_network": "string",
        "cluster_network": "string",
        "osd_full_ratio": float,
        "osd_nearfull_ratio": float,
        "journal_size": int,
        "ntp_server": "string"
    }
}
"""


"""
@apiDefine CODE_CLUSTER_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_uuid": "string",
        "cluster_name": "string",
        "cluster_auth": "string",
        "service_auth": "string",
        "client_auth": "string",
        "ceph_pgnum": int,
        "ceph_pgpnum": int,
        "public_network": "string",
        "cluster_network": "string",
        "osd_full_ratio": float,
        "osd_nearfull_ratio": float,
        "journal_size": int,
        "ntp_server": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_CLUSTER_PUT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_uuid": "string",
        "host_ip": "string",
        "host_type": "kvm/k8s"
    }
}
"""


"""
@apiDefine CODE_CLUSTER_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_list": [
            {
                "cluster_uuid": "string",
                "cluster_name": "string",
                "cluster_auth": "string",
                "service_auth": "string",
                "client_auth": "string",
                "ceph_pgnum": int,
                "ceph_pgpnum": int,
                "public_network": "string",
                "cluster_network": "string",
                "osd_full_ratio": float,
                "osd_nearfull_ratio": float,
                "journal_size": int,
                "ntp_server": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "cluster_uuid": "string",
                "cluster_name": "string",
                "cluster_auth": "string",
                "service_auth": "string",
                "client_auth": "string",
                "ceph_pgnum": int,
                "ceph_pgpnum": int,
                "public_network": "string",
                "cluster_network": "string",
                "osd_full_ratio": float,
                "osd_nearfull_ratio": float,
                "journal_size": int,
                "ntp_server": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "cluster_uuid": "string",
                "cluster_name": "string",
                "cluster_auth": "string",
                "service_auth": "string",
                "client_auth": "string",
                "ceph_pgnum": int,
                "ceph_pgpnum": int,
                "public_network": "string",
                "cluster_network": "string",
                "osd_full_ratio": float,
                "osd_nearfull_ratio": float,
                "journal_size": int,
                "ntp_server": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_HOST_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "host_uuid": "string",
        "host_name": "string",
        "host_ip": "string",
        "host_cpu": int,
        "host_mem": float,
        "host_disk": list,
        "host_nic": list
    }
}
"""


"""
@apiDefine CODE_HOST_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "host_uuid": "string",
        "host_name": "string",
        "host_ip": "string",
        "host_cpu": int,
        "host_mem": float,
        "host_disk": list,
        "host_nic": list,
        "host_status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_HOST_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "host_list": [
            {
                "host_uuid": "string",
                "host_name": "string",
                "host_ip": "string",
                "host_cpu": int,
                "host_mem": float,
                "host_disk": list,
                "host_nic": list,
                "host_status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "host_uuid": "string",
                "host_name": "string",
                "host_ip": "string",
                "host_cpu": int,
                "host_mem": float,
                "host_disk": list,
                "host_nic": list,
                "host_status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "host_uuid": "string",
                "host_name": "string",
                "host_ip": "string",
                "host_cpu": int,
                "host_mem": float,
                "host_disk": list,
                "host_nic": list,
                "host_status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
        ]
    }
}
"""


"""
@apiDefine CODE_MON_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "mon01_hostip": "string",
        "mon02_hostip": "string",
        "mon01_hostname": "string",
        "mon02_hostname": "string",
        "cluster_uuid": "string",
        "mon01_id": "string",
        "mon02_id": "string",
        "mon01_storage_ip": "string",
        "mon02_storage_ip": "string"
    }
}
"""


"""
@apiDefine CODE_MON_PUT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_uuid": "string",
        "host_uuid": "string",
        "host_name": "string",
        "host_ip": "string",
        "mon_id": "string",
        "storage_ip": "string"
    }
}
"""


"""
@apiDefine CODE_MON_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "mon_uuid": "string",
        "cluster_uuid": "string",
        "cluster_name": "string",
        "mon_id": "string",
        "host_uuid": "string",
        "host_name": "string",
        "storage_ip": "string",
        "status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_MON_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "mon_list": [
            {
                "mon_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "mon_id": "string",
                "host_uuid": "string",
                "host_name": "string",
                "storage_ip": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "mon_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "mon_id": "string",
                "host_uuid": "string",
                "host_name": "string",
                "storage_ip": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "mon_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "mon_id": "string",
                "host_uuid": "string",
                "host_name": "string",
                "storage_ip": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_OSD_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "osd_uuid": "string",
        "cluster_uuid": "string",
        "osd_id": int,
        "host_uuid": "string",
        "host_name": "string",
        "host_ip": "string",
        "storage_ip": "string",
        "jour_disk": "string",
        "data_disk": "string",
        "disk_type": "hdd/ssd",
        "weight": float
    }
}
"""


"""
@apiDefine CODE_OSD_PUT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_uuid": "string",
        "osd_uuid": "string",
        "osd_id": int,
        "weight": float
    }
}
"""


"""
@apiDefine CODE_OSD_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "osd_uuid": "string",
        "cluster_uuid": "string",
        "cluster_name": "string",
        "osd_id": int,
        "host_uuid": "string",
        "host_name": "string",
        "host_ip": "string",
        "storage_ip": "string",
        "jour_disk": "string",
        "data_disk": "string",
        "disk_type": "string",
        "weight": float,
        "status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_OSD_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "osd_list": [
            {
                "osd_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "osd_id": int,
                "host_uuid": "string",
                "host_name": "string",
                "host_ip": "string",
                "storage_ip": "string",
                "jour_disk": "string",
                "data_disk": "string",
                "disk_type": "string",
                "weight": float,
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "osd_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "osd_id": int,
                "host_uuid": "string",
                "host_name": "string",
                "host_ip": "string",
                "storage_ip": "string",
                "jour_disk": "string",
                "data_disk": "string",
                "disk_type": "string",
                "weight": float,
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "osd_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "osd_id": int,
                "host_uuid": "string",
                "host_name": "string",
                "host_ip": "string",
                "storage_ip": "string",
                "jour_disk": "string",
                "data_disk": "string",
                "disk_type": "string",
                "weight": float,
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_POOL_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "cluster_uuid": "string",
        "pool_type": "string",
        "pool_name": "string"
    }
}
"""


"""
@apiDefine CODE_POOL_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "pool_uuid": "string",
        "cluster_uuid": "string",
        "cluster_name": "string",
        "pool_name": "string",
        "pool_size": int,
        "used": int,
        "avail": int,
        "used_rate": float,
        "pool_type": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_POOL_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "pool_list": [
            {
                "pool_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "pool_name": "string",
                "pool_size": int,
                "used": int,
                "avail": int,
                "used_rate": float,
                "pool_type": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "pool_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "pool_name": "string",
                "pool_size": int,
                "used": int,
                "avail": int,
                "used_rate": float,
                "pool_type": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "pool_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "pool_name": "string",
                "pool_size": int,
                "used": int,
                "avail": int,
                "used_rate": float,
                "pool_type": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


"""
@apiDefine CODE_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "cluster_uuid": "string",
        "volume_name": "string",
        "pool_name": "string",
        "image_name": "string",
        "volume_size": int,
        "volume_type": "string",
        "fs_type": "string"
    }
}
"""


"""
@apiDefine CODE_PUT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "volume_name": "string",
        "pool_name": "string",
        "image_name": "string",
        "volume_size": int
    }
}
"""


"""
@apiDefine CODE_PUT_STATUS0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "volume_status": "string"
    }
}
"""


"""
@apiDefine CODE_PUT_RECLAIM0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_GET_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "volume_uuid": "string",
        "cluster_uuid": "string",
        "pool_name": "string",
        "volume_name": "string",
        "volume_size": int,
        "volume_type": "string",
        "volume_status": "string",
        "image_name": "string",
        "fs_type": "string",
        "mount_point": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_GET_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "volume_list": [
            {
                "volume_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "pool_name": "string",
                "volume_name": "string",
                "volume_size": int,
                "volume_type": "string",
                "volume_status": "string",
                "image_name": "string",
                "fs_type": "string",
                "mount_point": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "volume_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "pool_name": "string",
                "volume_name": "string",
                "volume_size": int,
                "volume_type": "string",
                "volume_status": "string",
                "image_name": "string",
                "fs_type": "string",
                "mount_point": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                "volume_uuid": "string",
                "cluster_uuid": "string",
                "cluster_name": "string",
                "pool_name": "string",
                "volume_name": "string",
                "volume_size": int,
                "volume_type": "string",
                "volume_status": "string",
                "image_name": "string",
                "fs_type": "string",
                "mount_point": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
        ]
    }
}
"""


###################################################################
#                       存储服务接口定义                          #
###################################################################


"""
@api {post} /api/v1.0/admin/storage/cephclusters 1.1 存储集群创建
@apiName cluster create
@apiGroup 1 cluster
@apiVersion 1.0.0
@apiDescription 存储集群创建
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_name": "string",
    "journal_size": int,
    "ntp_server": "ip",
    "cluster_uuid": "string",
    "cluster_auth": "string",
    "service_auth": "string",
    "client_auth": "string",
    "ceph_pgnum": int,
    "ceph_pgpnum": int,
    "public_network": "string",
    "cluster_network": "string",
    "osd_full_ratio": float
    "osd_nearfull_ratio": float
}
@apiUse CODE_CLUSTER_POST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephclusters 1.2 存储集群列表
@apiName cluster list
@apiGroup 1 cluster
@apiVersion 1.0.0
@apiDescription 存储集群列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLUSTER_LIST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephclusters/<cluster_uuid> 1.3 存储集群信息
@apiName cluster info
@apiGroup 1 cluster
@apiVersion 1.0.0
@apiDescription 存储集群信息
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLUSTER_INFO_0
"""


"""
@api {put} /api/v1.0/admin/storage/cephclusters/<cluster_uuid> 1.4 存储集群挂载
@apiName cluster mount
@apiGroup 1 cluster
@apiVersion 1.0.0
@apiDescription 存储集群挂载
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "host_ip": "string",
    "password": "string",
    "host_type": "kvm/k8s"
}
@apiUse CODE_CLUSTER_PUT_0
"""


"""
@api {post} /api/v1.0/admin/storage/cephhosts 2.1 主机创建
@apiName cephhost create
@apiGroup 2 cephhost
@apiVersion 1.0.0
@apiDescription 将主机添加到平台
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "host_ip": "string",
    "password": "string"
}
@apiUse CODE_HOST_POST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephhosts?page_size=<int>&page_num=<int> 2.2 主机列表
@apiName cephhost list
@apiGroup 2 cephhost
@apiVersion 1.0.0
@apiDescription 查询主机列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_HOST_LIST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephhosts/<host_uuid> 2.3 主机信息
@apiName cephhost info
@apiGroup 2 cephhost
@apiVersion 1.0.0
@apiDescription 查询主机信息
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_HOST_INFO_0
"""


"""
@api {delete} /api/v1.0/admin/storage/cephhosts/<host_uuid> 2.4 主机删除
@apiName cephhost delete
@apiGroup 2 cephhost
@apiVersion 1.0.0
@apiDescription 将主机移出平台
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/admin/storage/cephmons 3.1 cephmon初始化
@apiName cephmon init
@apiGroup 3 cephmon
@apiVersion 1.0.0
@apiDescription cephmon初始化安装
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_uuid": "string",
    "mon01_hostuuid": "string",
    "mon01_hostip": "string",
    "mon01_rootpwd": "string",
    "mon01_snic": "string",
    "mon02_hostuuid": "string",
    "mon02_hostip": "string",
    "mon02_rootpwd": "string",
    "mon02_snic": "string"
}
@apiUse CODE_MON_POST_0
"""


"""
@api {put} /api/v1.0/admin/storage/cephmons 3.2 cephmon添加
@apiName cephmon add
@apiGroup 3 cephmon
@apiVersion 1.0.0
@apiDescription 添加cephmon节点到ceph集群
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_uuid": "string",
    "host_uuid": "string",
    "host_ip": "string",
    "rootpwd": "string",
    "storage_nic": "string"
}
@apiUse CODE_MON_PUT_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephmons?cluster_uuid=<string> 3.3 cephmon列表
@apiName cephmon list
@apiGroup 3 cephmon
@apiVersion 1.0.0
@apiDescription 查询cephmon节点列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_MON_LIST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephmons/<mon_uuid> 3.4 cephmon信息
@apiName cephmon info
@apiGroup 3 cephmon
@apiVersion 1.0.0
@apiDescription 查询cephmon节点信息
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_MON_INFO_0
"""


"""
@api {post} /api/v1.0/admin/storage/cephosds 4.1 cephosd添加
@apiName cephosd add
@apiGroup 4 cephosd
@apiVersion 1.0.0
@apiDescription cephosd添加
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_uuid": "string",
    "host_uuid": "string",
    "host_ip": "string",
    "rootpwd": "string",
    "storage_nic": "string",
    "jour_disk": "string",
    "data_disk": "string",
    "disk_type": "hdd/ssd",
    "weight": float
}
@apiUse CODE_OSD_POST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephosds?cluster_uuid=<string>&page_size=<int>&page_num=<int> 4.2 cephosd列表
@apiName cephosd list
@apiGroup 4 cephosd
@apiVersion 1.0.0
@apiDescription 查询cephosd列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_OSD_LIST_0
"""


"""
@api {put} /api/v1.0/admin/storage/cephosds/<osd_uuid> 4.3 cephosd权重
@apiName cephosd reweight
@apiGroup 4 cephosd
@apiVersion 1.0.0
@apiDescription cephosd存储权重调整
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_uuid": "string",
    "weight": float
}
@apiUse CODE_OSD_PUT_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephosds/<osd_uuid> 4.4 cephosd信息
@apiName cephosd info
@apiGroup 4 cephosd
@apiVersion 1.0.0
@apiDescription 查询cephosd信息
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_OSD_INFO_0
"""


"""
@api {delete} /api/v1.0/admin/storage/cephosds/<osd_uuid>?cluster_uuid=<string>&rootpwd=<string> 4.5 cephosd删除
@apiName cephosd delete
@apiGroup 4 cephosd
@apiVersion 1.0.0
@apiDescription cephosd删除
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {post} /api/v1.0/admin/storage/cephpools 5.1 cephpools创建
@apiName cephpool add
@apiGroup 5 cephpool
@apiVersion 1.0.0
@apiDescription cephosd添加
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_uuid": "string",
    "pool_type": "hdd/ssd"
}
@apiUse CODE_POOL_POST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephpools?cluster_uuid=<string> 5.2 cephpools列表
@apiName cephpool list
@apiGroup 5 cephpool
@apiVersion 1.0.0
@apiDescription cephosd列表
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_POOL_LIST_0
"""


"""
@api {get} /api/v1.0/admin/storage/cephpools/<pool_uuid> 5.3 cephpools信息
@apiName cephpool info
@apiGroup 5 cephpool
@apiVersion 1.0.0
@apiDescription cephosd信息
@apiPermission admin
@apiParam {json} header {"token": "string"}
@apiUse CODE_POOL_INFO_0
"""


"""
@api {post} /api/v1.0/storage/volumes 6.1 存储卷创建
@apiName volume create
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 存储卷创建
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "cluster_uuid": "string",
    "volume_name": "string",
    "volume_size": int,
    "volume_type": "hdd/ssd",
    "fs_type": "xfs/ext4",
    "cost": float
}
@apiUse CODE_POST_0
"""


"""
@api {get} /api/v1.0/storage/volumes?cluster_uuid=<string>&page_size=<int>&page_num=<int> 6.2 存储卷列表
@apiName volume list
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 存储卷列表查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_LIST_0
"""


"""
@api {get} /api/v1.0/storage/volumes/<volume_uuid> 6.3 存储卷信息
@apiName volume info
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 存储卷详细信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_0
"""


"""
@api {put} /api/v1.0/storage/volumes/<volume_uuid>?update=<size> 6.4 存储卷更新（容量）
@apiName update volume size
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 存储卷容量更新
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "volume_size": int
}
@apiUse CODE_PUT_0
"""


"""
@api {put} /api/v1.0/storage/volumes/<volume_uuid>?update=<status> 6.5 存储卷更新（状态）
@apiName update volume status
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 存储卷状态更新
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "volume_status": "using/unused"
}
@apiUse CODE_PUT_STATUS0
"""


"""
@api {delete} /api/v1.0/storage/volumes/<volume_uuid> 6.6 存储卷删除
@apiName volume delete
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 存储卷删除
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {get} /api/v1.0/storage/volumes/reclaims?page_size=<int>&page_num=<int> 6.7 回收站列表
@apiName reclaim volume list
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 回收站中存储卷列表查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_GET_LIST_0
"""


"""
@api {put} /api/v1.0/storage/volumes/reclaims/<volume_uuid> 6.8 回收站恢复
@apiName recovery volume from reclaim
@apiGroup 6 volumes
@apiVersion 1.0.0
@apiDescription 从回收站中恢复已删除的存储卷
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_PUT_RECLAIM0
"""
