#! /usr/bin/ python
# -*- coding:utf8 -*-
# Date: 2016/7/22
# author:王晓峰
import urllib
import requests
import json
import urllib2
import os
from common.logs import logging as log
from common.code import request_result


class KApiMethods(object):

    def __init__(self):
        with open(os.environ.get('TOKEN_PATH'), 'r') as f:
            token = f.read()
        auth_info = 'Bearer %s' % token
        self.HEADERS = {'Authorization': auth_info}
        self.host_address = 'https://kubernetes.default.svc:443/api/v1'
        self.ing_address = 'https://kubernetes.default.svc:443/apis/extensions/v1beta1/namespaces'

    def delete_namespace(self, dict_data):
        log.info('delete the ns dict is: %s' % dict_data)
        namespace = dict_data.get('namespace')
        url = '%s/namespaces/%s' % (self.host_address, namespace)
        msg = requests.delete(url, headers=self.HEADERS, verify=False)
        log.info('delete the kubernetes ns result is : %s' % msg.text)
        return json.loads(msg.text)

    def get_account(self, dict_data):
        account_name = dict_data.get('name')
        namespace = dict_data.get('namespace')
        url = '%s/namespaces/%s/serviceaccounts/%s' % (self.host_address, namespace, account_name)
        msg = requests.get(url, headers=self.HEADERS, verify=False)
        res = msg.text

        log.info('get account result is %s,type is %s' % (res, type(res)))

        return json.loads(res)

    def get_noup_resource(self, json_list):
        rtype = json_list.pop('rtype')
        params = urllib.urlencode(json_list)
        url = '%s/%s?%s' % (self.host_address, rtype, params)
        msg = urllib2.Request(url, headers=self.HEADERS)
        res = urllib2.urlopen(msg)

        response = res.read()

        return response

    def show_namespace(self, json_list):
        url = '%s/namespaces/%s' % (self.host_address, json_list.get('namespace'))
        response = requests.get(url, headers=self.HEADERS, verify=False)
        log.info('show the namespace result is %s, type is %s' % (response.text, type(response.text)))
        return response.text

    def post_namespace(self, json_list):
        url = '%s/namespaces' % self.host_address
        response = requests.post(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)
        log.info('post namespace result is %s, type is %s' % (response.text, type(response.text)))

        return json.loads(str(response.text))

    def post_secret(self, json_list):
        namespace = json_list.get('metadata').get('namespace')
        url = '%s/namespaces/%s/secrets' % (self.host_address, namespace)
        response = requests.post(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)

        log.info('post secret result is %s, type is %s' % (response.text, type(response.text)))

        return json.loads(str(response.text))

    def post_account(self, dict_data):
        namespace = dict_data.get('metadata').get('namespace')
        url = '%s/namespaces/%s/serviceaccounts/default' % (self.host_address, namespace)
        response = requests.put(url, data=json.dumps(dict_data), headers=self.HEADERS, verify=False)

        log.info('post serviceaccount result is %s, type is %s' % (response.text, type(response.text)))

        return json.loads(str(response.text))

    def get_namespace_resource(self, json_list):

        rtype = json_list.pop('rtype')

        namespace = json_list.get('namespace')
        url = '%s/namespaces/%s/%s' % (self.host_address, namespace, rtype)

        msg = requests.get(url, headers=self.HEADERS, verify=False).text
        response = json.loads(str(msg))

        return response

    def get_name_resource(self, json_list):

        rtype = json_list.pop('rtype')
        namespace = json_list.get('metadata').get('namespace')
        name = json_list.get('metadata').get('name')
        url = '%s/namespaces/%s/%s/%s' % (self.host_address, namespace, rtype, name)
        ret = requests.get(url, headers=self.HEADERS, verify=False).text
        log.info('the resources messages is %s,type is %s' % (ret, type(ret)))
        return json.loads(str(ret))

    def post_namespace_resource(self, dict_data):

        namespace = dict_data.get('metadata').get('namespace')
        c_type = dict_data.pop('rtype')
        url = '%s/namespaces/%s/%s' % (self.host_address, namespace, c_type)

        the_page = requests.post(url, data=json.dumps(dict_data), headers=self.HEADERS, verify=False)
        response = the_page.text

        return response

    def post_ingress(self, dict_data):
        namespace = dict_data.get('metadata').get('namespace')
        url = '%s/%s/ingresses' % (self.ing_address, namespace)

        result = requests.post(url, data=json.dumps(dict_data), headers=self.HEADERS, verify=False)
        log.info('ingress:  create the ingress result is: %s, type is: %s' % (result, type(result)))

        return json.loads(result.text)

    def get_ingress(self, dict_data):
        namespace = dict_data.get('namespace')
        name = dict_data.get('name')
        url = '%s/%s/ingresses/%s' % (self.ing_address, namespace, name)

        result = requests.get(url, headers=self.HEADERS, verify=False)
        log.info('get the default ingress msg is: %s, type is: %s' % (result, type(result)))

        return json.loads(result.text)

    def update_ingress(self, dict_data):
        log.info('update the ingress, the json data is: %s' % dict_data)
        namespace = dict_data.get('metadata').get('namespace')
        name = dict_data.get('metadata').get('name')

        url = '%s/%s/ingresses/%s' % (self.ing_address, namespace, name)

        result = requests.put(url, data=json.dumps(dict_data), headers=self.HEADERS, verify=False)
        log.info('update the ingress result is: %s' % result.text)
        return json.loads(result.text)

    def delete_name_resource(self, json_list):

        rtype = json_list.pop('rtype')
        namespace = json_list.get('namespace')
        name = json_list.get('name')

        if rtype == 'ingress':
            url = '%s/%s/ingresses/%s' % (self.ing_address, namespace, name)
            result = requests.delete(url, headers=self.HEADERS, verify=False)
            log.info('ingress:  delete the ingress result is: %s' % result)

            return json.loads(result.text)

        url = '%s/namespaces/%s/%s/%s' % (self.host_address, namespace, rtype, name)
        response = requests.delete(url, headers=self.HEADERS, verify=False)

        log.info('delete resource result is %s, type is: %s' % (response, type(response)))
        return json.loads(str(response.text))

    def patch_name_resource(self, json_list):

        rtype = json_list.pop('rtype')

        if json_list.get('namespace'):
            namespace = json_list.pop('namespace')
        else:
            namespace = 'default'
        if json_list.get('name'):
            name = json_list.pop('name')

        else:
            m_name = '输入资源名,才可以进行修改'
            return m_name

        url = '%s/namespaces/%s/%s/%s' % (self.host_address, namespace, rtype, name)
        the_page = requests.patch(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)
        response = the_page.text

        return response

    def put_name_resource(self, json_list):
        rtype = json_list.pop('rtype')
        namespace = json_list.get('metadata').get('namespace')
        name = json_list.get('metadata').get('name')

        url = '%s/namespaces/%s/%s/%s' % (self.host_address, namespace, rtype, name)
        the_page = requests.put(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)
        log.info('kubernetes update result(to text) is:%s, type is : %s' % (the_page.text, type(the_page)))
        return request_result(0, str(the_page))

    def post_nohup_resource(self, json_list):
        global host_address
        rtype = json_list.pop('rtype')
        url = '%s/%s' % (host_address, rtype)
        the_page = requests.post(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)
        response = the_page.text
        return response

    def put_pods_status(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        url = '%s/namespaces/%s/pods/%s/status' % (host_address, namespace, name)
        response = requests.put(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)
        return response

    def post_pods_binding(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        url = '%s/namespaces/%s/pods/%s/binding' % (host_address, namespace, name)
        response = requests.post(url, data=json.dumps(json_list), headers=self.HEADERS, verify=False)
        return response

    def get_pods_exec(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        params = urllib.urlencode(json_list)
        url = '%s/namespaces/%s/pods/%s/exec?%s' % (host_address, namespace, name, params)
        response = requests.get(url, json_list)
        return response

    def post_pods_exec(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        url = '%s/namespaces/%s/pods/%s/exec' % (host_address, namespace, name)
        response = requests.post(url, json.dumps(json_list))
        return response

    def get_pods_log(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        params = urllib.urlencode(json_list)
        url = '%s/namespaces/%s/pods/%s/log?%s' % (host_address, namespace, name, params)
        response = requests.get(url, json_list)
        return response

    def get_pods_portforward(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        params = urllib.urlencode(json_list)
        url = '%s/namespaces/%s/pods/%s/portforward?%s' % (host_address, namespace, name, params)
        response = requests.get(url, json_list)
        return response

    def post_pods_portforward(self, json_list):
        global host_address
        namespace = json_list.pop('namespace')
        name = json_list.pop('name')
        url = '%s/namespaces/%s/pods/%s/portforward' % (host_address, namespace, name)
        response = requests.post(url, json.dumps(json_list))
        return response

