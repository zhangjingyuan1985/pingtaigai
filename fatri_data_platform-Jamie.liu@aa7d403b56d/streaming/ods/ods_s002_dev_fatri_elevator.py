#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-15 11:45:01
# @Author  : Happiless.zhang (Happiless.zhang@fatritech.com)
# @Version : v_1.0
# @note    : 从Kafka中读取设备表的数据并写入HBase和Kafka中
# @param    CONSUMER_TOPIC:     消费的topic
# @param    PRODUCER_TOPIC:     要生产的topic
# @param    SOURCE_TABLE_NAME:  源数据表名
# @param    TARGET_TABLE_NAME:  目标数据表名
# @param    COLUMN_FAMILY:      列族名
# @param    ROW_KEY:            rowkey字段
from common.channel.kafka_class import Kafka
from common.db.hbase.hbase_class import HBase
import json


CONSUMER_TOPIC = "example4"
PRODUCER_TOPIC = "ODS-S002-DEV-FATRI-ELEVATOR"
SOURCE_TABLE_NAME = "fatri_elevator"
TARGET_TABLE_NAME = "ods:ODS_S002_DEV_FATRI_ELEVATOR"
COLUMN_FAMILY = "info"
ROW_KEY = "DeviceId"


def main():
    # 1.获取Kafka对象
    kafka = Kafka()
    # 2.读取Kafka数据
    consumer = kafka.read_kafka(CONSUMER_TOPIC)
    # 3.获取HBase对象
    hbase = HBase()
    # 4.创建HBase表
    hbase.get_create_table(TARGET_TABLE_NAME, COLUMN_FAMILY)
    for message in consumer:
        data = json.loads(message.value)
        if data['table'] == SOURCE_TABLE_NAME:
            obj = data['data'][0]
            row_key = obj[ROW_KEY]
            # 5.写入HBase
            hbase.put_row(TARGET_TABLE_NAME, COLUMN_FAMILY, row_key, dict(obj))
            # 6.写入Kafka
            message = json.dumps({TARGET_TABLE_NAME: obj})
            kafka.write_kafka(PRODUCER_TOPIC, message)


if __name__ == '__main__':
    main()
