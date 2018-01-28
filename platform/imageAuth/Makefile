all: push

TAG = latest
PREFIX = index.boxlinker.com/boxlinker/imagerepo-base
IMAGEREPO_NAME = testimagerepo


gitpush:
	git commit -a -m "...."
	git push origin develop


gitpull:
	git pull origin develop

restart: gitpull
	docker-compose stop
	docker-compose rm -f
	docker-compose up -d

debugrestart:
	git pull origin develop
	docker-compose -f docker-compose-debug.yml stop
	docker-compose -f docker-compose-debug.yml rm -f
	docker-compose -f docker-compose-debug.yml up -d


build:
	docker build -t $(PREFIX):$(TAG) .

push: build
	docker push $(PREFIX):$(TAG)

test: build
	docker run --name=${IMAGEREPO_NAME} -it -p 8099:8001 $(PREFIX):$(TAG)

stop:
	docker stop ${IMAGEREPO_NAME} || true
	docker rm -f ${IMAGEREPO_NAME} || true

test: build stop
	docker run --name=${IMAGEREPO_NAME} -it -p 8099:8001 $(PREFIX):$(TAG)

apilog:
	docker exec -it v10_imagerepo-apiserver_1 tail -f /var/log/cloud.log

calllog:
	docker exec -it v10_imagerepo-callserver_1 tail -f /var/log/cloud.log
