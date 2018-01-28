# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/10
from common.logs import logging as log
from storage_api import StorageRpcApi
from common.parameters import context_data
from conf import conf


class VolumeDriver(object):

    def __init__(self):
        self.storage_api = StorageRpcApi()

    def put_using(self, dict_data):
        token = dict_data.get('token')
        volume_uuid = dict_data.get('volume_uuid')
        context = context_data(token, volume_uuid, 'update')
        parameters = {'volume_status': dict_data.get('volume_status'), 'update': 'status'}

        try:
            change_result = self.storage_api.disk_update(context, parameters)

            log.info('change the volume status result is:%s, type is %s' % (change_result, type(change_result)))

            if change_result.get('status') != 0:
                return False
        except Exception, e:
            log.error('change the volume status error, reason is: %s' % e)
            return False

        return change_result

    def storage_status(self, dict_data):
        response = ""
        volume = dict_data.get("volume")
        if volume is None or volume == '':
            return True

        if dict_data.get("action").upper() == "POST":
            for i in volume:
                volume_uuid = i.get("volume_uuid")
                json_status = {"volume_uuid": volume_uuid, "volume_status": "using"}
                dict_data.update(json_status)
                response = self.put_using(dict_data)

        if dict_data.get("action").upper() == "PUT":

            for i in volume:
                volume_uuid = i.get("volume_uuid")
                json_status = {"volume_uuid": volume_uuid, "volume_status": "unused"}
                dict_data.update(json_status)
                response = self.put_using(dict_data)
                log.info('delete the volumes data is fuck: %s' % dict_data)

        return response

    def volume_message(self, dict_data):
        token = dict_data.get('token')
        monitors = [x for x in conf.VOLUMEIP.split(',')]
        volume = dict_data.get('volume')

        ret = []
        ret_disk = []
        for i in volume:
            volume_uuid = i.get('volume_uuid')

            context = context_data(token, volume_uuid, "read")
            try:
                volume_result = self.storage_api.disk_info(context)
                log.info('get the volume message is:%s,type is %s' % (ret, type(ret)))

                if volume_result.get('status') != 0:
                    return False, False
            except Exception, e:
                log.error('get the volume message error, reason=%s' % e)
                return False, False

            volume_name = volume_result.get('result').get('volume_name')
            pool_name = volume_result.get('result').get('pool_name')
            image = volume_result.get('result').get('image_name')
            fs_type = volume_result.get('result').get('fs_type')
            readonly1 = i.get('readonly')
            if readonly1 == 'True':
                readonly = True
            else:
                readonly = False

            volumes = {
                        "name": volume_name,
                        "rbd": {
                            "monitors": monitors, "pool": pool_name, "image": image, "user": "admin",
                            "keyring": "/etc/ceph/keyring", "fsType": fs_type, "readOnly": readonly
                        }
                    }
            disk_msg = {'name': volume_name, 'readOnly': readonly, 'mountPath': i.get('disk_path')}

            ret_disk.append(disk_msg)
            ret.append(volumes)

        return ret, ret_disk

    def change_volume_status(self, dict_data):
        # change the database volume's status to unused
        # query the volume message first
        pass
