#!/usr/bin/env bash

apidoc -i user/ -o apidoc/user
apidoc -i registry/ -o apidoc/registry
apidoc -i oauth/ -o apidoc/oauth
apidoc -i v1/usercenter/ -o apidoc/usercenter -c view/v1/
apidoc -i v1/repository/ -o apidoc/repository
apidoc -i v2/oauthclient/ -o apidoc/v2oauth
apidoc -i icon/ -o apidoc/icon
apidoc -i v1/otherServer -o apidoc/otherServer