#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 读写Kafka的工具模块
from kafka import KafkaConsumer

group_id = "test"
bootstrap_servers = "hadoop-master:9092,hadoop-slave1:9092,hadoop-slave2:9092"


def read_kafka(topic):
    """
    读取Kafka数据
    :param topic:       消费的topic
    :return:            consumer对象
    """
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
    return consumer


def write_kafka():
    pass


if __name__ == '__main__':
    obj = read_kafka()
    print(obj)