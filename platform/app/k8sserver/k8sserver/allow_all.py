# -*- coding: utf-8 -*-
# Author: wang-xf <it-wangxf@all-reach.com>
# Date: 17/5/3 下午4:07

from common.logs import logging as log
import requests
import json
import os


class AllowAll(object):

    def __init__(self):
        with open(os.environ.get('TOKEN_PATH'), 'r') as f:
            token = f.read()
        auth_info = 'Bearer %s' % token
        self.HEADERS = {'Authorization': auth_info}
        self.host_address = 'https://kubernetes.default.svc:443/api/v1'
        self.ing_address = 'https://kubernetes.default.svc:443/apis/extensions/v1beta1/namespaces'

    def get_ns(self):
        ns = []
        url = "%s/namespaces" % self.host_address

        ret = requests.get(url, headers=self.HEADERS, verify=False)

        namespaces = json.loads(ret.text)
        if namespaces.get('kind') != 'NamespaceList':
            return False
        for i in namespaces.get('items'):
            ns.append(i.get('metadata').get('name'))

        return ns

    def create_config_map(self, config_json, namespace):
        url = "%s/namespaces/%s/configmaps" % (self.host_address, namespace)

        ret = requests.post(url, data=json.dumps(config_json), headers=self.HEADERS, verify=False)
        ret = json.loads(ret.text)

        if ret.get('kind') != 'ConfigMap':
            return False

        return ret

    def create_ingress(self, ing_json, namespace):
        url = "%s/%s/ingresses" % (self.ing_address, namespace)

        ret = requests.post(url, data=json.dumps(ing_json), headers=self.HEADERS, verify=False)

        ret = json.loads(ret.text)

        if ret.get('kind') != 'Ingress':
            return False

        return ret

    def create_resources(self, ns):
        try:
            for i in ns:
                url = "%s/namespaces/%s/services" % (self.host_address, i)

                svcs = requests.get(url, headers=self.HEADERS, verify=False)

                svc = json.loads(svcs.text)

                if svc.get('kind') != 'ServiceList':
                    return False

                for j in svc.get('items'):

                    namespace = j.get('metadata').get('namespace')
                    if j.get('metadata').get('annotations') is not None:
                        lb_http = j.get('metadata').get('annotations').get('serviceloadbalancer/lb.http')
                        lb_tcp = j.get('metadata').get('annotations').get('serviceloadbalancer/lb.tcp')

                        service_name = j.get('metadata').get('name')
                        container_port = j.get('spec').get('ports')[0].get('port')

                        if lb_http is not None and namespace == 'boxlinker':
                            domain_http = lb_http.split(':')[0]

                            ingress_json = {
                                            "apiVersion": "extensions/v1beta1", "kind": "Ingress",
                                            "metadata": {
                                                "name": service_name, "namespace": namespace,
                                                "annotations": {"kubernetes.io/ingress.class": "nginx",
                                                                "nginx.org/ssl-services": service_name,
                                                                "loadbalancer/lb.name": "system"}
                                            },
                                            "spec": {"rules": [{"host": domain_http,
                                                                "http": {"paths": [{"path": "/",
                                                                                    "backend": {"serviceName": service_name,
                                                                                                "servicePort": 443}
                                                                                    }]
                                                                         }
                                                                }],
                                                     "tls": [{'secretName': 'foo-secret'}],
                                                     "backend": {"serviceName": service_name,
                                                                 "servicePort": container_port}
                                                     }
                                        }

                            retss = self.create_ingress(ingress_json, namespace)

                            log.info('create the ingress result is: %s' % retss)

                        if lb_http is not None and namespace != 'boxlinker':
                            domain_http = lb_http.split(':')[0]

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

                            retss = self.create_ingress(ingress_json, namespace)

                            log.info('create the ingress result is: %s' % retss)

                        if lb_tcp is not None and namespace != 'boxlinker':
                            container_port = lb_tcp.split(':')[0]
                            config_map_json = {
                                "apiVersion": "v1",
                                "kind": "ConfigMap",
                                "metadata": {"name": service_name, "namespace": namespace,
                                             "annotations": {"loadbalancer/lb.name": "user"}},
                                "data": {"host": "lb1.boxlinker.com", "hostport": str(container_port),
                                         "servicename": service_name}
                            }

                            config_map_ret = self.create_config_map(config_map_json, namespace)

                            log.info('create the configmap result is: %s' % config_map_ret)

                        if lb_tcp is not None and namespace == 'boxlinker':
                            container_port = lb_tcp.split(':')[0]
                            config_map_json = {
                                "apiVersion": "v1",
                                "kind": "ConfigMap",
                                "metadata": {"name": service_name, "namespace": namespace,
                                             "annotations": {"loadbalancer/lb.name": "system"}},
                                "data": {"host": "boxlinker.com", "hostport": str(container_port),
                                         "servicename": service_name}
                            }

                            config_map_ret = self.create_config_map(config_map_json, namespace)

                            log.info('create the configmap result is: %s' % config_map_ret)
        except Exception, e:
            log.error('going wrong way, reason is: %s' % e)
            raise Exception('going wrong way')

        return

    def mains(self):
        ns = self.get_ns()
        self.create_resources(ns)



