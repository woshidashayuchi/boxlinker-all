all: push

# 0.0 shouldn't clobber any released builds
TAG = latest
PREFIX = index.boxlinker.com/boxlinker
IMAGE_NAME = nginx-apidoc

container:
	docker build -t ${PREFIX}/${IMAGE_NAME}:${TAG} .

push: container
	docker push ${PREFIX}/${IMAGE_NAME}:${TAG}

clean:
	docker rmi -f $(PREFIX):$(TAG) || true
