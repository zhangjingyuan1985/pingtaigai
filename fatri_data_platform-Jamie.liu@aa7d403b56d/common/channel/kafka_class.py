#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 读写Kafka的工具模块
from kafka import KafkaConsumer, KafkaProducer, KafkaClient
from kafka.errors import KafkaError

from conf.config import Config

import json

from common.model.kafka_model import KafkaLog, KafkaOffset
from common.db.mysql.mysql_utils import Mysql


class Kafka(object):
    def __init__(self, bootstrap_servers=Config().get_conf("Kafka", "kafka.bootstrap_servers"),
                 group_id=Config().get_conf("Kafka", "kafka.group_id"),
                 auto_offset_reset=Config().get_conf("Kafka", "kafka.auto_offset_reset")):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset

    def create_topic(self, topic):
        pass

    def read_kafka(self, topic):
        """
            读取Kafka数据
            :param topic:       消费的topic
            :return:            consumer对象
            """
        consumer = KafkaConsumer(topic, bootstrap_servers=self.bootstrap_servers, group_id=self.group_id,
                                 auto_offset_reset=self.auto_offset_reset)
        return consumer

    def write_kafka(self, topic, message):
        """
        写入kafka
        :param topic:           生产的topic
        :param message:         生产的消息
        :return:
        """
        if not topic or not message:
            print("write kafka failed, topic and message can not empty")
            return
        producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        try:
            msg = json.dumps(message)
            producer_record = producer.send(topic, msg.encode("utf-8"))
            self.write_offset(producer_record, topic)
        except KafkaError as e:
            print(e)
        finally:
            producer.close()

    def write_offset(self, producer_record, topic):
        mysql = Mysql()
        try:
            value = producer_record.get(timeout=3)
            offset = value.offset
            partition = value.partition
            create_time = value.timestamp
            kafka_offset = KafkaLog(self.bootstrap_servers, self.group_id, topic, partition, offset, create_time)
            mysql.add(kafka_offset)
        except Exception as e:
            mysql.rollback()
            print(e)
        finally:
            mysql.close()

    def update_offset(self, message):
        mysql = Mysql()
        offset = message.offset
        partition = message.partition
        consume_time = message.timestamp
        topic = message.topic
        try:
            consume_count = int(mysql.session.query(KafkaLog.consume_count). \
                                filter_by(bootstrap_servers=self.bootstrap_servers, topic=topic,
                                          offset=offset, partition=partition)
                                .one().consume_count) + 1
            mysql.session.query(KafkaLog). \
                filter_by(bootstrap_servers=self.bootstrap_servers, topic=topic,
                          offset=offset, partition=partition). \
                update({"consume_time": consume_time, "status": 1, "consume_count": consume_count})
            kafka_offset = mysql.session.query(KafkaOffset).\
                filter_by(bootstrap_servers=self.bootstrap_servers, group_id=self.group_id,
                          topic=topic, partition=partition)
            if len(kafka_offset.all()):
                mysql.add(KafkaOffset(self.bootstrap_servers, self.group_id, topic, partition, offset, consume_time))
            else:
                kafka_offset.update({"offset": offset, "consume_time": consume_time})
            mysql.session.commit()
        except Exception as e:
            print(e)
            mysql.rollback()
        finally:
            mysql.close()

    def get_brokers(self):
        brokers_cache = []
        client = KafkaClient(bootstrap_servers=self.bootstrap_servers, request_timeout_ms=3000)
        if not brokers_cache:
            brokers = client.cluster.brokers()
            if brokers:
                brokers_cache.extend([f"{x.host}:{x.port}" for x in brokers])
        return ",".join(brokers_cache)

    def get_partitions(self, topic):
        partition_cache = []
        if not partition_cache or topic not in partition_cache:
            client = KafkaClient(bootstrap_servers=self.bootstrap_servers, request_timeout_ms=300000)
            partitions = client.cluster.available_partitions_for_topic(topic)
            if partitions:
                partition_cache[topic] = [x for x in partitions]
            else:
                return []
        return partition_cache[topic]


# if __name__ == '__main__':
#     kafka = Kafka("8.129.43.47:9092,8.129.43.47:9093,8.129.43.47:9094")
#
#     kafka.get_brokers()
#     kafka.get_partitions("test")
#     consumer = kafka.read_kafka("al-s003-evt-model")
#     consumer.topics()
#     for message in consumer:
#         print(message)
#     kafka.write_kafka(None, None)
