all: push

# 0.0 shouldn't clobber any released builds
TAG = latest
PREFIX = index.boxlinker.com/boxlinker/rolling-update

server: main.go
	CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o rolling-update ./main.go

container: server
	docker build -t $(PREFIX):$(TAG) .

push: container
	docker push $(PREFIX):$(TAG)

test: container
	docker run -it -p 8080:80 $(PREFIX):$(TAG) --listen=":8080"

clean:
	# remove servicelb and contrib-haproxy images
	docker rmi -f $(PREFIX):$(TAG) || true

# docker build -t registry.36ap.com/admin/nginx-demo:latest -f Dockerfile.test . && docker push registry.36ap.com/admin/nginx-demo:latest
