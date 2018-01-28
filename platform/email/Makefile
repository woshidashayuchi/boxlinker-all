all: push

# 0.0 shouldn't clobber any released builds
TAG = 1.0.3
PREFIX = index.boxlinker.com/boxlinker
IMAGE_NAME = send-email

container:
	docker build -t ${PREFIX}/${IMAGE_NAME}:${TAG} .

push: container
	docker push ${PREFIX}/${IMAGE_NAME}:${TAG}

docs:
	apidoc -i lib/ -o doc/

clean:
	docker rmi -f $(PREFIX):$(TAG) || true
