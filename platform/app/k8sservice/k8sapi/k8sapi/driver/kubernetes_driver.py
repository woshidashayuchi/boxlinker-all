# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 2017/02/10
import re
import json
import requests
import time
import copy
from conf import conf
from common.code import request_result
from common.logs import logging as log
from db.service_db import ServiceDB
from db.metal_work import MetalWork
from volume_driver import VolumeDriver
from image_driver import images_message_get
from rpcapi_client import KubernetesRpcClient
from token_driver import TokenDriver
from billing_driver import BillingResource


class KubernetesDriver(object):

    def __init__(self):
        self.service_db = ServiceDB()
        self.krpc_client = KubernetesRpcClient()
        self.metal = MetalWork()
        self.volume = VolumeDriver()
        self.token_driver = TokenDriver()
        self.billing = BillingResource()
        self.node = conf.node
        self.lb = conf.lb

    @staticmethod
    def command_query(dict_data):
        in_command = dict_data.get("command")

        if in_command != "" and in_command is not None:
            commands = in_command.split(" ")

            return commands

    @staticmethod
    def container(con):
        ret = []
        for i in con:
            container_port = i.get('container_port')
            protocol = i.get('protocol')
            # access_mode = i.get("access_mode")
            # access_scope = i.get("access_scope")
            result = {'containerPort': container_port, 'protocol': protocol.upper()}
            ret.append(result)
        return ret

    @staticmethod
    def env(en):
        result = []
        if en is not None:
            for i in en:
                env_name = i.get('env_key')
                env_value = i.get('env_value')
                result.append({'name': env_name, 'value': env_value})
        return result

    def service_domain(self, context):
        ser = context.get('container')
        service_name = context.get('service_name')
        team_name = context.get('team_name')
        project_name = context.get('project_name')
        using_port = None
        tcp_lb = ''
        http_lb = ''
        m = 1

        for i in ser:
            if project_name is not None and project_name != '' and project_name != team_name:
                domain_http = '%s-%s-%s.%s:' % (team_name, project_name, service_name, self.lb)
            else:
                domain_http = '%s-%s.%s:' % (team_name, service_name, self.lb)
            if i.get('access_mode').upper() in ['HTTP', 'HTTPS'] and i.get('access_scope') == 'outsisde':
                http_lbadd = domain_http + str(i.get('container_port'))
                if http_lb == '':
                    http_lb = http_lb + http_lbadd
                else:
                    http_lb = http_lb + ',' + http_lbadd
            if (i.get('access_mode').upper() == 'TCP' or i.get('access_mode').upper() == 'UDP') \
                    and i.get('access_scope') == 'outsisde':
                resu = self.service_db.max_used_port()
                log.info('get the max port is %s, yuan=%s' % (str(resu[0][0]), resu))

                if len(resu) != 0 and resu[0][0] is not None:
                    using_port = resu[0][0]
                if using_port is None:
                    ran_port = '30000'
                    tcp_lb = '%s:%s' % (ran_port, i.get('container_port'))
                else:
                    if context.get('container_update') == 'yes' or context.get('rtype') == 'container':
                        try:
                            ran_port = self.service_db.get_svc_port(context)[0][0]

                        except Exception, e:
                            log.error('get the tcp_port from database error, reason is: %s' % e)

                    else:
                        ran_port = int(using_port)+m
                    m += 1
                    if tcp_lb == '':
                        tcp_lb = '%s:%s' % (ran_port, i.get('container_port'))
                    else:
                        tcp_lb = tcp_lb+',' + '%s:%s' % (ran_port, i.get('container_port'))

                i['tcp_port'] = ran_port

        container = {'container': ser}

        return http_lb, tcp_lb, container

    def container_domain(self, dict_data):
        http_lb, tcp_lb, tcp_port = self.service_domain(dict_data)
        log.info('http_lb=%s,tcp_lb=%s,tcp_port=%s' % (http_lb, tcp_lb, tcp_port))

        container = tcp_port.get("container")
        newcon = []

        if http_lb != '':
            for i in re.split(',', http_lb):
                num = i.rfind(':')
                c_port = i[num+1:]
                http_domain = i[:num]

                for j in container:
                    if j.get('access_scope') == 'inside' and j.get('access_mode').upper() in ['HTTP', 'HTTPS']:
                        j['http_domain'] = None
                    if str(j.get('container_port')) == str(c_port) and j.get('access_mode').upper() in ['HTTP', 'HTTPS']:
                        j['http_domain'] = http_domain
                        newcon.append(j)

        if tcp_lb != '':
            for x in re.split(',', tcp_lb):
                num = x.rfind(':')
                c_port = x[num+1:]
                tcp_domain = self.lb + ':' + x[:num]
                # tcp_domain = "boxlinker.com" + ":" + x[:num]
                for y in container:
                    if (y.get('access_mode').upper() == 'TCP' or y.get('access_mode').upper() == 'UDP') \
                            and y.get('access_scope') == 'inside':
                        y['tcp_domain'] = None
                    if str(y.get('container_port')) == str(c_port) and (y.get('access_mode').upper() == 'TCP' or
                            y.get('access_mode').upper() == 'UDP'):
                        y['tcp_domain'] = tcp_domain
                        newcon.append(y)

        for i in container:
            if i.get('access_scope') == 'inside' or i.get('access_mode') == '':
                i['http_domain'] = ''
                i['tcp_domain'] = ''
                newcon.append(i)

        return newcon

    def service_port(self, ser):
        result = []
        x = 1
        y = 1
        udp = 'UDP'
        for i in ser:
            port = int(i.get("container_port"))
            targetport = int(i.get("container_port"))
            if i.get("access_mode").upper() == "HTTP" or i.get("access_mode").upper() == "HTTPS":
                name_c = "http"+str(x)
                x += 1
                result1 = {"name": name_c, "port": port, "targetPort": targetport}
                result.append(result1)
            if i.get("access_mode").upper() == "TCP":
                name_c = "tcp"+str(y)
                y += 1
                result1 = {"name": name_c, "port": port, "targetPort": targetport}
                result.append(result1)
            if i.get("access_mode").upper() == 'UDP':
                name_c = "udp"+str(y)
                y += 1
                result1 = {"name": name_c, "protocol": udp, "port": port, "targetPort": targetport}
                result.append(result1)

        return result

    @staticmethod
    def cm_spec(cm_format):
        if cm_format.lower() == '1x':
            container_cpu = '200m'
            container_memory = '256M'
        elif cm_format.lower() == '2x':
            container_cpu = '200m'
            container_memory = '256M'
        elif cm_format.lower() == '4x':
            container_cpu = '300m'
            container_memory = '512M'
        elif cm_format.lower() == '8x':
            container_cpu = '300m'
            container_memory = '512M'
        else:
            container_cpu = '200m'
            container_memory = '256M'

        return container_cpu, container_memory

    def unit_element(self, dict_data):
        try:
            namespace = dict_data.get('project_uuid')
            service_name = dict_data.get('service_name').lower().replace('_', '-')
            pods_num = int(dict_data.get('pods_num'))
            cm_format = dict_data.get('cm_format')
            container_cpu, container_memory = self.cm_spec(cm_format)
            team_name = dict_data.get('team_name')
            command = self.command_query(dict_data)
            policy1 = dict_data.get('policy')
            container = dict_data.get('container')
            env = dict_data.get('env')
            auto_startup = dict_data.get('auto_startup')
            user_uuid = dict_data.get('user_uuid')
        except Exception, e:
            log.error('parameters explain error, reason is: %s' % e)
            return False

        try:
            image_name, image_version = images_message_get(dict_data)
        except Exception, e:
            log.error('get the image message error, reason is: %s' % e)
            return False

        if int(auto_startup) != 1:
            pods_num = 0

        if int(policy1) == 1:
            rc_krud = image_name[20:].replace('/', '_').replace(':', '_')
            pullpolicy = 'Always'
        else:
            rc_krud = 'null'
            pullpolicy = 'IfNotPresent'

        try:
            if dict_data.get('volume') is not None and dict_data.get('volume') != '':
                volumes, volume_mounts = self.volume.volume_message(dict_data)
                if volumes is False:
                    return False
            else:
                volumes = None
                volume_mounts = None
        except Exception, e:
            log.error('volume define error, reason=%s' % e)
            return False

        return namespace, image_name, image_version, service_name, pods_num, cm_format, container_cpu, \
            container_memory, team_name, command, container, env, user_uuid, rc_krud, pullpolicy, volumes, \
            volume_mounts

    def get_kubenete_ingress(self, namespace, ingress_name):

        try:
            ingress_ret = self.krpc_client.get_ingress({'namespace': namespace, 'name': ingress_name})
            log.info('get the ingress result is: %s' % ingress_ret)
        except Exception, e:
            log.error('get the ingress of namespace(%s) error, reason is: %s' % (namespace, e))
            return False

        return ingress_ret

    @staticmethod
    def name_struct(dict_data):
        team_name = dict_data.get('team_name')
        project_name = dict_data.get('project_name')
        service_name = dict_data.get('service_name')
        if project_name is not None and project_name != '' and project_name != team_name:
            domain_http = '%s-%s-%s' % (team_name, project_name, service_name)
        else:
            domain_http = '%s-%s' % (team_name, service_name)

        return domain_http

    def ingress_port(self, dict_data):
        container_port = 0
        try:
            for i in dict_data.get('container'):
                if i.get('access_mode') in ['HTTP', 'HTTPS'] and i.get('access_scope') == 'outsisde':
                    container_port = i.get('container_port')
        except Exception, e:
            log.error('get the container_port error, reason is: %s' % e)
            return False

        if container_port == 0:
            return False

        return container_port

    def add_ingress_http(self, dict_data):
        namespace = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')

        for i in dict_data.get('container'):
            if i.get('access_mode') == 'HTTP' and i.get('access_scope') == 'outsisde':
                log.info('create the ingress, the data is: %s' % dict_data)
                domain_http = self.name_struct(dict_data)
                container_port = self.ingress_port(dict_data)

                if not container_port:
                    return False

                ingress_json = {
                    "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                    "metadata": {
                        "name": service_name, "namespace": namespace,
                        "annotations": {"kubernetes.io/ingress.class": "nginx",
                                        "loadbalancer/lb.name": "user"}
                    },
                    "spec": {"rules": [{"host": "%s.%s" % (domain_http, self.lb),
                                        "http": {"paths": [{"path": "/",
                                                            "backend": {"serviceName": service_name,
                                                                        "servicePort": container_port}
                                                            }]
                                                 }
                                        }]
                             }
                }
                return ingress_json

            if i.get('access_mode') == 'HTTPS' and i.get('access_scope') == 'outsisde':
                domain_http = self.name_struct(dict_data)
                container_port = self.ingress_port(dict_data)
                ingress_json = {
                    "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                    "metadata": {
                        "name": service_name, "namespace": namespace,
                        "annotations": {"kubernetes.io/ingress.class": "nginx",
                                        "nginx.org/ssl-services": service_name,
                                        "loadbalancer/lb.name": "user"}
                    },
                    "spec": {"rules": [{"host": "%s.%s" % (domain_http, self.lb),
                                        "http": {"paths": [{"path": "/",
                                                            "backend": {"serviceName": service_name,
                                                                        "servicePort": 443}
                                                            }]
                                                 }
                                        }],
                             "tls": [{'secretName': 'certify-https'}],
                             "backend": {"serviceName": service_name,
                                         "servicePort": container_port}
                             }
                }

                return ingress_json

        return

    def configmap_port(self, dict_data):

        if dict_data.get('rtype') == 'lifecycle':
            try:
                tcp_port = self.service_db.get_using_port(dict_data)
                log.info('tcp aaa>>>>>>>>>>>>> %s' % tcp_port)
            except Exception, e:
                log.error('get if the service has using port error, reason is: %s' % e)
                return False

            if len(tcp_port) == 0 or len(tcp_port[0]) == 0:
                pass
            else:
                return int(tcp_port[0][0])

        try:
            max_use = self.service_db.max_used_port()[0][0]
            log.info('the max used tcp port is: %s' % max_use)
        except Exception, e:
            log.error('get the max used tcp port error, reason is: %s' % e)
            return False

        if max_use == 0 or max_use is None:
            return 30006
        else:
            return int(max_use) + 1

    def add_config_map(self, dict_data):
        namespace = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')
        for i in dict_data.get('container'):
            if i.get('access_mode') == 'TCP' and i.get('access_scope') == 'outsisde':
                log.info('create the configmap, the data is: %s' % dict_data)
                container_port = self.configmap_port(dict_data)

                conf_map_json = {"apiVersion": "v1",
                                 "kind": "ConfigMap",
                                 "metadata": {"name": service_name, "namespace": namespace,
                                              "annotations": {"loadbalancer/lb.name": "user",
                                                              "loadbalancer/lb.date": str(time.time())}},
                                 "data": {"host": "lb1.boxlinker.com", "hostport": str(container_port),
                                          "servicename": service_name}
                                 }

                return conf_map_json

            if i.get('access_mode') == 'UDP' and i.get('access_scope') == 'outsisde':
                container_port = self.configmap_port(dict_data)
                udp = 'true'
                conf_map_json = {"apiVersion": "v1",
                                 "kind": "ConfigMap",
                                 "metadata": {"name": service_name, "namespace": namespace,
                                              "annotations": {"loadbalancer/lb.name": "user",
                                                              "loadbalancer/lb.date": str(time.time())}},
                                 "data": {"host": "lb1.boxlinker.com", "hostport": str(container_port),
                                          "servicename": service_name, "udp": udp}
                                 }

                return conf_map_json

        return

    def add_rc(self, dict_data):
        log.info('add rc json data is: %s' % dict_data)
        try:
            namespace, image_name, image_version, service_name, pods_num, cm_format, container_cpu, \
                container_memory, team_name, command, container, env, user_uuid, rc_krud, pullpolicy, \
                volumes, volume_mounts = self.unit_element(dict_data)
        except Exception, e:
            log.error('get the explain parameters error, reason is: %s' % e)
            return False

        try:
            add_rc = {
               "rtype": "replicationcontrollers",
               "kind": "ReplicationController", "apiVersion": "v1",
               "metadata": {
                  "namespace": namespace, "name": service_name,
                  "labels": {"component": service_name, "rc-krud": rc_krud, "name": service_name}
               },
               "spec": {
                  "replicas": pods_num,
                  "selector": {"name": service_name},
                  "template": {
                     "metadata": {
                        "labels": {"component": dict_data.get("service_name"), "name": service_name,
                                   "logs": service_name+namespace}
                     },
                     "spec": {
                        "nodeSelector": {"role": "user"},
                        "containers": [
                           {"name": service_name, "image": image_name+":"+image_version, "imagePullPolicy": pullpolicy,
                            "command": command, "ports": self.container(container), "env": self.env(env),
                            # "resources": {"limits": {"cpu": container_cpu, "memory": container_memory}},
                            "volumeMounts": volume_mounts}
                        ], "volumes": volumes,
                     }
                  }
               },
            }

            if dict_data.get('env') == [{'env_key': '', 'env_value': ''}] or dict_data.get('env') == '':
                j = 0
                for i in add_rc['spec']['template']['spec']['containers']:
                    del add_rc['spec']['template']['spec']['containers'][j]['env']
                    j += 1

            if volumes is None:
                j = 0
                del add_rc['spec']['template']['spec']['volumes']
                for i in add_rc['spec']['template']['spec']['containers']:
                    del add_rc['spec']['template']['spec']['containers'][j]['volumeMounts']
                    j += 1

            if volumes is False:
                return False

            if command == '' or command is None or command == 'Null':
                j = 0
                for i in add_rc['spec']['template']['spec']['containers']:
                    del add_rc['spec']['template']['spec']['containers'][j]['command']
                    j += 1

        except Exception, e:
            log.error('rc json create error,reason=%s' % e)
            return False

        return add_rc

    def del_pod_element(self, dict_data):
        try:
            command = ''
            pullpolicy = ''
            rc_krud = ''
            image_name = "index.boxlinker.com/boxlinker/web-index"
            image_version = "latest"
            service_name = dict_data.get('service_name').lower().replace('_', '-')
            namespace = dict_data.get('project_uuid')
            pods_num = 0
            container = []
            images = image_name + image_version
        except Exception, e:
            log.error('parameters explain error, reason is:' % e)
            return

        try:
            rc_ret, containers_ret, env_ret, volume_ret = self.service_db.service_detail
        except Exception, e:
            log.error('get the all detail messages error, reason=%s' % e)
            raise

        for j in containers_ret:
            containers = {"container_port": j.get("container_port"),
                          "protocol": j.get("protocol"),
                          "access_mode": j.get("access_mode"),
                          "access_scope": j.get("access_scope")}
            container.append(containers)

        for i in rc_ret:
            if i.get('policy') == 1:
                rc_krud = images[20:].replace("/", "_").replace(":", "_")
                pullpolicy = "Always"
            else:
                pullpolicy = "IfNotPresent"
                rc_krud = "null"

            command = self.command_query({'command': rc_ret.get('command')})

        return command, pullpolicy, rc_krud, images, service_name, namespace, pods_num, container, images

    def delete_pod(self, dict_data):

        try:
            command, pullpolicy, rc_krud, images, service_name, namespace, pods_num, \
                container, images = self.del_pod_element(dict_data)
        except Exception, e:
            log.error('parameters explain error when delete pod...reason=%s' % e)
            return False

        del_pod = {
                   "kind": "ReplicationController", "apiVersion": "v1",
                   "metadata": {
                       "namespace": namespace, "name": service_name,
                       "labels": {"component": service_name, "rc-krud": rc_krud, "name": service_name}
                   },
                   "spec": {
                      "replicas": pods_num,
                      "selector": {"name": service_name},
                      "template": {
                         "metadata": {
                            "labels": {"name": service_name, "logs": service_name}
                         },
                         "spec": {
                            "nodeSelector": {"role": "user"},
                            "imagePullSecrets": [{"name": "registry-key"}],
                            "containers": [
                               {
                                  "name": service_name, "image": images,
                                  "imagePullPolicy": pullpolicy,
                                  "command": command, "ports": self.container(container)
                               }
                            ]
                         }
                      }
                   }
                }

        if command == "" or command is None:
            j = 0
            for i in del_pod["spec"]["template"]["spec"]["containers"]:
                del del_pod["spec"]["template"]["spec"]["containers"][j]["command"]
                j += 1

        return del_pod

    def check_domain_use(self, dict_data):
        try:
            db_ret = self.service_db.identify_check(dict_data)
        except Exception, e:
            log.error('check the identify error, reason is: %s' % e)
            return 'error'

        if len(db_ret) == 0:
            return False
        if str(db_ret[0][0]) == 'None' or str(db_ret[0][1]) == 'None':
            return False
        if str(db_ret[0][1]) == '0':
            return 'not_need'
        if str(db_ret[0][1]) == '1':
            return db_ret[0][0] + ':' + str(db_ret[0][2]) + ':' + str(db_ret[0][1])

    def get_one_re(self, dict_data):
        ret = self.krpc_client.get_one_re(dict_data)
        log.info('get the service message is: %s, type is %s' % (ret, type(ret)))
        if ret.get('kind') != 'Service':
            return False
        else:
            return ret

    def add_service(self, dict_data):
        log.info('update the service(k8s) data is: %s' % dict_data)
        namespace = dict_data.get('project_uuid')
        service_name = dict_data.get('service_name')

        try:
            http_lb, tcp_lb, tcp_port = self.service_domain(dict_data)
            if dict_data.get('rtype') == 'lifecycle':
                tcp_port = self.service_db.get_using_port(dict_data)
                if len(tcp_port) == 0 or len(tcp_port[0]) == 0:
                    pass
                else:
                    tcp_lb = self.lb + ':' + tcp_port[0][0]
        except Exception, e:
            log.error('the domain create error, reason=%s' % e)
            return False

        try:
            container = dict_data.get('container')
        except Exception, e:
            log.error('service json create error, reason=%s' % e)
            return False

        try:
            service_name1 = service_name.lower().replace('_', '-')
            add_service = {
                           "rtype": "services", "kind": "Service", "apiVersion": "v1",
                           "metadata": {
                              "annotations": {"serviceloadbalancer/lb.http": http_lb,
                                              "serviceloadbalancer/lb.tcp": tcp_lb,
                                              "serviceloadbalancer/lb.node": self.node
                                              # "serviceloadbalancer/lb.node": "main"
                                              },
                              "name": service_name1,
                              "namespace": namespace,
                              "labels": {"name": service_name1},
                           },
                           "spec": {
                              "ports": self.service_port(container),
                              "selector": {"component": dict_data.get("service_name")}  # "name": service_name1}
                           },
                        }
            if dict_data.get('rtype') == 'container':
                ret = self.get_one_re(add_service)

                if ret is False:
                    return False
                else:
                    add_service['metadata']['resourceVersion'] = ret['metadata']['resourceVersion']
                    add_service['spec']['clusterIP'] = ret['spec']['clusterIP']

            if dict_data.get('rtype') == 'container':
                identify_check = self.check_domain_use(dict_data)
                if identify_check == 'error':
                    return False
                if identify_check and identify_check != 'not_need':
                    add_service['metadata']['annotations']['serviceloadbalancer/lb.http'] = identify_check.split(':')[0] \
                                                                                            + ':' + identify_check.split(':')[1]

            if http_lb == '' or http_lb is None:
                add_service['metadata']['annotations'].pop('serviceloadbalancer/lb.http')
            if tcp_lb == '' or tcp_lb is None:
                add_service['metadata']['annotations'].pop('serviceloadbalancer/lb.tcp')
            if (http_lb == '' and tcp_lb == '') or (http_lb is None and tcp_lb is None):
                add_service['metadata'].pop('annotations')

        except Exception, e:
            log.error('service create json error reason=%s' % e)
            return False

        return add_service

    def show_namespace(self, dict_data):
        namespace = dict_data.get('project_uuid')
        ns_ret = self.krpc_client.show_ns({'namespace': namespace})
        return ns_ret

    def create_namespace(self, dict_data):
        namespace = dict_data.get('project_uuid')
        ns_dict = {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": namespace}}
        ns_cre_ret = self.krpc_client.create_ns(ns_dict)

        if ns_cre_ret.get('kind') != 'Namespace':
            log.error('ns create error, create result is : %s' % ns_cre_ret)
            return False
        return True

    def create_secret(self, dict_data):
        namespace = dict_data.get('project_uuid')
        secret_dict = {"apiVersion": "v1", "kind": "Secret",
                       "metadata": {"name": "registry-key", "namespace": namespace},
                       "data":
                           {".dockerconfigjson":
                                "ewoJImF1dGhzIjogewoJCSJpbmRleC5ib3hsaW5rZXIuY29tIjogewoJCQkiYXV0aCI6ICJZbTk0YkdsdWEyVnlPbEZCV25kemVERXlNdz09IgoJCX0KCX0KfQ=="},
                       "type": "kubernetes.io/dockerconfigjson"
                       }
        secret_cre_ret = self.krpc_client.create_secret(secret_dict)
        if secret_cre_ret.get('kind') != 'Secret':
            return False
        return True

    def create_svc_account(self, dict_data):
        namespace = dict_data.get('project_uuid')
        service_account = self.krpc_client.get_account({'namespace': namespace, 'name': 'default'})
        log.info('get service account...the result is: %s, type is:%s' % (service_account, type(service_account)))

        account_json = {
                "kind": "ServiceAccount", "apiVersion": "v1",
                "metadata": {"name": "default", "namespace": namespace},
                "secrets": service_account.get("secrets"),
                "imagePullSecrets": [{"name": "registry-key"}]
            }

        cre_account = self.krpc_client.create_account(account_json)
        if not cre_account:
            log.error('service account create error, the create result is : %s' % cre_account)
            return False

        return True

    def access_container(self, context):
        con = []

        try:
            containers = self.service_db.detail_container(context)
        except Exception, e:
            log.error('query the database of containers error, reason=%s' % e)
            raise Exception('query the data of containers error')

        try:
            for i in containers:
                for j in context.get('ports'):
                    if j.get('containerPort') is not None and i.get('container_port') is not None:
                        if int(j.get('containerPort')) == int(i.get('container_port')):
                            access = {'container_port': j.get('containerPort'), 'protocol': i.get('protocol'),
                                      'access_mode': i.get('access_mode')}
                            con.append(access)
        except Exception, e:
            log.error('explain the containers data error, reason is: %s' % e)
            raise Exception('explain the containers data error')

        return con

    def get_pod_name(self, context):
        pod = []
        con_ret = []
        pod_message = {"namespace": context.get("project_uuid"), 'rtype': 'pods'}

        try:
            response = self.krpc_client.get_pod_messages(pod_message).get('items')
        except Exception, e:
            log.error("explain the kubernetes response error,reason=%s" % e)
            return False

        try:
            for i in response:
                if context.get("service_name") == i.get("metadata").get("labels").get("component"):

                    if context.get('rtype') == 'pods_msg':
                        for j in i.get("spec").get("containers"):
                            p = {"ports": j.get("ports")}
                            p.update(context)
                            try:
                                con_ret = self.access_container(p)
                            except Exception, e:
                                log.error('corresponding containers ports error, reason=%s' % e)
                                return False
                    # state = i.get("status").get("containerStatuses")[0].get('state')
                    # if state.has_key('waiting'):
                    #     status = state.get('waiting').get('reason')
                    # else:
                    #     status = 'Running'

                    status = i.get('status').get('phase')

                    pod_ms = {"pod_phase": status, "pod_name": i.get("metadata").get("name"),
                              "pod_ip": i.get("status").get("podIP"), 'containers': con_ret}
                    pod.append(pod_ms)
        except Exception, e:
            log.error("explain the pods messages error,reason=%s" % e)
            return False

        return pod

    def inner_delete_pod(self, context):
        pods = self.get_pod_name(context)
        if pods is False:
            log.error('PODS MESSAGES GET ERROR')
            return request_result(502)

        for i in pods:
            log.info('pod_name is: %s' % i.get('pod_name'))
            del_pod_json = {'namespace': context.get('project_uuid'), 'name': i.get('pod_name'), 'rtype': 'pods'}
            pod_ret = self.krpc_client.delete_service_a_rc(del_pod_json)

            if pod_ret.get('code') not in [200, 404] and pod_ret.get('code') is not None:
                log.error('DELETE POD RESULT IS--POD:%s' % pod_ret)
                return request_result(502)

        return True

    @staticmethod
    def easy_struct(context, target_json):
        target_json['token'] = context.get('token')
        target_json['user_uuid'] = context.get('user_uuid')

        return target_json

    def create_service(self, context):

        ns_if_exist = self.show_namespace(context)
        log.info('namespace ns_if_exist result is: %s' % ns_if_exist)
        if ns_if_exist.get('kind') != 'Namespace':
            ret_ns = self.create_namespace(context)
            ret_secret = self.create_secret(context)
            ret_account = self.create_svc_account(context)

            if not ret_ns or not ret_secret or not ret_account:
                log.error('CREATE NS,SECRET,ACCOUNT ERROR, RESULT:NS: %s,SECRET: %s, ACCOUNT: %s' %
                          (ret_ns, ret_secret, ret_account))
                return request_result(501)

        add_rc = self.add_rc(context)
        add_service = self.add_service(context)
        ingress_json = self.add_ingress_http(context)
        config_map_json = self.add_config_map(context)

        if add_rc is False or add_service is False or ingress_json is False or config_map_json is False:
            return request_result(501)

        add_rc = self.easy_struct(context, add_rc)
        add_service = self.easy_struct(context, add_service)

        self.krpc_client.create_services(add_rc)
        self.krpc_client.create_services(add_service)
        if ingress_json is not None and ingress_json is not False:
            ingress_json = self.easy_struct(context, ingress_json)
            self.krpc_client.create_ingress(ingress_json)
        if config_map_json is not None and config_map_json is not False:
            config_map_json = self.easy_struct(context, config_map_json)
            config_map_json['rtype'] = 'configmaps'
            self.krpc_client.create_services(config_map_json)

        return True

    def delete_service(self, context):

        pods = self.get_pod_name(context)
        if pods is False:
            log.error('PODS MESSAGES GET ERROR')
            return request_result(503)

        namespace = context.get('project_uuid')
        name = context.get('service_name').lower().replace('_', '-')

        del_rc_json = {'namespace': namespace, 'name': name, 'rtype': 'replicationcontrollers'}
        del_svc_json = {'namespace': namespace, 'name': name, 'rtype': 'services'}
        del_ing_json = {'namespace': namespace, 'name': name, 'rtype': 'ingress'}
        del_confmap_json = {'namespace': namespace, 'name': name, 'rtype': 'configmaps'}

        rc_ret = self.krpc_client.delete_service_a_rc(del_rc_json)
        svc_ret = self.krpc_client.delete_service_a_rc(del_svc_json)
        ing_ret = self.krpc_client.delete_service_a_rc(del_ing_json)
        configmap_ret = self.krpc_client.delete_service_a_rc(del_confmap_json)
        log.info('select configmap result is: %s' % configmap_ret)

        for i in pods:
            log.info('pod_name is: %s' % i.get('pod_name'))
            del_pod_json = {'namespace': namespace, 'name': i.get('pod_name'), 'rtype': 'pods'}
            pod_ret = self.krpc_client.delete_service_a_rc(del_pod_json)

            if pod_ret.get('code') != 200 and pod_ret.get('code') is not None:
                log.error('DELETE POD RESULT IS--POD:%s' % pod_ret)
                return request_result(503)

        if (rc_ret.get('code') != 200 and rc_ret.get('code') != 404) or \
                (svc_ret.get('code') != 200 and svc_ret.get('code') != 404) or \
                (ing_ret.get('code') != 200 and ing_ret.get('code') != 404) or \
                (configmap_ret.get('code') != 200 and configmap_ret.get('code') != 404):
            log.error('DELETE SERVICE RESULT IS--RC:%s;SERVICE:%s,'
                      'INGRESS: %s, CONFIGMAP: %s' % (rc_ret, svc_ret, ing_ret, configmap_ret))

            return request_result(503)

        return True

    def update_rc(self, context):
        try:
            svc_detail_original = self.metal.service_detail(context)
        except Exception, e:
            log.error('get the service original details(kubernetes_driver) message error, reason=%s' % e)
            return request_result(404)

        if svc_detail_original.get('status') != 0:
            return request_result(404)

        try:
            log.info('context is %s, type is %s' % (context, type(context)))

            svc_detail = svc_detail_original.get('result')
            svc_detail['service_name'] = context.get('service_name')
            svc_detail['project_uuid'] = context.get('project_uuid')
            svc_detail['rtype'] = context.get('rtype')
            svc_detail['image_id'] = svc_detail.get('image_id')
            svc_detail['token'] = context.get('token')
            if context.get('rtype') == 'container':
                svc_detail['team_name'] = context.get('team_name')
                svc_detail['project_name'] = context.get('project_name')
        except Exception, e:
            log.error('struct the params when update service error, reason=%s' % e)
            return request_result(502)

        try:
            rc_up_json = self.add_rc(svc_detail)
            if context.get('rtype') == 'container':
                svc_up_json = self.add_service(svc_detail)
                svc_up_json['rtype'] = 'services'
        except Exception, e:
            log.error('rc_json or svc json struct error, reason=%s' % e)
            return request_result(502)

        rc_up_json['rtype'] = 'replicationcontrollers'
        if context.get('operate') == 'stop':
            rc_up_json['spec']['replicas'] = 0

        rc_up_ret = self.krpc_client.update_service(rc_up_json)
        if context.get('rtype') == 'container':
            log.info('update the container json data is: %s' % svc_up_json)
            svc_up_ret = self.krpc_client.update_service(svc_up_json)
            if svc_up_ret.get('result') != '<Response [200]>':
                log.error('SERVICE UPDATE RESULT IS: %s' % svc_up_ret)
                return request_result(502)

        if rc_up_ret.get('result') != '<Response [200]>':
            log.info('SERVICE UPDATE ERROR,RC_RET---:%s' % rc_up_ret)
            return request_result(502)

        ret = self.inner_delete_pod(context)
        if ret is not True:
            return ret

        return True

    def update_ingress(self, dict_data):
        service_name = dict_data.get('service_name')
        namespace = dict_data.get('project_uuid')

        try:
            certify = self.service_db.get_ingress_certify(namespace, service_name)[0][0]
        except Exception, e:
            log.error('get_ingress_certify error, reason is: %s' % e)
            raise Exception('get ingress certify error')

        for c in dict_data.get('container'):
            if c.get('access_mode') == 'TCP':
                return {'kind': 'Ingress'}

        domain_http = ''
        for i in dict_data.get('container'):
            log.info('the container data for update ingress data is: %s' % i)
            if i.get('domain') is not None and i.get('domain') != 'NULL' and i.get('domain') != '' and str(i.get('identify')) != '0':
                domain_http = i.get('domain')
            else:
                team_name = dict_data.get('team_name')
                project_name = dict_data.get('project_name')
                if project_name is not None and project_name != '' and project_name != team_name:
                    domain_http = '%s-%s-%s.%s' % (team_name, project_name, service_name, self.lb)
                else:
                    domain_http = '%s-%s.%s' % (team_name, service_name, self.lb)

        log.info('update the ingress the domain_http is: %s' % domain_http)
        container_port = self.ingress_port(dict_data)

        if certify == 'HTTP' or certify == 'http':
            if self.lb in domain_http:
                ingress_json = {
                            "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                            "metadata": {
                                "name": service_name, "namespace": namespace,
                                "annotations": {"kubernetes.io/ingress.class": "nginx",
                                                "loadbalancer/lb.name": "user"}
                            },
                            "spec": {"rules": [{"host": domain_http,
                                                "http": {"paths": [{"path": "/",
                                                                    "backend": {"serviceName": service_name,
                                                                                "servicePort": container_port}
                                                                    }]
                                                         }
                                                }]
                                     }
                        }
            else:
                domain_http1 = ''
                if 'www.' in domain_http:
                    domain_http1 = domain_http.replace('www.', '')
                if 'www.' not in domain_http:
                    domain_http1 = 'www.' + domain_http
                ingress_json = {
                            "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                            "metadata": {
                                "name": service_name, "namespace": namespace,
                                "annotations": {"kubernetes.io/ingress.class": "nginx",
                                                "loadbalancer/lb.name": "user"}
                            },
                            "spec": {"rules": [{"host": domain_http,
                                                "http": {"paths": [{"path": "/",
                                                                    "backend": {"serviceName": service_name,
                                                                                "servicePort": container_port}
                                                                    }]
                                                         }
                                                },
                                               {"host": domain_http1,
                                                "http": {"paths": [{"path": "/",
                                                                    "backend": {"serviceName": service_name,
                                                                                "servicePort": container_port}
                                                                    }]
                                                         }
                                                }]
                                     }
                        }
            log.info('update the ingress json is: %s' % ingress_json)
            ret = self.krpc_client.update_ingress(ingress_json)

        elif certify == 'HTTPS' or certify == 'https':
            if self.lb in domain_http:
                ingress_json = {
                            "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                            "metadata": {
                                "name": service_name, "namespace": namespace,
                                "annotations": {"kubernetes.io/ingress.class": "nginx",
                                                "nginx.org/ssl-services": service_name,
                                                "loadbalancer/lb.name": "user"}
                            },
                            "spec": {"rules": [{"host": domain_http,
                                                "http": {"paths": [{"path": "/",
                                                                    "backend": {"serviceName": service_name,
                                                                                "servicePort": 443}
                                                                    }]
                                                         }
                                                }],
                                     "tls": [{'secretName': 'certify-https'}],
                                     "backend": {"serviceName": service_name,
                                                 "servicePort": container_port}
                                     }
                        }
            else:
                domain_http1 = ''
                if 'www.' in domain_http:
                    domain_http1 = domain_http.replace('www.', '')
                if 'www.' not in domain_http:
                    domain_http1 = 'www.' + domain_http
                ingress_json = {
                            "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                            "metadata": {
                                "name": service_name, "namespace": namespace,
                                "annotations": {"kubernetes.io/ingress.class": "nginx",
                                                "nginx.org/ssl-services": service_name,
                                                "loadbalancer/lb.name": "user"}
                            },
                            "spec": {"rules": [{"host": domain_http,
                                                "http": {"paths": [{"path": "/",
                                                                    "backend": {"serviceName": service_name,
                                                                                "servicePort": 443}
                                                                    }]
                                                         }
                                                },
                                               {"host": "%s" % domain_http1,
                                                "http": {"paths": [{"path": "/",
                                                                    "backend": {"serviceName": service_name,
                                                                                "servicePort": 443}
                                                                    }]
                                                         }
                                                }],
                                     "tls": [{'secretName': 'certify-https'}],
                                     "backend": {"serviceName": service_name,
                                                 "servicePort": container_port}
                                     }
                        }
            log.info('update the ingress json is: %s' % ingress_json)
            ret = self.krpc_client.update_ingress(ingress_json)

        else:
            ret = {'kind': 'Ingress'}

        return ret

    def update_configmap(self, context):
        for i in context.get('container'):
            if i.get('access_mode') in ['HTTP', 'HTTPS']:
                return {'kind': 'ConfigMap'}

        for i in context.get('container'):
            if i.get('access_scope') == 'outsisde':
                try:
                    use_port = self.service_db.get_svc_port(context)[0][0]
                    log.info('更新TCP获取到的已用端口为:%s' % use_port)
                except Exception, e:
                    log.error('get the using port error, reason is: %s' % e)
                    return request_result(404)

                try:
                    config_json = self.add_config_map(context)
                    config_json['data']['hostport'] = str(use_port)
                    config_json['rtype'] = 'configmaps'
                except Exception, e:
                    log.error('configmap json struct error, reason is: %s' % e)
                    return request_result(502)

                ret = self.krpc_client.update_service(config_json)
                log.info('update the configmap result is: %s, type is: %s' % (ret, type(ret)))
                if ret.get('result') != '<Response [200]>':
                    return request_result(502)

        return {'kind': 'ConfigMap'}

    def identify_update(self, context):

        try:
            svc_detail_original = self.metal.service_detail(context)
        except Exception, e:
            log.error('get the service original details(kubernetes_driver) message error, reason=%s' % e)
            return request_result(404)

        if svc_detail_original.get('status') != 0:
            return request_result(404)

        try:
            log.info('context is %s, type is %s' % (context, type(context)))

            svc_detail = svc_detail_original.get('result')
            svc_detail['service_name'] = context.get('service_name')
            svc_detail['project_uuid'] = context.get('project_uuid')
            svc_detail['rtype'] = 'container'
            svc_detail['image_id'] = svc_detail.get('image_id')
            svc_detail['token'] = context.get('token')
            svc_detail['team_name'] = context.get('team_name')
            svc_detail['project_name'] = context.get('project_name')
        except Exception, e:
            log.error('struct the params when update service error, reason=%s' % e)
            return request_result(502)

        try:

            svc_up_json = self.add_service(svc_detail)
            svc_up_json['rtype'] = 'services'
        except Exception, e:
            log.error('svc json struct error, reason=%s' % e)
            return request_result(502)

        log.info('update service(be structed to k8s) json data is: %s' % svc_up_json)
        svc_up_ret = self.krpc_client.update_service(svc_up_json)
        if svc_up_ret.get('result') != '<Response [200]>':
            log.error('SERVICE UPDATE RESULT IS: %s' % svc_up_ret)
            return request_result(502)

        try:
            ingress_ret = self.update_ingress(svc_detail)
            log.info('update the ingress result is: %s' % ingress_ret)
        except Exception, e:
            log.error('update the ingress error, reason is: %s' % e)
            return request_result(502)

        if ingress_ret.get('kind') != 'Ingress':
            return request_result(502)

        return True

    def http_tcp_change(self, context):
        namespace = context.get('project_uuid')
        name = context.get('service_name')
        try:
            db_ret = self.service_db.get_container_msg(context)
            container = []
            for i in db_ret:
                container_port = i[0]
                protocol = i[1]
                access_mode = i[2]
                access_scope = i[3]

                container.append({'container_port': container_port, 'protocol': protocol,
                                  'access_mode': access_mode, 'access_scope': access_scope})
        except Exception, e:
            log.error('get the container message from databse error, reason is: %s' % e)
            raise Exception('get the container message from databse error')

        for m in container:
            if m.get('access_mode') == 'http' or m.get('access_mode') == 'HTTP' or m.get('access_mode') == 'HTTPS':
                for n in context.get('container'):
                    if n.get('access_mode') == 'tcp' or n.get('access_mode') == 'TCP' or n.get('access_mode') == 'UDP':
                        try:
                            m_port = self.service_db.max_used_port()[0][0]
                            self.service_db.update_using_port(int(m_port)+1, namespace, name)
                        except Exception, e:
                            log.error('get the max port error, reason is: %s' % e)
                            raise Exception('oprater database error')

                        del_ing_json = {'namespace': namespace, 'name': name, 'rtype': 'ingress'}
                        ing_ret = self.krpc_client.delete_service_a_rc(del_ing_json)
                        if ing_ret.get('code') != 200 and ing_ret.get('code') != 404:
                            raise Exception('ingress delete error when change the http tp tcp')

                        config_map_json = self.add_config_map(context)
                        if config_map_json is not None and config_map_json is not False:
                            config_map_json = self.easy_struct(context, config_map_json)
                            config_map_json['rtype'] = 'configmaps'
                            self.krpc_client.create_services(config_map_json)
                            tcp_port = int(self.service_db.max_used_port()[0][0])+1
                            n['tcp_port'] = tcp_port
                            self.service_db.http_to_tcp_container(namespace, name, n)

                        return True

            if m.get('access_mode') == 'tcp' or m.get('access_mode') == 'TCP' or m.get('access_mode') == 'UDP':
                for n in context.get('container'):
                    if n.get('access_mode') == 'http' or n.get('access_mode') == 'HTTP' or n.get('access_mode') == 'HTTPS':
                        del_confmap_json = {'namespace': namespace, 'name': name, 'rtype': 'configmaps'}
                        configmap_ret = self.krpc_client.delete_service_a_rc(del_confmap_json)
                        if configmap_ret.get('code') != 200 and configmap_ret.get('code') != 404:
                            raise Exception('configmap delete error when change the tcp tp http')

                        ingress_json = self.add_ingress_http(context)
                        if ingress_json is not None and ingress_json is not False:
                            ingress_json = self.easy_struct(context, ingress_json)
                            self.krpc_client.create_ingress(ingress_json)

                        # else:
                        #     log.error('ingress json struct error')
                        #     raise Exception('ingress json struct error')

                        return True

        return False

    def out_in_change(self, context):
        namespace = context.get('project_uuid')
        name = context.get('service_name')
        try:
            db_ret = self.service_db.get_container_msg(context)
            container = []
            for i in db_ret:
                container_port = i[0]
                protocol = i[1]
                access_mode = i[2]
                access_scope = i[3]

                container.append({'container_port': container_port, 'protocol': protocol,
                                  'access_mode': access_mode, 'access_scope': access_scope})
        except Exception, e:
            log.error('get the container message from databse error, reason is: %s' % e)
            raise Exception('get the container message from databse error')

        for m in container:
            for n in context.get('container'):
                if m.get('access_scope') == n.get('access_scope') and \
                        m.get('access_mode') in ['HTTP', 'TCP', 'HTTPS', 'UDP'] \
                        and n.get('access_mode') in ['HTTP', 'TCP', 'HTTPS', 'UDP']:
                    return True
                if m.get('access_scope') == 'inside' and n.get('access_scope') == 'outsisde' and \
                        m.get('access_mode') in ['HTTP', 'TCP', 'HTTPS', 'UDP'] and \
                        n.get('access_mode') in ['HTTP', 'TCP', 'HTTPS', 'UDP']:
                    if n.get('access_mode') == 'HTTP' or n.get('access_mode') == 'HTTPS':

                        ingress_json = self.add_ingress_http(context)
                        if ingress_json is not None and ingress_json is not False:
                            ingress_json = self.easy_struct(context, ingress_json)
                            self.krpc_client.create_ingress(ingress_json)

                        else:
                            log.error('ingress json struct error')
                            raise Exception('ingress json struct error')

                    if n.get('access_mode') == 'TCP' or n.get('access_mode') == 'UDP':
                        config_map_json = self.add_config_map(context)
                        if config_map_json is not None and config_map_json is not False:
                            config_map_json = self.easy_struct(context, config_map_json)
                            config_map_json['rtype'] = 'configmaps'
                            self.krpc_client.create_services(config_map_json)
                            tcp_port = int(self.service_db.max_used_port()[0][0])+1
                            n['tcp_port'] = tcp_port
                            self.service_db.http_to_tcp_container(namespace, name, n)
                        else:
                            log.error('config map struct json error')
                            raise Exception('config map struct json error')

                    return False

                if m.get('access_scope') == 'outsisde' and n.get('access_scope') == 'inside' \
                        and m.get('access_mode') in ['HTTP', 'TCP', 'HTTPS', 'UDP'] and n.get('access_mode') in ['HTTP', 'TCP', 'HTTPS', 'UDP']:
                    if m.get('access_mode') == 'HTTP' or m.get('access_mode') == 'HTTPS':
                        del_ing_json = {'namespace': namespace, 'name': name, 'rtype': 'ingress'}
                        ing_ret = self.krpc_client.delete_service_a_rc(del_ing_json)
                        if ing_ret.get('code') != 200 and ing_ret.get('code') != 404:
                            raise Exception('ingress delete error when change the http tp tcp')

                    if m.get('access_mode') == 'TCP' or m.get('access_mode') == 'UDP':
                        del_confmap_json = {'namespace': namespace, 'name': name, 'rtype': 'configmaps'}
                        configmap_ret = self.krpc_client.delete_service_a_rc(del_confmap_json)
                        if configmap_ret.get('code') != 200 and configmap_ret.get('code') != 404:
                            raise Exception('configmap delete error when change the tcp tp http')

                    return False

        return True

    def update_certify(self, context):
        try:
            self.service_db.update_ingress_certify(context)
        except Exception, e:
            log.error('update the database error, reason is: %s' % e)
            return request_result(403)

        try:
            ingress_ret = self.identify_update(context)
            if ingress_ret is True:
                return request_result(0, {'resource_name': context.get('service_name')})
        except Exception, e:
            log.error('struct the update ingress json error, reason is: %s' % e)
            return request_result(503)

    def update_volume_status(self, dict_data):
        using_volume = self.service_db.get_using_volume(dict_data)
        log.info('from database get the using volumes is: %s' % using_volume)
        ch_volume = dict()
        to_change_volume = []
        for i in using_volume:
            ch_volume['volume_uuid'] = i.get('volume_uuid')
            to_change_volume.append(copy.deepcopy(ch_volume))
            log.info('explain the database data ,ch_volume is: %s,to_change_volume is: %s' % (ch_volume,
                                                                                              to_change_volume))

        result = self.volume.storage_status({'volume': to_change_volume, 'action': 'put',
                                             'token': dict_data.get('token')})
        if result is False:
            return False

        return True

    def update_env(self, context):

        database_ret = self.service_db.update_env(context)
        if database_ret is False:
            return request_result(403)

        service_ret = self.update_rc(context)
        if service_ret is not True:
            return service_ret

        return True

    def update_cm(self, context):
        try:
            database_ret = self.service_db.update_cm(context)
        except Exception, e:
            log.error('database update error, reason is: %s' % e)
            return request_result(403)
        if database_ret is not None:
            return request_result(403)

        service_ret = self.update_rc(context)
        if service_ret is not True:
            return service_ret

        return True

    def update_volume(self, context):
        database_ret = self.service_db.update_volume(context)
        if database_ret is False:
            return request_result(403)

        service_ret = self.update_rc(context)
        if service_ret is not True:
            return service_ret

        return True

    def update_container(self, context):
        context['container_update'] = 'yes'
        try:
            change_check = self.http_tcp_change(context)
        except Exception, e:
            log.error('check if the service is change with http and tcp error, reason is: %s' % e)
            return request_result(502)
        try:
            in_out_check = self.out_in_change(context)
        except Exception, e:
            log.error('check outside or inside change error, reason is: %s' % e)
            return request_result(502)
        try:
            con_ret = self.check_domain_use(context)
            log.info('get the domain use or not result is: %s' % con_ret)
        except Exception, e:
            log.error('get the domain message error, reason is: %s' % e)
            return request_result(404)

        try:
            container = self.container_domain(context)
            log.info('struct the container result when update the container is: %s' % container)
        except Exception, e:
            log.error('list the container message error, reason is: %s' % e)
            return request_result(502)
        if con_ret is not False and con_ret != 'not_need':
            try:
                domain = con_ret.split(':')[0]
                identify = con_ret.split(':')[2]
                if domain:
                    for i in container:
                        if i.get('http_domain') is not None:
                            i['domain'] = domain
                            i['identify'] = identify
            except Exception, e:
                log.error('get the domain error, reason is: %s' % e)
                return request_result(502)

        if con_ret == 'not_need':
            try:
                ret_domain = self.service_db.identify_check(context)
                for i in container:
                    if i.get('http_domain') is not None:
                        i['domain'] = ret_domain[0][0]
                        i['identify'] = ret_domain[0][1]
            except Exception, e:
                log.error('get the domain message again error, reason is: %s' % e)
                return request_result(404)

        new_container = {'container': container}
        context.update(new_container)

        try:
            self.service_db.update_container(context)
            log.info('important message for if change or not is: change check:%s, in_out_check: %s' % (change_check,
                                                                                                       in_out_check) )
            if (not change_check) and in_out_check:

                ingress_ret = self.update_ingress(context)
                config_ret = self.update_configmap(context)
                if ingress_ret.get('kind') != 'Ingress' or config_ret.get('kind') != 'ConfigMap':
                    log.error('update the ingress or configmap error, ')
                    log.info('ingress_ret is: %s, configmap_ret is: %s' % (ingress_ret, config_ret))
                    return request_result(502)
        except Exception, e:
            log.error('container inner database error, reason is: %s' % e)
            return request_result(403)

        rc_ret = self.update_rc(context)
        if rc_ret is not True:
            log.error('RC UPDATE RESULT IS:%s' % rc_ret)
            return request_result(502)

        return True

    def update_status(self, context):
        try:
            db_result = self.service_db.update_status(context)
        except Exception, e:
            log.error('update status error, reason is:%s' % e)
            return request_result(403)
        if db_result is False:
            return request_result(403)

        rc_ret = self.update_rc(context)
        if rc_ret is not True:
            log.error('RC UPDATE RESULT IS:%s' % rc_ret)
            return request_result(502)

        return True

    def update_telescopic(self, context):
        try:
            db_result = self.service_db.update_telescopic(context)
        except Exception, e:
            log.error('update status error, reason is:%s' % e)
            return request_result(403)
        if db_result is False:
            return request_result(403)

        rc_ret = self.update_rc(context)
        if rc_ret is not True:
            log.error('RC UPDATE RESULT IS:%s' % rc_ret)
            return request_result(502)

        return True

    def update_publish(self, context):
        try:
            self.service_db.update_publish(context)
        except Exception, e:
            log.error('update the database error, reason is: %s' % e)
            return request_result(403)

        try:
            rc_ret = self.update_rc(context)
            if rc_ret is not True:
                log.error('RC UPDATE RESULT IS:%s' % rc_ret)
                return request_result(502)
        except Exception, e:
            log.error('update the service error, reason is: %s' % e)
            return request_result(502)

        return True

    def update_command(self, context):
        try:
            db_result = self.service_db.update_command(context)
        except Exception, e:
            log.error('update status error, reason is:%s' % e)
            return request_result(403)
        if db_result is False:
            return request_result(403)

        rc_ret = self.update_rc(context)
        if rc_ret is not True:
            log.error('RC UPDATE RESULT IS:%s' % rc_ret)
            return request_result(502)

        return True

    def update_domain(self, context):
        try:
            ret_http = self.service_db.get_http_domain(context)
            log.info('get the http_domain message is: %s,ret_http[0] is: %s' % (ret_http, ret_http[0]))
            if int(ret_http[0][0]) != 0:
                return request_result(301)
        except Exception, e:
            log.error('get the http_domain to identify the domain error, reason is: %s' % e)
            return request_result(404)

        try:
            domain = self.service_db.get_domain(context)
        except Exception, e:
            log.error('get the domain message error, reason is: %s' % e)
            return request_result(404)

        if context.get('domain') is not None and context.get('domain') != '':
            if len(domain[0]) != 0 and str(domain[0][1]) == '1':
                try:
                    self.service_db.update_http_domain(context)
                except Exception, e:
                    log.error('update the http_domain error, reason is: %s' % e)
                    return request_result(403)

            try:
                db_result = self.service_db.update_domain(context)
            except Exception, e:
                log.error('update status error, reason is:%s' % e)
                return request_result(403)
            if db_result is False:
                return request_result(301)

        else:
            try:
                if len(domain[0]) != 0:
                    up_ret = self.service_db.update_domain_to_none(context)
                    if up_ret is not None:
                        log.info('UPDATE THE DATABASE ERROR')
                        return request_result(403)

                    if int(domain[0][1]) == 1:
                        result = self.identify_update(context)
                        return result

                return request_result(0, 'update successfully')

            except Exception, e:
                log.error('after get the domain message, update the service error, reason is:%s' % e)
                return request_result(502)

        return True

    def update_identify(self, context):
        try:
            domain = self.service_db.get_domain(context)
        except Exception, e:
            log.error('get the domain message error, reason is: %s' % e)
            return request_result(404)

        if int(context.get('identify')) == 0 and int(domain[0][1]) == 1:
            return request_result(0, "sorry admin, we don't need to do this")

        if int(context.get('identify')) == 1 and int(domain[0][1]) == 0:
                try:
                    self.service_db.update_identify_to_1(context)
                    self.service_db.update_http_domain(context)
                except Exception, e:
                    log.error('update the databse for domain to can not use error, reason is: %s' % e)
                    return request_result(403)

                try:
                    ret = self.identify_update(context)
                    return ret
                except Exception, e:
                    log.error('update the service(k8s) error, reason is: %s' % e)
                    return request_result(502)

        else:
            log.info('not need to change anything...')
            return True

    def update_description(self, context):
        try:
            ret = self.service_db.update_description(context)
            if ret is not None:
                log.error('UPDATE THE DATABASE ERROR')
                return request_result(403)
            return True
        except Exception, e:
            log.error('update the description error, reason is: %s' % e)
            return request_result(403)

    def all_use_up(self, context):
        try:
            inner_context = self.metal.get_container(context)
            ret = self.update_configmap(inner_context)
            if ret.get('kind') != 'ConfigMap':
                return request_result(502)
        except Exception, e:
            log.error('all update error, reason is: %s' % e)
            return request_result(502)

        return

    def update_main(self, context):
        rtype = context.get('rtype')

        if rtype == 'env':
            ret = self.update_env(context)

            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'cm':
            ret = self.update_cm(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'volume':
            ret = self.update_volume(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'container':
            ret = self.update_container(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'status':
            ret = self.update_status(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'telescopic':
            ret = self.update_telescopic(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'policy':
            ret = self.update_publish(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'command':
            ret = self.update_command(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        if rtype == 'domain':
            ret = self.update_domain(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret
        if rtype == 'identify':
            ret = self.update_identify(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret
        if rtype == 'description':
            ret = self.update_description(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret
        if rtype == 'certify':
            ret = self.update_certify(context)
            config_ret = self.all_use_up(context)
            if config_ret is not None:
                return config_ret

            return ret

        return True
