
VERSION = latest
DOC_IMAGE_PREFIX = index.boxlinker.com/boxlinker
DOC_IMAGE_NAME = docs

doc:
	cd docs && apidoc -i ../platform/ -o docs/ -e node_modules -e vendor
	cd docs && docker build -t ${DOC_IMAGE_PREFIX}/${DOC_IMAGE_NAME}:${VERSION} .
	docker push ${DOC_IMAGE_PREFIX}/${DOC_IMAGE_NAME}:${VERSION}
