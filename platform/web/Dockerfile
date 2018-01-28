FROM index.boxlinker.com/library/alpine-node:latest

RUN mkdir /src

ADD . /src


WORKDIR /src/build

EXPOSE 3000


CMD ["node","server.js"]
