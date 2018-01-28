all: push

# 0.0 shouldn't clobber any released builds
TAG = latest
PREFIX = index.boxlinker.com/boxlinker/servicelb

server: lb.go
	CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o lb ./lb.go ./loadbalancer_log.go

container: server
	docker build -t $(PREFIX):$(TAG) -f Dockerfile.lb .

push: container
	docker push $(PREFIX):$(TAG)

clean:
	docker rmi -f $(PREFIX):$(TAG) || true
