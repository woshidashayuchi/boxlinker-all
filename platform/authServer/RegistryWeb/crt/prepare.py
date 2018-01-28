#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals # We require Python 2.6 or later
from string import Template
import random
import string
import os
import sys
from io import open

import platform


sysstr = platform.system()  # Windows测试模式

if sys.version_info[:3][0] == 2:
    import ConfigParser as ConfigParser
    import StringIO as StringIO

if sys.version_info[:3][0] == 3:
    import configparser as ConfigParser
    import io as StringIO

def validate(conf): 
    if len(conf.get("configuration", "secret_key")) != 16:
        raise Exception("Error: The length of secret key has to be 16 characters!")

#Read configurations
conf = StringIO.StringIO()
conf.write("[configuration]\n")


conf.write(open("deploy.cfg").read())

conf.seek(0, os.SEEK_SET)
rcp = ConfigParser.RawConfigParser()
rcp.readfp(conf)

validate(rcp)



customize_crt = rcp.get("configuration", "customize_crt")
crt_country = rcp.get("configuration", "crt_country")
crt_state = rcp.get("configuration", "crt_state")
crt_location = rcp.get("configuration", "crt_location")
crt_organization = rcp.get("configuration", "crt_organization")
crt_organizationalunit = rcp.get("configuration", "crt_organizationalunit")
crt_commonname = rcp.get("configuration", "crt_commonname")
crt_email = rcp.get("configuration", "crt_email")

verify_remote_cert = rcp.get("configuration", "verify_remote_cert")
secret_key = rcp.get("configuration", "secret_key")
########

ui_secret = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(16))  

base_dir = os.path.dirname(__file__)
config_dir = os.path.join(base_dir, "config")



def render(src, dest, **kw):
    t = Template(open(src, 'r').read())
    with open(dest, 'w') as f:
        f.write(t.substitute(**kw))
    print("Generated configuration file: %s" % dest)

registry_conf = os.path.join(config_dir, "registry", "config.yml")
db_conf_env = os.path.join(config_dir, "db", "env")
docker_compose_conf = os.path.join(base_dir, "docker-compose.yml")


docker_compose_conf_debug = os.path.join(base_dir, "docker-compose_debug.yml")


registry_conf_path = os.path.join(config_dir, "registry")
if os.path.exists(registry_conf_path):
    pass
else:
    os.makedirs(registry_conf_path)


conf_files = [ registry_conf, db_conf_env ]
def rmdir(cf):
    for f in cf:
        if os.path.exists(f):
            print("Clearing the configuration file: %s" % f)
            os.remove(f)
rmdir(conf_files)





def validate_crt_subj(dirty_subj):
    subj_list = [item for item in dirty_subj.strip().split("/") \
        if len(item.split("=")) == 2 and len(item.split("=")[1]) > 0]
    return "/" + "/".join(subj_list)

FNULL = open(os.devnull, 'w')

from functools import wraps
def stat_decorator(func):
    @wraps(func)
    def check_wrapper(*args, **kwargs):
        stat = func(*args, **kwargs)
        message = "Generated configuration file: %s" % kwargs['path'] \
                if stat == 0 else "Fail to generate %s" % kwargs['path']
        print(message)
        if stat != 0:
            sys.exit(1)
    return check_wrapper

@stat_decorator
def check_private_key_stat(*args, **kwargs):
    return subprocess.call(["openssl", "genrsa", "-out", kwargs['path'], "1024"],\
        stdout=FNULL, stderr=subprocess.STDOUT)

@stat_decorator
def check_certificate_stat(*args, **kwargs):
    dirty_subj = "/C={0}/ST={1}/L={2}/O={3}/OU={4}/CN={5}/emailAddress={6}"\
        .format(crt_country, crt_state, crt_location, crt_organization,\
        crt_organizationalunit, crt_commonname, crt_email)
    subj = validate_crt_subj(dirty_subj)
    return subprocess.call(["openssl", "req", "-new", "-x509", "-key",\
        private_key_pem, "-out", root_crt, "-days", "3650", "-subj", subj], \
        stdout=FNULL, stderr=subprocess.STDOUT)

def openssl_is_installed(stat):
    if stat == 0:
        return True
    else:
        print("Cannot find openssl installed in this computer\nUse default SSL certificate file")
        return False

if customize_crt == 'on':
    import subprocess
    shell_stat = subprocess.check_call(["which", "openssl"], stdout=FNULL, stderr=subprocess.STDOUT)
    if openssl_is_installed(shell_stat):
        private_key_pem = os.path.join(config_dir, "registry", "private_key.pem")
        root_crt = os.path.join(config_dir, "registry", "root.crt")
        crt_conf_files = [ private_key_pem, root_crt ]
        rmdir(crt_conf_files)

        check_private_key_stat(path=private_key_pem)
        check_certificate_stat(path=root_crt)

FNULL.close()
print("The configuration files are ready, please use docker-compose to start the service.")
