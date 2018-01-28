all: push

PREFIX = index.boxlinker.com/boxlinker/auth-build
TAG = latest

scp: gen
	scp cmd/server root@123.56.9.18:/go/bin

gen:
	cd cmd && CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o server

build: gen
	docker build -t ${PREFIX}:${TAG} .

push: build
	docker push ${PREFIX}:${TAG}