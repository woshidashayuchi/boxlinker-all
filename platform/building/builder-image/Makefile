.PHONY: test build data

IMAGE=remind101/conveyor-builder
TAG=master
DATA_IMAGE=conveyor-builder-data
EMAIL=330785652@qq.com

test: bootstrap
	docker run --privileged=true \
		--volumes-from=data \
		-e CACHE=off \
		-e REPOSITORY=cabernety/chat-demo \
		-e BRANCH=master \
		-e SHA=d10a2c0f4f24b9f9a25192e63233b33a44bc0301 \
		-e DRY=true \
		-it --rm --entrypoint bash \
		${IMAGE}:${TAG}

bootstrap: build data

build: Dockerfile bin/*
	docker build -t ${IMAGE}:${TAG} .

data: data/.docker/config.json data/.ssh/id_rsa
	docker rm data || true
	docker create --name data \
		-v ${PWD}/data/.ssh:/var/run/conveyor/.ssh \
		-v ${PWD}/data/.docker/config.json:/var/run/conveyor/.docker/config.json \
		alpine:3.1 sh

data/.docker/config.json:
	cp ${HOME}/.docker/config.json data/.docker/config.json

data/.ssh/id_rsa:
	ssh-keygen -t rsa -b 4096 -C ${EMAIL} -f data/.ssh/id_rsa -P ""
