#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@time: 16/9/1 下午2:49
"""

# References:
#  https://github.com/kwk/docker-registry-setup#manual-token-based-workflow-to-list-repositories
#  https://docs.docker.com/registry/spec/api
#  http://docs.python-requests.org/en/latest/user/authentication/#new-forms-of-authentication
#  https://github.com/JonathonReinhart/py-docker-registry


import sys
import requests
from requests.auth import AuthBase, HTTPBasicAuth


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, req):
        req.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return req


class RegistryError(Exception):
    def __init__(self, message, code=None, detail=None):
        super(RegistryError, self).__init__(message)
        self.code = code
        self.detail = detail

    @classmethod
    def from_json(cls, json):
        """
        Encapsulate an error response in an exception
        :param json: the JSON data returned by the API request
        """
        errors = json.get('errors')
        if not errors or len(errors) == 0:
            return cls('Unknown error')

        # For simplicity, we'll just include the first error.
        err = errors[0]
        return cls(
            message=err.get('message'),
            code=err.get('code'),
            detail=err.get('detail')
        )


class AuthenticationError(Exception):
    pass


class Registry:
    def __init__(self, url, username, password, verify_ssl=False):
        url = url.rstrip('/')
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        self.url = url
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl

        # We keep just the last-used token around,
        # to prevent unnecessary requests both with the RegistryWeb and user server.
        # It is yet to be seen how well this single-entry cache performs across varying scopes of API calls.
        self.auth = None
        self.headers = None


    def authenticate(self):
        """ Forcefully user for testing """
        r = requests.head(self.url + '/v2/', verify=self.verify_ssl)
        self._authenticate_for(r)

    def _authenticate_for(self, resp):
        """
        Authenticate to satsify the unauthorized response
        Get the user. info from the headers
        :param resp:
        :return:
        """
        scheme, params = resp.headers['Www-Authenticate'].split(None, 1)

        print '---- _authenticate_for ----'
        print scheme
        print params
        assert (scheme == 'Bearer')
        info = {k: v.strip('"') for k, v in (i.split('=') for i in params.split(','))}
        print info

        # Request a token from the user server
        params = {k: v for k, v in info.iteritems() if k in ('service', 'scope')}
        auth = HTTPBasicAuth(self.username, self.password)

        print 's--s-s-s-s-ss'
        print params
        r2 = requests.get(info['realm'], params=params, auth=auth, verify=self.verify_ssl)
        if r2.status_code == 401:
            raise AuthenticationError()

        r2.raise_for_status()
        print 'ssssss------------ssss'
        print r2.json()['token']

        self.auth = BearerAuth(r2.json()['token'])
        self.headers = '{}'.format(r2.json()['token'])


    def _do_get(self, endpoint):
        url = '{0}/v2/{1}'.format(self.url, endpoint)

        # Try to use previous bearer token
        r = requests.get(url, auth=self.auth, verify=self.verify_ssl)
        print url

        # If necessary, try to authenticate and try again
        if r.status_code == 401:
            self._authenticate_for(r)
            headers = {'Authenticate': self.auth}
            r = requests.get(url, auth=self.auth, verify=self.verify_ssl) #, headers=headers)

        json = r.json()
        print json
        if r.status_code != 200:
            raise RegistryError.from_json(json)

        return json

    def get_tags(self, name):
        endpoint = '{name}/tags/list'.format(name=name)
        return self._do_get(endpoint=endpoint)

    def get_manifest(self, name, ref):
        endpoint = '{name}/manifests/{ref}'.format(name=name, ref=ref)
        return self._do_get(endpoint=endpoint)

    def get_catalog(self):
        return self._do_get('_catalog')

    def api_test(self):
        return self._do_get('')

