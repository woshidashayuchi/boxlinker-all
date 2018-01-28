# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

import json
import pika
import uuid

from time import sleep
from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.single import Singleton


class RabbitmqClient(object):

    def mq_connect(self, mq_server01=conf.mq_server01,
                   mq_server02=conf.mq_server02,
                   mq_port=conf.mq_port):

        log.debug('Connecting to rabbitmq server, server01=%s, server02=%s'
                  % (mq_server01, mq_server02))

        try:
            self.connection = pika.BlockingConnection(
                              pika.ConnectionParameters(
                                   host=mq_server01, port=mq_port))
            self.channel = self.connection.channel()
        except Exception, e:
            log.error('rabbitmq server %s connection error: reason=%s'
                      % (mq_server01, e))
            try:
                self.connection = pika.BlockingConnection(
                                  pika.ConnectionParameters(
                                       host=mq_server02, port=mq_port))
                self.channel = self.connection.channel()
            except Exception, e:
                log.error('rabbitmq server %s connection error: reason=%s'
                          % (mq_server02, e))
                raise

    def mq_disconnect(self):
        log.debug('Disconnect from rabbitmq server')
        self.channel.close()
        self.connection.close()

    def on_response(self, channel, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def callback_create(self):
        log.debug('Create callback queue')
        self.callback_queue = self.channel.queue_declare(
                              exclusive=True).method.queue
        self.channel.basic_consume(self.on_response, queue=self.callback_queue)

    def broad_exchange(self, exchange_name):
        self.channel.exchange_declare(
                     exchange=exchange_name,
                     exchange_type='fanout')

    def rpc_call(self, queue_name, json_data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   properties=pika.BasicProperties(
                                              reply_to=self.callback_queue,
                                              correlation_id=self.corr_id,
                                              ),
                                   body=str(json_data))

    def rpc_cast(self, queue_name, json_data):
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   body=str(json_data))

    def broad_cast(self, exchange_name, json_data):
        self.channel.basic_publish(exchange=exchange_name,
                                   routing_key='',
                                   body=str(json_data))

    def get_response(self, timeout, queue_name):
        cnt = 0
        timeout = int(timeout) * 10
        while self.response is None:
            cnt += 1
            if cnt >= timeout:
                log.warning('RPC client exec time out, queue = %s' % queue_name)
                self.response = request_result(597)
                return
            self.connection.sleep(0.1)
            self.connection.process_data_events()

    def rpc_call_client(self, queue_name, timeout, dict_data):
        try:
            json_data = json.dumps(dict_data)
            self.mq_connect()
            self.callback_create()
            self.rpc_call(queue_name, json_data)
            self.get_response(timeout, queue_name)
            self.mq_disconnect()
            log.info('rabbitmq get the response is:%s,type:%s' % (self.response, type(self.response)))
            return json.loads(self.response)
        except Exception, e:
            log.error('RabbitMQ call client exec error: queue=%s, reason=%s'
                      % (queue_name, e))
            raise

    def rpc_cast_client(self, queue_name, dict_data):
        try:
            json_data = json.dumps(dict_data)
            self.mq_connect()
            self.rpc_cast(queue_name, json_data)
            self.mq_disconnect()
        except Exception, e:
            log.error('RabbitMQ cast client exec error: queue=%s, reason=%s'
                      % (queue_name, e))
            raise

    def broadcast_client(self, exchange_name, dict_data):
        try:
            json_data = json.dumps(dict_data)
            self.mq_connect()
            self.broad_exchange(exchange_name)
            self.broad_cast(exchange_name, json_data)
            self.mq_disconnect()
        except Exception, e:
            log.error(
                'RabbitMQ broadcast client exec error: exchange=%s, reason=%s'
                % (exchange_name, e))
            raise
