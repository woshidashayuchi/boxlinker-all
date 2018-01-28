FROM index.boxlinker.com/library/node:latest

RUN mkdir /app
COPY . /app

WORKDIR /app

ENTRYPOINT ["node","lib/index.js"]