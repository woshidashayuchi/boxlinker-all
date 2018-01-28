FROM index.boxlinker.com/library/alpine-node:latest

RUN mkdir /app
COPY . /app

WORKDIR /app

ENTRYPOINT ["node","lib/index.js"]
